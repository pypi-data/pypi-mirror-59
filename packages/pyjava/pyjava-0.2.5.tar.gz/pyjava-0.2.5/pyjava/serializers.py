#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import collections
import itertools
import marshal
import struct
import sys
import types
import zlib
from itertools import chain, product

from pyjava import cloudpickle
from pyjava.datatype.types import _check_series_localize_timestamps, _check_series_convert_timestamps_internal

if sys.version < '3':
    import cPickle as pickle
    from itertools import izip as zip, imap as map
else:
    import pickle

    basestring = unicode = str
    xrange = range
pickle_protocol = pickle.HIGHEST_PROTOCOL


class SpecialLengths(object):
    END_OF_DATA_SECTION = -1
    PYTHON_EXCEPTION_THROWN = -2
    TIMING_DATA = -3
    END_OF_STREAM = -4
    NULL = -5
    START_ARROW_STREAM = -6
    READ_SCHEMA = -7


class Serializer(object):

    def dump_stream(self, iterator, stream):
        """
        Serialize an iterator of objects to the output stream.
        """
        raise NotImplementedError

    def load_stream(self, stream):
        """
        Return an iterator of deserialized objects from the input stream.
        """
        raise NotImplementedError

    def _load_stream_without_unbatching(self, stream):
        """
        Return an iterator of deserialized batches (iterable) of objects from the input stream.
        If the serializer does not operate on batches the default implementation returns an
        iterator of single element lists.
        """
        return map(lambda x: [x], self.load_stream(stream))

    # Note: our notion of "equality" is that output generated by
    # equal serializers can be deserialized using the same serializer.

    # This default implementation handles the simple cases;
    # subclasses should override __eq__ as appropriate.

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "%s()" % self.__class__.__name__

    def __hash__(self):
        return hash(str(self))


class FramedSerializer(Serializer):
    """
    Serializer that writes objects as a stream of (length, data) pairs,
    where `length` is a 32-bit integer and data is `length` bytes.
    """

    def __init__(self):
        # On Python 2.6, we can't write bytearrays to streams, so we need to convert them
        # to strings first. Check if the version number is that old.
        self._only_write_strings = sys.version_info[0:2] <= (2, 6)

    def dump_stream(self, iterator, stream):
        for obj in iterator:
            self._write_with_length(obj, stream)

    def load_stream(self, stream):
        while True:
            try:
                yield self._read_with_length(stream)
            except EOFError:
                return

    def _write_with_length(self, obj, stream):
        serialized = self.dumps(obj)
        if serialized is None:
            raise ValueError("serialized value should not be None")
        if len(serialized) > (1 << 31):
            raise ValueError("can not serialize object larger than 2G")
        write_int(len(serialized), stream)
        if self._only_write_strings:
            stream.write(str(serialized))
        else:
            stream.write(serialized)

    def _read_with_length(self, stream):
        length = read_int(stream)
        if length == SpecialLengths.END_OF_DATA_SECTION:
            raise EOFError
        elif length == SpecialLengths.NULL:
            return None
        obj = stream.read(length)
        if len(obj) < length:
            raise EOFError
        return self.loads(obj)

    def dumps(self, obj):
        """
        Serialize an object into a byte array.
        When batching is used, this will be called with an array of objects.
        """
        raise NotImplementedError

    def loads(self, obj):
        """
        Deserialize an object from a byte array.
        """
        raise NotImplementedError


class ArrowCollectSerializer(Serializer):
    """
    Deserialize a stream of batches followed by batch order information. Used in
    DataFrame._collectAsArrow() after invoking Dataset.collectAsArrowToPython() in the JVM.
    """

    def __init__(self):
        self.serializer = ArrowStreamSerializer()

    def dump_stream(self, iterator, stream):
        return self.serializer.dump_stream(iterator, stream)

    def load_stream(self, stream):
        """
        Load a stream of un-ordered Arrow RecordBatches, where the last iteration yields
        a list of indices that can be used to put the RecordBatches in the correct order.
        """
        # load the batches
        for batch in self.serializer.load_stream(stream):
            yield batch

        # load the batch order indices or propagate any error that occurred in the JVM
        num = read_int(stream)
        if num == -1:
            error_msg = UTF8Deserializer().loads(stream)
            raise RuntimeError("An error occurred while calling "
                               "ArrowCollectSerializer.load_stream: {}".format(error_msg))
        batch_order = []
        for i in xrange(num):
            index = read_int(stream)
            batch_order.append(index)
        yield batch_order

    def __repr__(self):
        return "ArrowCollectSerializer(%s)" % self.serializer


class ArrowStreamSerializer(Serializer):
    """
    Serializes Arrow record batches as a stream.
    """

    def dump_stream(self, iterator, stream):
        import pyarrow as pa
        import pyjava.utils as utils
        is_dev = utils.is_dev()

        if is_dev:
            print("----pyarrow version---")
            print(pa.__version__)
        writer = None
        try:
            for batch in iterator:
                if is_dev:
                    print(batch.to_pandas())
                if writer is None:
                    writer = pa.RecordBatchStreamWriter(stream, batch.schema)
                writer.write_batch(batch)

            # if iterator is empty, we should write default schema
            if writer is None:
                if is_dev:
                    print("----dump empty arrow---")
                rb = pa.RecordBatch.from_arrays([[]], schema=pa.schema([('value', pa.string())]))
                writer = pa.RecordBatchStreamWriter(stream, rb.schema)
                writer.write_batch(rb)

        finally:
            if writer is not None:
                writer.close()

    def load_stream(self, stream):
        import pyarrow as pa
        reader = pa.ipc.open_stream(stream)
        for batch in reader:
            yield batch

    def __repr__(self):
        return "ArrowStreamSerializer"


class ArrowStreamPandasSerializer(ArrowStreamSerializer):
    """
    Serializes Pandas.Series as Arrow data with Arrow streaming format.

    :param timezone: A timezone to respect when handling timestamp values
    :param safecheck: If True, conversion from Arrow to Pandas checks for overflow/truncation
    :param assign_cols_by_name: If True, then Pandas DataFrames will get columns by name
    """

    def __init__(self, timezone, safecheck, assign_cols_by_name):
        super(ArrowStreamPandasSerializer, self).__init__()
        self._timezone = timezone
        self._safecheck = safecheck
        self._assign_cols_by_name = assign_cols_by_name

    def arrow_to_pandas(self, arrow_column):

        # If the given column is a date type column, creates a series of datetime.date directly
        # instead of creating datetime64[ns] as intermediate data to avoid overflow caused by
        # datetime64[ns] type handling.
        s = arrow_column.to_pandas(date_as_object=True)

        s = _check_series_localize_timestamps(s, self._timezone)
        return s

    def _create_batch(self, series):
        """
        Create an Arrow record batch from the given pandas.Series or list of Series,
        with optional type.

        :param series: A single pandas.Series, list of Series, or list of (series, arrow_type)
        :return: Arrow RecordBatch
        """
        import pandas as pd
        import pyarrow as pa
        # Make input conform to [(series1, type1), (series2, type2), ...]
        if not isinstance(series, (list, tuple)) or \
                (len(series) == 2 and isinstance(series[1], pa.DataType)):
            series = [series]
        series = ((s, None) if not isinstance(s, (list, tuple)) else s for s in series)

        def create_array(s, t):
            mask = s.isnull()
            # Ensure timestamp series are in expected form for Spark internal representation
            if t is not None and pa.types.is_timestamp(t):
                s = _check_series_convert_timestamps_internal(s, self._timezone)
            try:
                array = pa.Array.from_pandas(s, mask=mask, type=t, safe=self._safecheck)
            except pa.ArrowException as e:
                error_msg = "Exception thrown when converting pandas.Series (%s) to Arrow " + \
                            "Array (%s). It can be caused by overflows or other unsafe " + \
                            "conversions warned by Arrow. Arrow safe type check can be " + \
                            "disabled by using SQL config " + \
                            "`spark.sql.execution.pandas.arrowSafeTypeConversion`."
                raise RuntimeError(error_msg % (s.dtype, t), e)
            return array

        arrs = []
        for s, t in series:
            if t is not None and pa.types.is_struct(t):
                if not isinstance(s, pd.DataFrame):
                    raise ValueError("A field of type StructType expects a pandas.DataFrame, "
                                     "but got: %s" % str(type(s)))

                # Input partition and result pandas.DataFrame empty, make empty Arrays with struct
                if len(s) == 0 and len(s.columns) == 0:
                    arrs_names = [(pa.array([], type=field.type), field.name) for field in t]
                # Assign result columns by schema name if user labeled with strings
                elif self._assign_cols_by_name and any(isinstance(name, basestring)
                                                       for name in s.columns):
                    arrs_names = [(create_array(s[field.name], field.type), field.name)
                                  for field in t]
                # Assign result columns by  position
                else:
                    arrs_names = [(create_array(s[s.columns[i]], field.type), field.name)
                                  for i, field in enumerate(t)]

                struct_arrs, struct_names = zip(*arrs_names)
                arrs.append(pa.StructArray.from_arrays(struct_arrs, struct_names))
            else:
                arrs.append(create_array(s, t))
        return pa.RecordBatch.from_arrays(arrs, ["_%d" % i for i in xrange(len(arrs))])

    def dump_stream(self, iterator, stream):
        """
        Make ArrowRecordBatches from Pandas Series and serialize. Input is a single series or
        a list of series accompanied by an optional pyarrow type to coerce the data to.
        [
          [[column1 values],[column2 values]] #batch_0
          [[column1 values],[column2 values]] #batch_2
          ....
          [[column1 values],[column2 values]] #batch_n
        ]
        """
        batches = (self._create_batch(series) for series in iterator)
        super(ArrowStreamPandasSerializer, self).dump_stream(batches, stream)

    def load_stream(self, stream):
        """
        Deserialize ArrowRecordBatches to an Arrow table and return as a list of pandas.Series.
        """
        batches = super(ArrowStreamPandasSerializer, self).load_stream(stream)
        import pyarrow as pa
        for batch in batches:
            yield [self.arrow_to_pandas(c) for c in pa.Table.from_batches([batch]).itercolumns()]

    def __repr__(self):
        return "ArrowStreamPandasSerializer"


class ArrowStreamPandasUDFSerializer(ArrowStreamPandasSerializer):
    """
    Serializer used by Python worker to evaluate Pandas UDFs
    """

    def __init__(self, timezone, safecheck, assign_cols_by_name, df_for_struct=False):
        super(ArrowStreamPandasUDFSerializer, self) \
            .__init__(timezone, safecheck, assign_cols_by_name)
        self._df_for_struct = df_for_struct

    def arrow_to_pandas(self, arrow_column):
        import pyarrow.types as types

        if self._df_for_struct and types.is_struct(arrow_column.type):
            import pandas as pd
            series = [super(ArrowStreamPandasUDFSerializer, self).arrow_to_pandas(column)
                          .rename(field.name)
                      for column, field in zip(arrow_column.flatten(), arrow_column.type)]
            s = pd.concat(series, axis=1)
        else:
            s = super(ArrowStreamPandasUDFSerializer, self).arrow_to_pandas(arrow_column)
        return s

    def dump_stream(self, iterator, stream):
        """
        Override because Pandas UDFs require a START_ARROW_STREAM before the Arrow stream is sent.
        This should be sent after creating the first record batch so in case of an error, it can
        be sent back to the JVM before the Arrow stream starts.
        """

        def init_stream_yield_batches():
            should_write_start_length = True
            for series in iterator:
                batch = self._create_batch(series)
                if should_write_start_length:
                    write_int(SpecialLengths.START_ARROW_STREAM, stream)
                    should_write_start_length = False
                yield batch

        return ArrowStreamSerializer.dump_stream(self, init_stream_yield_batches(), stream)

    def __repr__(self):
        return "ArrowStreamPandasUDFSerializer"


class BatchedSerializer(Serializer):
    """
    Serializes a stream of objects in batches by calling its wrapped
    Serializer with streams of objects.
    """

    UNLIMITED_BATCH_SIZE = -1
    UNKNOWN_BATCH_SIZE = 0

    def __init__(self, serializer, batchSize=UNLIMITED_BATCH_SIZE):
        self.serializer = serializer
        self.batchSize = batchSize

    def _batched(self, iterator):
        if self.batchSize == self.UNLIMITED_BATCH_SIZE:
            yield list(iterator)
        elif hasattr(iterator, "__len__") and hasattr(iterator, "__getslice__"):
            n = len(iterator)
            for i in xrange(0, n, self.batchSize):
                yield iterator[i: i + self.batchSize]
        else:
            items = []
            count = 0
            for item in iterator:
                items.append(item)
                count += 1
                if count == self.batchSize:
                    yield items
                    items = []
                    count = 0
            if items:
                yield items

    def dump_stream(self, iterator, stream):
        self.serializer.dump_stream(self._batched(iterator), stream)

    def load_stream(self, stream):
        return chain.from_iterable(self._load_stream_without_unbatching(stream))

    def _load_stream_without_unbatching(self, stream):
        return self.serializer.load_stream(stream)

    def __repr__(self):
        return "BatchedSerializer(%s, %d)" % (str(self.serializer), self.batchSize)


class FlattenedValuesSerializer(BatchedSerializer):
    """
    Serializes a stream of list of pairs, split the list of values
    which contain more than a certain number of objects to make them
    have similar sizes.
    """

    def __init__(self, serializer, batchSize=10):
        BatchedSerializer.__init__(self, serializer, batchSize)

    def _batched(self, iterator):
        n = self.batchSize
        for key, values in iterator:
            for i in range(0, len(values), n):
                yield key, values[i:i + n]

    def load_stream(self, stream):
        return self.serializer.load_stream(stream)

    def __repr__(self):
        return "FlattenedValuesSerializer(%s, %d)" % (self.serializer, self.batchSize)


class AutoBatchedSerializer(BatchedSerializer):
    """
    Choose the size of batch automatically based on the size of object
    """

    def __init__(self, serializer, bestSize=1 << 16):
        BatchedSerializer.__init__(self, serializer, self.UNKNOWN_BATCH_SIZE)
        self.bestSize = bestSize

    def dump_stream(self, iterator, stream):
        batch, best = 1, self.bestSize
        iterator = iter(iterator)
        while True:
            vs = list(itertools.islice(iterator, batch))
            if not vs:
                break

            bytes = self.serializer.dumps(vs)
            write_int(len(bytes), stream)
            stream.write(bytes)

            size = len(bytes)
            if size < best:
                batch *= 2
            elif size > best * 10 and batch > 1:
                batch //= 2

    def __repr__(self):
        return "AutoBatchedSerializer(%s)" % self.serializer


class CartesianDeserializer(Serializer):

    def __init__(self, key_ser, val_ser):
        self.key_ser = key_ser
        self.val_ser = val_ser

    def _load_stream_without_unbatching(self, stream):
        key_batch_stream = self.key_ser._load_stream_without_unbatching(stream)
        val_batch_stream = self.val_ser._load_stream_without_unbatching(stream)
        for (key_batch, val_batch) in zip(key_batch_stream, val_batch_stream):
            # for correctness with repeated cartesian/zip this must be returned as one batch
            yield product(key_batch, val_batch)

    def load_stream(self, stream):
        return chain.from_iterable(self._load_stream_without_unbatching(stream))

    def __repr__(self):
        return "CartesianDeserializer(%s, %s)" % \
               (str(self.key_ser), str(self.val_ser))


class PairDeserializer(Serializer):

    def __init__(self, key_ser, val_ser):
        self.key_ser = key_ser
        self.val_ser = val_ser

    def _load_stream_without_unbatching(self, stream):
        key_batch_stream = self.key_ser._load_stream_without_unbatching(stream)
        val_batch_stream = self.val_ser._load_stream_without_unbatching(stream)
        for (key_batch, val_batch) in zip(key_batch_stream, val_batch_stream):
            # For double-zipped RDDs, the batches can be iterators from other PairDeserializer,
            # instead of lists. We need to convert them to lists if needed.
            key_batch = key_batch if hasattr(key_batch, '__len__') else list(key_batch)
            val_batch = val_batch if hasattr(val_batch, '__len__') else list(val_batch)
            if len(key_batch) != len(val_batch):
                raise ValueError("Can not deserialize PairRDD with different number of items"
                                 " in batches: (%d, %d)" % (len(key_batch), len(val_batch)))
            # for correctness with repeated cartesian/zip this must be returned as one batch
            yield zip(key_batch, val_batch)

    def load_stream(self, stream):
        return chain.from_iterable(self._load_stream_without_unbatching(stream))

    def __repr__(self):
        return "PairDeserializer(%s, %s)" % (str(self.key_ser), str(self.val_ser))


class NoOpSerializer(FramedSerializer):

    def loads(self, obj):
        return obj

    def dumps(self, obj):
        return obj


# Hack namedtuple, make it picklable

__cls = {}


def _restore(name, fields, value):
    """ Restore an object of namedtuple"""
    k = (name, fields)
    cls = __cls.get(k)
    if cls is None:
        cls = collections.namedtuple(name, fields)
        __cls[k] = cls
    return cls(*value)


def _hack_namedtuple(cls):
    """ Make class generated by namedtuple picklable """
    name = cls.__name__
    fields = cls._fields

    def __reduce__(self):
        return (_restore, (name, fields, tuple(self)))

    cls.__reduce__ = __reduce__
    cls._is_namedtuple_ = True
    return cls


def _hijack_namedtuple():
    """ Hack namedtuple() to make it picklable """
    # hijack only one time
    if hasattr(collections.namedtuple, "__hijack"):
        return

    global _old_namedtuple  # or it will put in closure
    global _old_namedtuple_kwdefaults  # or it will put in closure too

    def _copy_func(f):
        return types.FunctionType(f.__code__, f.__globals__, f.__name__,
                                  f.__defaults__, f.__closure__)

    def _kwdefaults(f):
        # __kwdefaults__ contains the default values of keyword-only arguments which are
        # introduced from Python 3. The possible cases for __kwdefaults__ in namedtuple
        # are as below:
        #
        # - Does not exist in Python 2.
        # - Returns None in <= Python 3.5.x.
        # - Returns a dictionary containing the default values to the keys from Python 3.6.x
        #    (See https://bugs.python.org/issue25628).
        kargs = getattr(f, "__kwdefaults__", None)
        if kargs is None:
            return {}
        else:
            return kargs

    _old_namedtuple = _copy_func(collections.namedtuple)
    _old_namedtuple_kwdefaults = _kwdefaults(collections.namedtuple)

    def namedtuple(*args, **kwargs):
        for k, v in _old_namedtuple_kwdefaults.items():
            kwargs[k] = kwargs.get(k, v)
        cls = _old_namedtuple(*args, **kwargs)
        return _hack_namedtuple(cls)

    # replace namedtuple with the new one
    collections.namedtuple.__globals__["_old_namedtuple_kwdefaults"] = _old_namedtuple_kwdefaults
    collections.namedtuple.__globals__["_old_namedtuple"] = _old_namedtuple
    collections.namedtuple.__globals__["_hack_namedtuple"] = _hack_namedtuple
    collections.namedtuple.__code__ = namedtuple.__code__
    collections.namedtuple.__hijack = 1

    # hack the cls already generated by namedtuple.
    # Those created in other modules can be pickled as normal,
    # so only hack those in __main__ module
    for n, o in sys.modules["__main__"].__dict__.items():
        if (type(o) is type and o.__base__ is tuple
                and hasattr(o, "_fields")
                and "__reduce__" not in o.__dict__):
            _hack_namedtuple(o)  # hack inplace


_hijack_namedtuple()


class PickleSerializer(FramedSerializer):
    """
    Serializes objects using Python's pickle serializer:

        http://docs.python.org/2/library/pickle.html

    This serializer supports nearly any Python object, but may
    not be as fast as more specialized serializers.
    """

    def dumps(self, obj):
        return pickle.dumps(obj, pickle_protocol)

    if sys.version >= '3':
        def loads(self, obj, encoding="bytes"):
            return pickle.loads(obj, encoding=encoding)
    else:
        def loads(self, obj, encoding=None):
            return pickle.loads(obj)


class CloudPickleSerializer(PickleSerializer):

    def dumps(self, obj):
        try:
            return cloudpickle.dumps(obj, pickle_protocol)
        except pickle.PickleError:
            raise
        except Exception as e:
            import pyjava.utils as utils
            emsg = utils._exception_message(e)
            if "'i' format requires" in emsg:
                msg = "Object too large to serialize: %s" % emsg
            else:
                msg = "Could not serialize object: %s: %s" % (e.__class__.__name__, emsg)
            cloudpickle.print_exec(sys.stderr)
            raise pickle.PicklingError(msg)


class MarshalSerializer(FramedSerializer):
    """
    Serializes objects using Python's Marshal serializer:

        http://docs.python.org/2/library/marshal.html

    This serializer is faster than PickleSerializer but supports fewer datatypes.
    """

    def dumps(self, obj):
        return marshal.dumps(obj)

    def loads(self, obj):
        return marshal.loads(obj)


class AutoSerializer(FramedSerializer):
    """
    Choose marshal or pickle as serialization protocol automatically
    """

    def __init__(self):
        FramedSerializer.__init__(self)
        self._type = None

    def dumps(self, obj):
        if self._type is not None:
            return b'P' + pickle.dumps(obj, -1)
        try:
            return b'M' + marshal.dumps(obj)
        except Exception:
            self._type = b'P'
            return b'P' + pickle.dumps(obj, -1)

    def loads(self, obj):
        _type = obj[0]
        if _type == b'M':
            return marshal.loads(obj[1:])
        elif _type == b'P':
            return pickle.loads(obj[1:])
        else:
            raise ValueError("invalid serialization type: %s" % _type)


class CompressedSerializer(FramedSerializer):
    """
    Compress the serialized data
    """

    def __init__(self, serializer):
        FramedSerializer.__init__(self)
        assert isinstance(serializer, FramedSerializer), "serializer must be a FramedSerializer"
        self.serializer = serializer

    def dumps(self, obj):
        return zlib.compress(self.serializer.dumps(obj), 1)

    def loads(self, obj):
        return self.serializer.loads(zlib.decompress(obj))

    def __repr__(self):
        return "CompressedSerializer(%s)" % self.serializer


class UTF8Deserializer(Serializer):
    """
    Deserializes streams written by String.getBytes.
    """

    def __init__(self, use_unicode=True):
        self.use_unicode = use_unicode

    def loads(self, stream):
        length = read_int(stream)
        if length == SpecialLengths.END_OF_DATA_SECTION:
            raise EOFError
        elif length == SpecialLengths.NULL:
            return None
        s = stream.read(length)
        return s.decode("utf-8") if self.use_unicode else s

    def load_stream(self, stream):
        try:
            while True:
                yield self.loads(stream)
        except struct.error:
            return
        except EOFError:
            return

    def __repr__(self):
        return "UTF8Deserializer(%s)" % self.use_unicode


def read_long(stream):
    length = stream.read(8)
    if not length:
        raise EOFError
    return struct.unpack("!q", length)[0]


def write_long(value, stream):
    stream.write(struct.pack("!q", value))


def pack_long(value):
    return struct.pack("!q", value)


def read_int(stream):
    length = stream.read(4)
    if not length:
        raise EOFError
    return struct.unpack("!i", length)[0]


def write_int(value, stream):
    stream.write(struct.pack("!i", value))


def read_bool(stream):
    length = stream.read(1)
    if not length:
        raise EOFError
    return struct.unpack("!?", length)[0]


def write_with_length(obj, stream):
    write_int(len(obj), stream)
    stream.write(obj)


class ChunkedStream(object):
    """
    This is a file-like object takes a stream of data, of unknown length, and breaks it into fixed
    length frames.  The intended use case is serializing large data and sending it immediately over
    a socket -- we do not want to buffer the entire data before sending it, but the receiving end
    needs to know whether or not there is more data coming.

    It works by buffering the incoming data in some fixed-size chunks.  If the buffer is full, it
    first sends the buffer size, then the data.  This repeats as long as there is more data to send.
    When this is closed, it sends the length of whatever data is in the buffer, then that data, and
    finally a "length" of -1 to indicate the stream has completed.
    """

    def __init__(self, wrapped, buffer_size):
        self.buffer_size = buffer_size
        self.buffer = bytearray(buffer_size)
        self.current_pos = 0
        self.wrapped = wrapped

    def write(self, bytes):
        byte_pos = 0
        byte_remaining = len(bytes)
        while byte_remaining > 0:
            new_pos = byte_remaining + self.current_pos
            if new_pos < self.buffer_size:
                # just put it in our buffer
                self.buffer[self.current_pos:new_pos] = bytes[byte_pos:]
                self.current_pos = new_pos
                byte_remaining = 0
            else:
                # fill the buffer, send the length then the contents, and start filling again
                space_left = self.buffer_size - self.current_pos
                new_byte_pos = byte_pos + space_left
                self.buffer[self.current_pos:self.buffer_size] = bytes[byte_pos:new_byte_pos]
                write_int(self.buffer_size, self.wrapped)
                self.wrapped.write(self.buffer)
                byte_remaining -= space_left
                byte_pos = new_byte_pos
                self.current_pos = 0

    def close(self):
        # if there is anything left in the buffer, write it out first
        if self.current_pos > 0:
            write_int(self.current_pos, self.wrapped)
            self.wrapped.write(self.buffer[:self.current_pos])
        # -1 length indicates to the receiving end that we're done.
        write_int(-1, self.wrapped)
        self.wrapped.close()

    @property
    def closed(self):
        """
        Return True if the `wrapped` object has been closed.
        NOTE: this property is required by pyarrow to be used as a file-like object in
        pyarrow.RecordBatchStreamWriter from ArrowStreamSerializer
        """
        return self.wrapped.closed


if __name__ == '__main__':
    import doctest

    (failure_count, test_count) = doctest.testmod()
    if failure_count:
        sys.exit(-1)

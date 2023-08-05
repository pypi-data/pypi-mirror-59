# @generated by generate_proto_mypy_stubs.py.  Do not edit!
import sys
from feast.core.Source_pb2 import (
    Source as feast___core___Source_pb2___Source,
)

from feast.types.Value_pb2 import (
    ValueType as feast___types___Value_pb2___ValueType,
)

from google.protobuf.descriptor import (
    Descriptor as google___protobuf___descriptor___Descriptor,
    EnumDescriptor as google___protobuf___descriptor___EnumDescriptor,
)

from google.protobuf.duration_pb2 import (
    Duration as google___protobuf___duration_pb2___Duration,
)

from google.protobuf.internal.containers import (
    RepeatedCompositeFieldContainer as google___protobuf___internal___containers___RepeatedCompositeFieldContainer,
)

from google.protobuf.message import (
    Message as google___protobuf___message___Message,
)

from google.protobuf.timestamp_pb2 import (
    Timestamp as google___protobuf___timestamp_pb2___Timestamp,
)

from typing import (
    Iterable as typing___Iterable,
    List as typing___List,
    Optional as typing___Optional,
    Text as typing___Text,
    Tuple as typing___Tuple,
    cast as typing___cast,
)

from typing_extensions import (
    Literal as typing_extensions___Literal,
)


class FeatureSetStatus(int):
    DESCRIPTOR: google___protobuf___descriptor___EnumDescriptor = ...
    @classmethod
    def Name(cls, number: int) -> str: ...
    @classmethod
    def Value(cls, name: str) -> FeatureSetStatus: ...
    @classmethod
    def keys(cls) -> typing___List[str]: ...
    @classmethod
    def values(cls) -> typing___List[FeatureSetStatus]: ...
    @classmethod
    def items(cls) -> typing___List[typing___Tuple[str, FeatureSetStatus]]: ...
    STATUS_INVALID = typing___cast(FeatureSetStatus, 0)
    STATUS_PENDING = typing___cast(FeatureSetStatus, 1)
    STATUS_READY = typing___cast(FeatureSetStatus, 2)
STATUS_INVALID = typing___cast(FeatureSetStatus, 0)
STATUS_PENDING = typing___cast(FeatureSetStatus, 1)
STATUS_READY = typing___cast(FeatureSetStatus, 2)

class FeatureSet(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...

    @property
    def spec(self) -> FeatureSetSpec: ...

    @property
    def meta(self) -> FeatureSetMeta: ...

    def __init__(self,
        *,
        spec : typing___Optional[FeatureSetSpec] = None,
        meta : typing___Optional[FeatureSetMeta] = None,
        ) -> None: ...
    @classmethod
    def FromString(cls, s: bytes) -> FeatureSet: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    if sys.version_info >= (3,):
        def HasField(self, field_name: typing_extensions___Literal[u"meta",u"spec"]) -> bool: ...
        def ClearField(self, field_name: typing_extensions___Literal[u"meta",u"spec"]) -> None: ...
    else:
        def HasField(self, field_name: typing_extensions___Literal[u"meta",b"meta",u"spec",b"spec"]) -> bool: ...
        def ClearField(self, field_name: typing_extensions___Literal[u"meta",b"meta",u"spec",b"spec"]) -> None: ...

class FeatureSetSpec(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    project = ... # type: typing___Text
    name = ... # type: typing___Text
    version = ... # type: int

    @property
    def entities(self) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[EntitySpec]: ...

    @property
    def features(self) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[FeatureSpec]: ...

    @property
    def max_age(self) -> google___protobuf___duration_pb2___Duration: ...

    @property
    def source(self) -> feast___core___Source_pb2___Source: ...

    def __init__(self,
        *,
        project : typing___Optional[typing___Text] = None,
        name : typing___Optional[typing___Text] = None,
        version : typing___Optional[int] = None,
        entities : typing___Optional[typing___Iterable[EntitySpec]] = None,
        features : typing___Optional[typing___Iterable[FeatureSpec]] = None,
        max_age : typing___Optional[google___protobuf___duration_pb2___Duration] = None,
        source : typing___Optional[feast___core___Source_pb2___Source] = None,
        ) -> None: ...
    @classmethod
    def FromString(cls, s: bytes) -> FeatureSetSpec: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    if sys.version_info >= (3,):
        def HasField(self, field_name: typing_extensions___Literal[u"max_age",u"source"]) -> bool: ...
        def ClearField(self, field_name: typing_extensions___Literal[u"entities",u"features",u"max_age",u"name",u"project",u"source",u"version"]) -> None: ...
    else:
        def HasField(self, field_name: typing_extensions___Literal[u"max_age",b"max_age",u"source",b"source"]) -> bool: ...
        def ClearField(self, field_name: typing_extensions___Literal[u"entities",b"entities",u"features",b"features",u"max_age",b"max_age",u"name",b"name",u"project",b"project",u"source",b"source",u"version",b"version"]) -> None: ...

class EntitySpec(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    name = ... # type: typing___Text
    value_type = ... # type: feast___types___Value_pb2___ValueType.Enum

    def __init__(self,
        *,
        name : typing___Optional[typing___Text] = None,
        value_type : typing___Optional[feast___types___Value_pb2___ValueType.Enum] = None,
        ) -> None: ...
    @classmethod
    def FromString(cls, s: bytes) -> EntitySpec: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    if sys.version_info >= (3,):
        def ClearField(self, field_name: typing_extensions___Literal[u"name",u"value_type"]) -> None: ...
    else:
        def ClearField(self, field_name: typing_extensions___Literal[u"name",b"name",u"value_type",b"value_type"]) -> None: ...

class FeatureSpec(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    name = ... # type: typing___Text
    value_type = ... # type: feast___types___Value_pb2___ValueType.Enum

    def __init__(self,
        *,
        name : typing___Optional[typing___Text] = None,
        value_type : typing___Optional[feast___types___Value_pb2___ValueType.Enum] = None,
        ) -> None: ...
    @classmethod
    def FromString(cls, s: bytes) -> FeatureSpec: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    if sys.version_info >= (3,):
        def ClearField(self, field_name: typing_extensions___Literal[u"name",u"value_type"]) -> None: ...
    else:
        def ClearField(self, field_name: typing_extensions___Literal[u"name",b"name",u"value_type",b"value_type"]) -> None: ...

class FeatureSetMeta(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    status = ... # type: FeatureSetStatus

    @property
    def created_timestamp(self) -> google___protobuf___timestamp_pb2___Timestamp: ...

    def __init__(self,
        *,
        created_timestamp : typing___Optional[google___protobuf___timestamp_pb2___Timestamp] = None,
        status : typing___Optional[FeatureSetStatus] = None,
        ) -> None: ...
    @classmethod
    def FromString(cls, s: bytes) -> FeatureSetMeta: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    if sys.version_info >= (3,):
        def HasField(self, field_name: typing_extensions___Literal[u"created_timestamp"]) -> bool: ...
        def ClearField(self, field_name: typing_extensions___Literal[u"created_timestamp",u"status"]) -> None: ...
    else:
        def HasField(self, field_name: typing_extensions___Literal[u"created_timestamp",b"created_timestamp"]) -> bool: ...
        def ClearField(self, field_name: typing_extensions___Literal[u"created_timestamp",b"created_timestamp",u"status",b"status"]) -> None: ...

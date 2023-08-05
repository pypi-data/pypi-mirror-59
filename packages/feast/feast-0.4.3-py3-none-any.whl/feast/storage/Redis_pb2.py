# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: feast/storage/Redis.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from feast.types import Field_pb2 as feast_dot_types_dot_Field__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='feast/storage/Redis.proto',
  package='feast.storage',
  syntax='proto3',
  serialized_options=_b('\n\rfeast.storageB\nRedisProtoZ2github.com/gojek/feast/sdk/go/protos/feast/storage'),
  serialized_pb=_b('\n\x19\x66\x65\x61st/storage/Redis.proto\x12\rfeast.storage\x1a\x17\x66\x65\x61st/types/Field.proto\"E\n\x08RedisKey\x12\x13\n\x0b\x66\x65\x61ture_set\x18\x02 \x01(\t\x12$\n\x08\x65ntities\x18\x03 \x03(\x0b\x32\x12.feast.types.FieldBO\n\rfeast.storageB\nRedisProtoZ2github.com/gojek/feast/sdk/go/protos/feast/storageb\x06proto3')
  ,
  dependencies=[feast_dot_types_dot_Field__pb2.DESCRIPTOR,])




_REDISKEY = _descriptor.Descriptor(
  name='RedisKey',
  full_name='feast.storage.RedisKey',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='feature_set', full_name='feast.storage.RedisKey.feature_set', index=0,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='entities', full_name='feast.storage.RedisKey.entities', index=1,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=69,
  serialized_end=138,
)

_REDISKEY.fields_by_name['entities'].message_type = feast_dot_types_dot_Field__pb2._FIELD
DESCRIPTOR.message_types_by_name['RedisKey'] = _REDISKEY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

RedisKey = _reflection.GeneratedProtocolMessageType('RedisKey', (_message.Message,), {
  'DESCRIPTOR' : _REDISKEY,
  '__module__' : 'feast.storage.Redis_pb2'
  # @@protoc_insertion_point(class_scope:feast.storage.RedisKey)
  })
_sym_db.RegisterMessage(RedisKey)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)

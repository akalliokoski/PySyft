# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: proto/lib/python/range.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from syft.proto.core.common import recursive_serde_pb2 as proto_dot_core_dot_common_dot_recursive__serde__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='proto/lib/python/range.proto',
  package='syft.lib.python',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x1cproto/lib/python/range.proto\x12\x0fsyft.lib.python\x1a\'proto/core/common/recursive_serde.proto\"`\n\x05Range\x12\r\n\x05start\x18\x01 \x01(\x03\x12\x0c\n\x04stop\x18\x02 \x01(\x03\x12\x0c\n\x04step\x18\x03 \x01(\x03\x12,\n\x02id\x18\x04 \x01(\x0b\x32 .syft.core.common.RecursiveSerdeb\x06proto3'
  ,
  dependencies=[proto_dot_core_dot_common_dot_recursive__serde__pb2.DESCRIPTOR,])




_RANGE = _descriptor.Descriptor(
  name='Range',
  full_name='syft.lib.python.Range',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='start', full_name='syft.lib.python.Range.start', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='stop', full_name='syft.lib.python.Range.stop', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='step', full_name='syft.lib.python.Range.step', index=2,
      number=3, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='id', full_name='syft.lib.python.Range.id', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=90,
  serialized_end=186,
)

_RANGE.fields_by_name['id'].message_type = proto_dot_core_dot_common_dot_recursive__serde__pb2._RECURSIVESERDE
DESCRIPTOR.message_types_by_name['Range'] = _RANGE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Range = _reflection.GeneratedProtocolMessageType('Range', (_message.Message,), {
  'DESCRIPTOR' : _RANGE,
  '__module__' : 'proto.lib.python.range_pb2'
  # @@protoc_insertion_point(class_scope:syft.lib.python.Range)
  })
_sym_db.RegisterMessage(Range)


# @@protoc_insertion_point(module_scope)

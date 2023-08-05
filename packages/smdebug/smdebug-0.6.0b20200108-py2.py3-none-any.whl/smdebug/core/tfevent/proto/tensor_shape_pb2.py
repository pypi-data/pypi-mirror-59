# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: smdebug/core/tfevent/proto/tensor_shape.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='smdebug/core/tfevent/proto/tensor_shape.proto',
  package='smdebug',
  syntax='proto3',
  serialized_options=_b('\n\030org.tensorflow.frameworkB\021TensorShapeProtosP\001\370\001\001'),
  serialized_pb=_b('\n-smdebug/core/tfevent/proto/tensor_shape.proto\x12\x07smdebug\"w\n\x10TensorShapeProto\x12*\n\x03\x64im\x18\x02 \x03(\x0b\x32\x1d.smdebug.TensorShapeProto.Dim\x12\x14\n\x0cunknown_rank\x18\x03 \x01(\x08\x1a!\n\x03\x44im\x12\x0c\n\x04size\x18\x01 \x01(\x03\x12\x0c\n\x04name\x18\x02 \x01(\tB2\n\x18org.tensorflow.frameworkB\x11TensorShapeProtosP\x01\xf8\x01\x01\x62\x06proto3')
)




_TENSORSHAPEPROTO_DIM = _descriptor.Descriptor(
  name='Dim',
  full_name='smdebug.TensorShapeProto.Dim',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='size', full_name='smdebug.TensorShapeProto.Dim.size', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name', full_name='smdebug.TensorShapeProto.Dim.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
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
  serialized_start=144,
  serialized_end=177,
)

_TENSORSHAPEPROTO = _descriptor.Descriptor(
  name='TensorShapeProto',
  full_name='smdebug.TensorShapeProto',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='dim', full_name='smdebug.TensorShapeProto.dim', index=0,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='unknown_rank', full_name='smdebug.TensorShapeProto.unknown_rank', index=1,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_TENSORSHAPEPROTO_DIM, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=58,
  serialized_end=177,
)

_TENSORSHAPEPROTO_DIM.containing_type = _TENSORSHAPEPROTO
_TENSORSHAPEPROTO.fields_by_name['dim'].message_type = _TENSORSHAPEPROTO_DIM
DESCRIPTOR.message_types_by_name['TensorShapeProto'] = _TENSORSHAPEPROTO
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

TensorShapeProto = _reflection.GeneratedProtocolMessageType('TensorShapeProto', (_message.Message,), dict(

  Dim = _reflection.GeneratedProtocolMessageType('Dim', (_message.Message,), dict(
    DESCRIPTOR = _TENSORSHAPEPROTO_DIM,
    __module__ = 'smdebug.core.tfevent.proto.tensor_shape_pb2'
    # @@protoc_insertion_point(class_scope:smdebug.TensorShapeProto.Dim)
    ))
  ,
  DESCRIPTOR = _TENSORSHAPEPROTO,
  __module__ = 'smdebug.core.tfevent.proto.tensor_shape_pb2'
  # @@protoc_insertion_point(class_scope:smdebug.TensorShapeProto)
  ))
_sym_db.RegisterMessage(TensorShapeProto)
_sym_db.RegisterMessage(TensorShapeProto.Dim)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)

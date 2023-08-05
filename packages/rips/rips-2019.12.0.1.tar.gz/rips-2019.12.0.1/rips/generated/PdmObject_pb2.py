# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: PdmObject.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import Definitions_pb2 as Definitions__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='PdmObject.proto',
  package='rips',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x0fPdmObject.proto\x12\x04rips\x1a\x11\x44\x65\x66initions.proto\"T\n\x1aPdmDescendantObjectRequest\x12\x1f\n\x06object\x18\x01 \x01(\x0b\x32\x0f.rips.PdmObject\x12\x15\n\rchild_keyword\x18\x02 \x01(\t\"M\n\x15PdmChildObjectRequest\x12\x1f\n\x06object\x18\x01 \x01(\x0b\x32\x0f.rips.PdmObject\x12\x13\n\x0b\x63hild_field\x18\x02 \x01(\t\"h\n\x1b\x43reatePdmChildObjectRequest\x12\x1f\n\x06object\x18\x01 \x01(\x0b\x32\x0f.rips.PdmObject\x12\x13\n\x0b\x63hild_field\x18\x02 \x01(\t\x12\x13\n\x0b\x63hild_class\x18\x03 \x01(\t\"Q\n\x16PdmParentObjectRequest\x12\x1f\n\x06object\x18\x01 \x01(\x0b\x32\x0f.rips.PdmObject\x12\x16\n\x0eparent_keyword\x18\x02 \x01(\t\"\x9b\x01\n\tPdmObject\x12\x15\n\rclass_keyword\x18\x01 \x01(\t\x12\x0f\n\x07\x61\x64\x64ress\x18\x02 \x01(\x04\x12\x33\n\nparameters\x18\x03 \x03(\x0b\x32\x1f.rips.PdmObject.ParametersEntry\x1a\x31\n\x0fParametersEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"2\n\x0ePdmObjectArray\x12 \n\x07objects\x18\x01 \x03(\x0b\x32\x0f.rips.PdmObject2\x84\x03\n\x10PdmObjectService\x12S\n\x17GetDescendantPdmObjects\x12 .rips.PdmDescendantObjectRequest\x1a\x14.rips.PdmObjectArray\"\x00\x12I\n\x12GetChildPdmObjects\x12\x1b.rips.PdmChildObjectRequest\x1a\x14.rips.PdmObjectArray\"\x00\x12G\n\x14GetAncestorPdmObject\x12\x1c.rips.PdmParentObjectRequest\x1a\x0f.rips.PdmObject\"\x00\x12L\n\x14\x43reateChildPdmObject\x12!.rips.CreatePdmChildObjectRequest\x1a\x0f.rips.PdmObject\"\x00\x12\x39\n\x17UpdateExistingPdmObject\x12\x0f.rips.PdmObject\x1a\x0b.rips.Empty\"\x00\x62\x06proto3')
  ,
  dependencies=[Definitions__pb2.DESCRIPTOR,])




_PDMDESCENDANTOBJECTREQUEST = _descriptor.Descriptor(
  name='PdmDescendantObjectRequest',
  full_name='rips.PdmDescendantObjectRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='object', full_name='rips.PdmDescendantObjectRequest.object', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='child_keyword', full_name='rips.PdmDescendantObjectRequest.child_keyword', index=1,
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
  serialized_start=44,
  serialized_end=128,
)


_PDMCHILDOBJECTREQUEST = _descriptor.Descriptor(
  name='PdmChildObjectRequest',
  full_name='rips.PdmChildObjectRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='object', full_name='rips.PdmChildObjectRequest.object', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='child_field', full_name='rips.PdmChildObjectRequest.child_field', index=1,
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
  serialized_start=130,
  serialized_end=207,
)


_CREATEPDMCHILDOBJECTREQUEST = _descriptor.Descriptor(
  name='CreatePdmChildObjectRequest',
  full_name='rips.CreatePdmChildObjectRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='object', full_name='rips.CreatePdmChildObjectRequest.object', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='child_field', full_name='rips.CreatePdmChildObjectRequest.child_field', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='child_class', full_name='rips.CreatePdmChildObjectRequest.child_class', index=2,
      number=3, type=9, cpp_type=9, label=1,
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
  serialized_start=209,
  serialized_end=313,
)


_PDMPARENTOBJECTREQUEST = _descriptor.Descriptor(
  name='PdmParentObjectRequest',
  full_name='rips.PdmParentObjectRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='object', full_name='rips.PdmParentObjectRequest.object', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='parent_keyword', full_name='rips.PdmParentObjectRequest.parent_keyword', index=1,
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
  serialized_start=315,
  serialized_end=396,
)


_PDMOBJECT_PARAMETERSENTRY = _descriptor.Descriptor(
  name='ParametersEntry',
  full_name='rips.PdmObject.ParametersEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='rips.PdmObject.ParametersEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='rips.PdmObject.ParametersEntry.value', index=1,
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
  serialized_options=_b('8\001'),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=505,
  serialized_end=554,
)

_PDMOBJECT = _descriptor.Descriptor(
  name='PdmObject',
  full_name='rips.PdmObject',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='class_keyword', full_name='rips.PdmObject.class_keyword', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='address', full_name='rips.PdmObject.address', index=1,
      number=2, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='parameters', full_name='rips.PdmObject.parameters', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_PDMOBJECT_PARAMETERSENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=399,
  serialized_end=554,
)


_PDMOBJECTARRAY = _descriptor.Descriptor(
  name='PdmObjectArray',
  full_name='rips.PdmObjectArray',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='objects', full_name='rips.PdmObjectArray.objects', index=0,
      number=1, type=11, cpp_type=10, label=3,
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
  serialized_start=556,
  serialized_end=606,
)

_PDMDESCENDANTOBJECTREQUEST.fields_by_name['object'].message_type = _PDMOBJECT
_PDMCHILDOBJECTREQUEST.fields_by_name['object'].message_type = _PDMOBJECT
_CREATEPDMCHILDOBJECTREQUEST.fields_by_name['object'].message_type = _PDMOBJECT
_PDMPARENTOBJECTREQUEST.fields_by_name['object'].message_type = _PDMOBJECT
_PDMOBJECT_PARAMETERSENTRY.containing_type = _PDMOBJECT
_PDMOBJECT.fields_by_name['parameters'].message_type = _PDMOBJECT_PARAMETERSENTRY
_PDMOBJECTARRAY.fields_by_name['objects'].message_type = _PDMOBJECT
DESCRIPTOR.message_types_by_name['PdmDescendantObjectRequest'] = _PDMDESCENDANTOBJECTREQUEST
DESCRIPTOR.message_types_by_name['PdmChildObjectRequest'] = _PDMCHILDOBJECTREQUEST
DESCRIPTOR.message_types_by_name['CreatePdmChildObjectRequest'] = _CREATEPDMCHILDOBJECTREQUEST
DESCRIPTOR.message_types_by_name['PdmParentObjectRequest'] = _PDMPARENTOBJECTREQUEST
DESCRIPTOR.message_types_by_name['PdmObject'] = _PDMOBJECT
DESCRIPTOR.message_types_by_name['PdmObjectArray'] = _PDMOBJECTARRAY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

PdmDescendantObjectRequest = _reflection.GeneratedProtocolMessageType('PdmDescendantObjectRequest', (_message.Message,), dict(
  DESCRIPTOR = _PDMDESCENDANTOBJECTREQUEST,
  __module__ = 'PdmObject_pb2'
  # @@protoc_insertion_point(class_scope:rips.PdmDescendantObjectRequest)
  ))
_sym_db.RegisterMessage(PdmDescendantObjectRequest)

PdmChildObjectRequest = _reflection.GeneratedProtocolMessageType('PdmChildObjectRequest', (_message.Message,), dict(
  DESCRIPTOR = _PDMCHILDOBJECTREQUEST,
  __module__ = 'PdmObject_pb2'
  # @@protoc_insertion_point(class_scope:rips.PdmChildObjectRequest)
  ))
_sym_db.RegisterMessage(PdmChildObjectRequest)

CreatePdmChildObjectRequest = _reflection.GeneratedProtocolMessageType('CreatePdmChildObjectRequest', (_message.Message,), dict(
  DESCRIPTOR = _CREATEPDMCHILDOBJECTREQUEST,
  __module__ = 'PdmObject_pb2'
  # @@protoc_insertion_point(class_scope:rips.CreatePdmChildObjectRequest)
  ))
_sym_db.RegisterMessage(CreatePdmChildObjectRequest)

PdmParentObjectRequest = _reflection.GeneratedProtocolMessageType('PdmParentObjectRequest', (_message.Message,), dict(
  DESCRIPTOR = _PDMPARENTOBJECTREQUEST,
  __module__ = 'PdmObject_pb2'
  # @@protoc_insertion_point(class_scope:rips.PdmParentObjectRequest)
  ))
_sym_db.RegisterMessage(PdmParentObjectRequest)

PdmObject = _reflection.GeneratedProtocolMessageType('PdmObject', (_message.Message,), dict(

  ParametersEntry = _reflection.GeneratedProtocolMessageType('ParametersEntry', (_message.Message,), dict(
    DESCRIPTOR = _PDMOBJECT_PARAMETERSENTRY,
    __module__ = 'PdmObject_pb2'
    # @@protoc_insertion_point(class_scope:rips.PdmObject.ParametersEntry)
    ))
  ,
  DESCRIPTOR = _PDMOBJECT,
  __module__ = 'PdmObject_pb2'
  # @@protoc_insertion_point(class_scope:rips.PdmObject)
  ))
_sym_db.RegisterMessage(PdmObject)
_sym_db.RegisterMessage(PdmObject.ParametersEntry)

PdmObjectArray = _reflection.GeneratedProtocolMessageType('PdmObjectArray', (_message.Message,), dict(
  DESCRIPTOR = _PDMOBJECTARRAY,
  __module__ = 'PdmObject_pb2'
  # @@protoc_insertion_point(class_scope:rips.PdmObjectArray)
  ))
_sym_db.RegisterMessage(PdmObjectArray)


_PDMOBJECT_PARAMETERSENTRY._options = None

_PDMOBJECTSERVICE = _descriptor.ServiceDescriptor(
  name='PdmObjectService',
  full_name='rips.PdmObjectService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=609,
  serialized_end=997,
  methods=[
  _descriptor.MethodDescriptor(
    name='GetDescendantPdmObjects',
    full_name='rips.PdmObjectService.GetDescendantPdmObjects',
    index=0,
    containing_service=None,
    input_type=_PDMDESCENDANTOBJECTREQUEST,
    output_type=_PDMOBJECTARRAY,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='GetChildPdmObjects',
    full_name='rips.PdmObjectService.GetChildPdmObjects',
    index=1,
    containing_service=None,
    input_type=_PDMCHILDOBJECTREQUEST,
    output_type=_PDMOBJECTARRAY,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='GetAncestorPdmObject',
    full_name='rips.PdmObjectService.GetAncestorPdmObject',
    index=2,
    containing_service=None,
    input_type=_PDMPARENTOBJECTREQUEST,
    output_type=_PDMOBJECT,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='CreateChildPdmObject',
    full_name='rips.PdmObjectService.CreateChildPdmObject',
    index=3,
    containing_service=None,
    input_type=_CREATEPDMCHILDOBJECTREQUEST,
    output_type=_PDMOBJECT,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='UpdateExistingPdmObject',
    full_name='rips.PdmObjectService.UpdateExistingPdmObject',
    index=4,
    containing_service=None,
    input_type=_PDMOBJECT,
    output_type=Definitions__pb2._EMPTY,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_PDMOBJECTSERVICE)

DESCRIPTOR.services_by_name['PdmObjectService'] = _PDMOBJECTSERVICE

# @@protoc_insertion_point(module_scope)

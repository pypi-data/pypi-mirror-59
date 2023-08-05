# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from . import common_pb2 as common__pb2
from . import operationLogService_pb2 as operationLogService__pb2


class OperationLogServiceStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.Log = channel.unary_unary(
        '/longleding.log.OperationLogService/Log',
        request_serializer=operationLogService__pb2.OperationLogMessage.SerializeToString,
        response_deserializer=common__pb2.ResponseMessage.FromString,
        )
    self.GetOperationLogs = channel.unary_unary(
        '/longleding.log.OperationLogService/GetOperationLogs',
        request_serializer=operationLogService__pb2.GetOperationLogsRequest.SerializeToString,
        response_deserializer=common__pb2.ResponseMessage.FromString,
        )


class OperationLogServiceServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def Log(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetOperationLogs(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_OperationLogServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'Log': grpc.unary_unary_rpc_method_handler(
          servicer.Log,
          request_deserializer=operationLogService__pb2.OperationLogMessage.FromString,
          response_serializer=common__pb2.ResponseMessage.SerializeToString,
      ),
      'GetOperationLogs': grpc.unary_unary_rpc_method_handler(
          servicer.GetOperationLogs,
          request_deserializer=operationLogService__pb2.GetOperationLogsRequest.FromString,
          response_serializer=common__pb2.ResponseMessage.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'longleding.log.OperationLogService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))

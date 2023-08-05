import grpc
import dict_to_protobuf
from mesh_rpc.mesh import MeshRPC
from mesh_rpc.exp import MeshRPCException

from .lib.gtfs_realtime_pb2 import FeedMessage
from .defaults import Default

class MeshGTFSR(MeshRPC):
    def __init__(self, endpoint='127.0.0.1:5555'):
        super().__init__(endpoint)

    def subscribe(self, geospace):

        s = super().subscribe(Default.topic, geospace)

        feed = FeedMessage()

        channelLen = len(Default.topic)

        try:
            for msg in s:
                try:
                    feed.ParseFromString(msg.raw)
                except Exception as e:
                    continue
                yield feed, msg.topic.pop()[channelLen:]
        except grpc.RpcError as e:
            raise MeshRPCException(e.details())
    
    def unsubscribe(self, geospace):

        s = super().unsubscribe(Default.topic, geospace)

        return s
        
    def registerToPublish(self, geospace):
        try:
            super().registerToPublish(Default.topic, geospace)
        except MeshRPCException as e:
            raise 
    
    def unregisterToPublish(self, geospace):
        try:
            super().unregisterToPublish(Default.topic, geospace)
        except MeshRPCException as e:
            raise

    def publish(self, geospace, d):

        if isinstance(d, dict):
            d["header"]["gtfs_realtime_version"] = "2.0"
            feed = FeedMessage()
            dict_to_protobuf.dict_to_protobuf(d, feed)
            raw = feed.SerializeToString()
        else:
            raw = d

        try:
            res = super().publish(Default.topic, geospace, raw)
        except MeshRPCException as e:
            raise 
    
    def get_channel(self):
        return Default.topic
    

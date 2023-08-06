import threading
import time
from time import sleep
from typing import Iterable, List, Tuple, Union
from uuid import uuid4

import grpc
from google.protobuf.internal.wire_format import INT32_MAX, INT64_MAX
from grpc import StatusCode
from grpc._channel import _InactiveRpcError

from axonclient.common_pb2 import SerializedObject
from axonclient.event_pb2 import (
    Event,
    GetAggregateEventsRequest,
    GetAggregateSnapshotsRequest,
    GetEventsRequest,
    GetFirstTokenRequest,
    GetLastTokenRequest,
)
from axonclient.event_pb2_grpc import EventStoreStub
from axonclient.exceptions import OutOfRangeError

DEFAULT_LOCAL_AXONSERVER_URI = "localhost:8124"


class AxonEvent(object):
    def __init__(
        self,
        aggregate_identifier: str,
        aggregate_sequence_number: int,
        aggregate_type: str,
        message_identifier: str = "",
        timestamp: int = 0,
        payload_type: str = "",
        payload_revision: str = "",
        payload_data: bytes = b"",
        snapshot: bool = False,
        meta_data=None,  # Todo: Improve definition (MetaDataValue)
    ):
        if meta_data is None:
            meta_data = {}
        if message_identifier is None:
            message_identifier = str(uuid4())
        assert aggregate_type, "Non-empty string required (otherwise can't get events)"
        self.message_identifier = message_identifier
        self.aggregate_identifier = aggregate_identifier
        self.aggregate_sequence_number = aggregate_sequence_number
        self.aggregate_type = aggregate_type
        self.timestamp = timestamp or self.create_timestamp()
        self.payload_type = payload_type
        self.payload_revision = payload_revision
        self.payload_data = payload_data
        self.snapshot = snapshot
        self.meta_data = meta_data

    def to_grpc(self):
        return Event(
            message_identifier=self.message_identifier,
            aggregate_identifier=self.aggregate_identifier,
            aggregate_sequence_number=self.aggregate_sequence_number,
            aggregate_type=self.aggregate_type,
            timestamp=self.timestamp,
            payload=SerializedObject(
                type=self.payload_type,
                revision=self.payload_revision,
                data=self.payload_data,
            ),
            snapshot=self.snapshot,
            meta_data=self.meta_data,
        )

    @classmethod
    def from_grpc(cls, event: Event):
        return cls(
            message_identifier=event.message_identifier,
            aggregate_identifier=event.aggregate_identifier,
            aggregate_sequence_number=event.aggregate_sequence_number,
            aggregate_type=event.aggregate_type,
            timestamp=event.timestamp,
            payload_type=event.payload.type,
            payload_revision=event.payload.revision,
            payload_data=event.payload.data,
            snapshot=event.snapshot,
            meta_data=event.meta_data,
        )

    @classmethod
    def create_timestamp(cls):
        return round(time.time() * 1000)


class AxonClient:
    def __init__(self, uri):
        self.uri = uri
        self.channel = grpc.insecure_channel(self.uri)
        self.event_store_stub = EventStoreStub(self.channel)

    def list_aggregate_events(
        self, aggregate_id: str, initial_sequence: int, allow_snapshots: bool
    ):
        return list(
            self.iter_aggregate_events(aggregate_id, initial_sequence, allow_snapshots)
        )

    def iter_aggregate_events(
        self, aggregate_id: str, initial_sequence: int, allow_snapshots: bool
    ):
        assert isinstance(aggregate_id, str)
        request = GetAggregateEventsRequest(
            aggregate_id=aggregate_id,
            initial_sequence=initial_sequence,
            allow_snapshots=allow_snapshots,
        )
        response = self.event_store_stub.ListAggregateEvents(request)
        for event in response:
            yield AxonEvent.from_grpc(event)

    def append_event(self, events: Union[AxonEvent, Iterable[AxonEvent]]):
        if isinstance(events, AxonEvent):
            events = [events]
        events = [event.to_grpc() for event in events]
        try:
            confirmation = self.event_store_stub.AppendEvent(iter(events))
        except _InactiveRpcError as e:
            if e.code() == StatusCode.OUT_OF_RANGE:
                raise OutOfRangeError(e.debug_error_string())
            else:
                raise e

        assert confirmation.success, "Operation failed"

    def list_snapshot_events(
        self,
        aggregate_id: str,
        initial_sequence=0,
        max_sequence=INT64_MAX,
        max_results=INT32_MAX,
    ):
        """
        Returns list of snapshots of aggregate_id, in reverse order.
        """
        return list(
            self.iter_snapshot_events(
                aggregate_id, initial_sequence, max_sequence, max_results
            )
        )

    def iter_snapshot_events(
        self,
        aggregate_id: str,
        initial_sequence=0,
        max_sequence=INT64_MAX,
        max_results=INT32_MAX,
    ):
        """
        Returns iterator of snapshots of aggregate_id, in reverse order.
        """
        assert isinstance(aggregate_id, str)
        request = GetAggregateSnapshotsRequest(
            aggregate_id=aggregate_id,
            initial_sequence=initial_sequence,
            max_sequence=max_sequence,
            max_results=max_results,
        )
        response = self.event_store_stub.ListAggregateSnapshots(request)
        for event in response:
            yield AxonEvent.from_grpc(event)

    def append_snapshot(self, event: AxonEvent):
        confirmation = self.event_store_stub.AppendSnapshot(event.to_grpc())
        assert confirmation.success, "Operation failed"

    def close_connection(self):
        self.channel.close()

    def list_events(
        self,
        tracking_token: int = 0,
        number_of_permits: int = INT32_MAX,
        client_id: str = "",
        component_name: str = "",
        processor: str = "",
        blacklist: Iterable = (),
    ) -> List[Tuple[str, AxonEvent]]:

        return list(
            self.iter_events(
                tracking_token,
                number_of_permits,
                client_id,
                component_name,
                processor,
                blacklist,
            )
        )

    def iter_events(
        self,
        tracking_token: int = 0,
        number_of_permits: int = INT32_MAX,
        client_id: str = "",
        component_name: str = "",
        processor: str = "",
        blacklist: Iterable = (),
    ) -> Iterable[Tuple[str, AxonEvent]]:

        request = GetEventsRequest(
            tracking_token=tracking_token,
            number_of_permits=number_of_permits,
            client_id=client_id,
            component_name=component_name,
            processor=processor,
            blacklist=blacklist,
        )

        # This doesn't work...
        # response = self.event_store_stub.ListEvents(iter([request]))

        # But this does. :-)
        stop_event = threading.Event()
        def request_iterator():
            yield request
            sleep(0.1)
            stop_event.wait(timeout=5)

        response = self.event_store_stub.ListEvents(request_iterator())

        stop_event.set()

        for event_with_token in response:
            yield event_with_token.token, AxonEvent.from_grpc(event_with_token.event)

    def get_last_token(self):
        last_token = self.event_store_stub.GetLastToken(GetLastTokenRequest())
        return last_token.token

    def get_first_token(self):
        first_token = self.event_store_stub.GetFirstToken(GetFirstTokenRequest())
        return first_token.token

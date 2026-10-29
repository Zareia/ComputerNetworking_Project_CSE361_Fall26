"""RJDAP wire format: header layout, message types, encode/decode helpers.

Required header fields: Task_ID, Worker_ID, Attempt_Num, Payload_Checksum.
The final bit layout must be documented in docs/rfc (Message Formats section).
"""

from enum import IntEnum

PROTOCOL_ID = 0x524A  # "RJ"
VERSION = 1
MAX_PAYLOAD = 512  # bytes, per project constraint


class MsgType(IntEnum):
    WORKER_JOIN = 0
    HEARTBEAT = 1
    TASK_DISPATCH = 2
    TASK_RESULT = 3
    ACK_RESULT = 4


# TODO: choose the header layout and struct format string, e.g. "!HBBIHHI"
HEADER_FORMAT = None


def encode(msg_type, task_id, worker_id, attempt, payload=b""):
    """Build a packet: header + payload. TODO."""
    raise NotImplementedError


def decode(data):
    """Parse a packet and verify the checksum. TODO."""
    raise NotImplementedError

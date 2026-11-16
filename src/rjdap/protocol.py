from enum import IntEnum
import struct
import zlib

PROTOCOL_ID = 0x524A  # "RJ"
VERSION = 1
MAX_PAYLOAD = 512  # bytes, per project constraint


class MsgType(IntEnum):
    WORKER_JOIN = 0
    JOIN_ACK = 1
    HEARTBEAT = 2
    TASK_DISPATCH = 3
    TASK_RESULT = 4
    ACK_RESULT = 5


HEADER_FORMAT = "!BBIHHHI"
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)


def encode_message(msg_type, worker_id, task_id=0, attempt_num=0, payload=b""):

    if isinstance(payload, str):
        payload = payload.encode("utf-8")
    if len(payload) > MAX_PAYLOAD:
        raise ValueError("Payload exceeds 512 bytes")



    checksum = zlib.crc32(payload)

    header = struct.pack(
        HEADER_FORMAT,
        VERSION,
        msg_type,
        task_id,
        worker_id,
        attempt_num,
        len(payload),
        checksum
    )

    return header + payload


def decode_message(data):

    if len(data) < HEADER_SIZE:
        raise ValueError("Packet is smaller than the header")

    version,msg_type,task_id,worker_id,attempt,payload_length,checksum = struct.unpack(HEADER_FORMAT,data[:HEADER_SIZE])

    payload = data[HEADER_SIZE:]

    if version != VERSION:
        raise ValueError("Unsupported protocol version")
    if payload_length > MAX_PAYLOAD:
        raise ValueError("Payload exceeds 512 bytes")
    if payload_length != len(payload):
        raise ValueError("Invalid payload length")
    if checksum != (zlib.crc32(payload)):
        raise ValueError("Checksum Mismatch")

    return {
        "version" : version,
        "message_type" : msg_type,
        "task_id" : task_id,
        "worker_id" : worker_id,
        "attempt_number" : attempt,
        "payload" : payload
    }

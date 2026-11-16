
import socket
import sys

from protocol import *


# Server configuration
SERVER_IP = "127.0.0.1"
SERVER_PORT = 5000


# Read worker ID
if len(sys.argv) != 2:
    print("Usage: python worker.py <worker_id>")
    sys.exit(1)

worker_id = int(sys.argv[1])

if not 1 <= worker_id <= 65535:
    print("Worker ID must be between 1 and 65535")
    sys.exit(1)


# Create UDP socket
worker_socket = socket.socket(
    socket.AF_INET,
    socket.SOCK_DGRAM
)

worker_socket.settimeout(5)

server_address = (SERVER_IP, SERVER_PORT)


try:

    # ---------------------------------
    # 1. Register with the server
    # ---------------------------------

    join_message = encode_message(
        msg_type=MsgType.WORKER_JOIN,
        worker_id=worker_id
    )

    worker_socket.sendto(join_message, server_address)

    print(f"Worker {worker_id}: WORKER_JOIN sent")


    # ---------------------------------
    # 2. Receive JOIN_ACK
    # ---------------------------------

    data, address = worker_socket.recvfrom(1024)

    if address != server_address:
        raise ValueError("Response received from unexpected address")

    response = decode_message(data)

    if (
        response["message_type"] != MsgType.JOIN_ACK
        or response["worker_id"] != worker_id
    ):
        raise ValueError("Expected JOIN_ACK")

    print("JOIN_ACK received. Registration successful!")


    # ---------------------------------
    # 3. Receive TASK_DISPATCH
    # ---------------------------------

    data, address = worker_socket.recvfrom(1024)

    if address != server_address:
        raise ValueError("Task received from unexpected address")

    task = decode_message(data)

    if (
        task["message_type"] != MsgType.TASK_DISPATCH
        or task["worker_id"] != worker_id
    ):
        raise ValueError("Expected TASK_DISPATCH for this worker")

    task_id = task["task_id"]

    print(f"\nTASK_DISPATCH received")
    print(f"Task ID: {task_id}")


    # ---------------------------------
    # 4. Execute the task
    # ---------------------------------

    numbers = task["payload"].decode("utf-8")

    first_number, second_number = map(
        int,
        numbers.split(",")
    )

    result = first_number + second_number

    print(
        f"Worker {worker_id}: "
        f"{first_number} + {second_number} = {result}"
    )


    # ---------------------------------
    # 5. Send TASK_RESULT
    # ---------------------------------

    result_message = encode_message(
        msg_type=MsgType.TASK_RESULT,
        worker_id=worker_id,
        task_id=task_id,
        payload=str(result)
    )

    worker_socket.sendto(result_message, server_address)

    print("TASK_RESULT sent to server")


    # ---------------------------------
    # 6. Receive ACK_RESULT
    # ---------------------------------

    data, address = worker_socket.recvfrom(1024)

    if address != server_address:
        raise ValueError("ACK received from unexpected address")

    ack = decode_message(data)

    if (
        ack["message_type"] == MsgType.ACK_RESULT
        and ack["worker_id"] == worker_id
        and ack["task_id"] == task_id
    ):
        print("ACK_RESULT received")
        print("Task completed successfully!")

    else:
        raise ValueError("Invalid ACK_RESULT")


except socket.timeout:
    print("Timeout: Server did not respond within 5 seconds")

except (ValueError, UnicodeDecodeError) as error:
    print(f"Protocol error: {error}")

finally:
    worker_socket.close()

from socket import socket, AF_INET, SOCK_DGRAM
from protocol import *

# Config
SERVER_IP = "127.0.0.1"
SERVER_PORT = 5000

# registered workers list, tasks list, results list
workers = {}
tasks = {}
results = {}

server_socket = socket(AF_INET, SOCK_DGRAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
print(f"Command Server listening on {SERVER_IP}:{SERVER_PORT}")

while True:

    data, address = server_socket.recvfrom(1024)

    try:
        message = decode_message(data)

        worker_id = message["worker_id"]
        message_type = message["message_type"]
        task_id = message["task_id"]

        if message_type == MsgType.WORKER_JOIN:
            if worker_id == 0:
                print("invalid worker id")
                continue
            if worker_id in workers:
                print(f"Worker {worker_id} re-registered")
            else:
                print(f"Worker {worker_id} registered")

            workers[worker_id] = {
                "address" : address
            }

            print(f"Address: {address}")
            print(f"Total workers: {len(workers)}")
            print("-" * 30)

            # Send JOIN_ACK
            responce = encode_message(msg_type=MsgType.JOIN_ACK,worker_id=worker_id)
            server_socket.sendto(responce, address)

            task_id = 1000 + worker_id
            task_payload = "40,27"

            tasks[task_id] = {
                "worker_id" : worker_id,
                "payload" : task_payload
            }

            task_message = encode_message(
                msg_type= MsgType.TASK_DISPATCH,
                worker_id=worker_id,
                task_id=task_id,
                payload=task_payload
            )

            server_socket.sendto(task_message,address)

            print(f"TASK_DISPATCH sent to Worker {worker_id} ")
            print(f"Task ID: {task_id}")
        elif message_type == MsgType.TASK_RESULT:
            if worker_id not in workers:
                print(f"Result from unkown worker {worker_id}")
                continue
            if task_id not in tasks:
                print(f"Unkown task ID: {task_id}")
                continue
            if tasks[task_id]["worker_id"] != worker_id:
                print("Task result recieved from the wrong worker")
                continue
            if address != workers[worker_id]["address"]:
                print("Result received from an unexpected address")
                continue

            result_value = message["payload"].decode("utf-8")

            results[task_id] = result_value

            print(f"\n Result received from worker {worker_id}")
            print(f"Task ID: {task_id}")
            print(f"Result: {result_value}")


            ack_message = encode_message(
                msg_type=MsgType.ACK_RESULT,
                worker_id=worker_id,
                task_id=task_id
            )

            server_socket.sendto(ack_message, address)

            print(f"ACK_RESULT sent for Task {task_id}")
            print(f"Total completed tasks: {len(results)}")

        else:
            print("Unknown message type")
    except ValueError as error:
        print(f"Invalid Packet: {error}")

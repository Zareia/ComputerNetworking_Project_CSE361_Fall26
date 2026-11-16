
from protocol import *


# Create a message
original_payload = "Hello RJDAP!"

message = encode_message(msg_type=MsgType.WORKER_JOIN,task_id=0,worker_id=1,attempt_num=0,payload=original_payload)


print("Encoded message:", message)

# Decode the message
decoded = decode_message(message)

print("\nDecoded message:")
for key, value in decoded.items():
    print(f"{key}: {value}")

# Verify the payload
assert decoded["payload"].decode("utf-8") == original_payload

print("\nProtocol test passed!")


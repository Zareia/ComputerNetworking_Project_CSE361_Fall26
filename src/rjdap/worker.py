"""RJDAP compute node (worker client).

Responsibilities:
- Send WORKER_JOIN, then periodic HEARTBEAT
- On TASK_DISPATCH, run the compute loop (e.g. find a hash in a number range)
- Send TASK_RESULT and retransmit until ACK_RESULT arrives (bounded retries)
- Track idle vs. computing time (worker_idle_time_ms)
"""

import argparse


def compute(task_payload):
    """Simulated computation. TODO."""
    raise NotImplementedError


def main():
    parser = argparse.ArgumentParser(description="RJDAP worker")
    parser.add_argument("--server", default="127.0.0.1:9000")
    parser.add_argument("--id", type=int, required=True)
    args = parser.parse_args()
    # TODO: implement worker loop
    raise NotImplementedError


if __name__ == "__main__":
    main()

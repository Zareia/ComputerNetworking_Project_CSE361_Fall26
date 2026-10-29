"""RJDAP Command Hub (server).

Responsibilities:
- Accept WORKER_JOIN, track worker liveness via HEARTBEAT
- Keep the task queue (>= 1000 tasks) and send TASK_DISPATCH
- Reassign tasks whose worker timed out (reassigned_task_count)
- Accept TASK_RESULT exactly once, always reply ACK_RESULT,
  count retransmitted duplicates (duplicate_results_dropped)
"""

import argparse


def main():
    parser = argparse.ArgumentParser(description="RJDAP Command Hub")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=9000)
    parser.add_argument("--tasks", type=int, default=1000)
    parser.add_argument("--timeout-ms", type=int, default=200)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()
    # TODO: implement server loop
    raise NotImplementedError


if __name__ == "__main__":
    main()

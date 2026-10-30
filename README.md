# RJDAP — Reliable Job Dispatch & Aggregation Protocol

CSE361 Computer Networks, Fall 2026 — Project 2 (Distributed Fleet Defense)

RJDAP is a UDP-based protocol that distributes stateless compute tasks from a central
**Command Hub** (server) to a pool of **worker nodes** (clients), guaranteeing each task
result is counted **exactly once** even when packets are lost or delayed.

> **Status:** project skeleton. Protocol, server and worker are not implemented yet —
> the commands below describe the intended interface.

## Team

| Name | Student ID |
|------|------------|
| _name_ | _id_ |
| _name_ | _id_ |
| _name_ | _id_ |

Demo video links are in [README.txt](README.txt) (required by the LMS submission).

## Protocol summary

| Item | Value |
|------|-------|
| Transport | UDP only |
| Header fields (required) | `Task_ID`, `Worker_ID`, `Attempt_Num`, `Payload_Checksum` |
| Message types | `WORKER_JOIN`, `HEARTBEAT`, `TASK_DISPATCH`, `TASK_RESULT`, `ACK_RESULT` |
| Max payload per packet | 512 bytes |
| Worker pool | ≥ 4 clients |
| Task queue | ≥ 1,000 tasks |
| Reassignment timeout | server-defined (e.g. 200 ms) |

Full specification: [docs/rfc/mini_rfc.md](docs/rfc/mini_rfc.md)

## Repository layout

```
src/rjdap/         protocol.py (header/encode/decode), server.py, worker.py, logger.py
scripts/           run_baseline.sh, run_experiments.sh, capture_pcap.sh
scripts/netem/     apply.sh / clear.sh — add and remove tc netem impairments
experiments/       scenario configs (seeds, task counts, netem profiles)
results/           raw outputs: csv/, pcap/, logs/, plots/  (one folder per run: <timestamp>_seed<N>)
analysis/          plot_results.py — reproduces the report plots from the CSVs
tests/             unit tests (header encode/decode, duplicate suppression)
docs/              proposal, Mini-RFC, technical report, slides, diagrams
```

## Requirements

- Python 3 (protocol code uses the standard library only)
- Linux or WSL2 for the netem experiments: `iproute2` (`tc`), `tcpdump`
- Plotting: `pip install -r requirements.txt`

## Running

Run from the repository root.

**Linux / WSL2**

```bash
export PYTHONPATH=src
python3 -m rjdap.server --port 9000 --tasks 1000
python3 -m rjdap.worker --server 127.0.0.1:9000 --id 1   # repeat with --id 2, 3, 4
```

**Windows (PowerShell)**

```powershell
$env:PYTHONPATH = "src"
python -m rjdap.server --port 9000 --tasks 1000
python -m rjdap.worker --server 127.0.0.1:9000 --id 1
```

**Automated runs (Linux, needs sudo for netem/tcpdump)**

```bash
./scripts/run_baseline.sh          # baseline scenario only
sudo ./scripts/run_experiments.sh  # all scenarios, 5 repeats each (REPEATS=N to change)
```

## Test scenarios

| Scenario | Impairment | Acceptance criteria |
|----------|------------|---------------------|
| Baseline (LAN) | none | 1,000 tasks completed, zero duplicate executions |
| Worker Crash | hard-kill client 1 mid-run (`kill -9`) | server detects timeout, reassigns to clients 2/3/4, 100% complete |
| Severe Loss | `netem loss 10%` | duplicate suppression triggers, no result counted twice |
| Delayed ACKs | `netem delay 150ms` on server outbound only | workers handle late ACKs without crashing or retransmitting forever |

netem commands (`lo` = loopback; replace with your interface for multi-host runs):

```bash
# Severe Loss
sudo tc qdisc add dev lo root netem loss 10%

# Delayed ACKs — delay only packets sent FROM the server (UDP source port 9000)
sudo tc qdisc add dev lo root handle 1: prio
sudo tc qdisc add dev lo parent 1:3 handle 30: netem delay 150ms
sudo tc filter add dev lo parent 1:0 protocol ip u32 match ip sport 9000 0xffff flowid 1:3

# Remove any impairment
sudo tc qdisc del dev lo root
```

The same commands are wrapped in `scripts/netem/apply.sh <iface> loss10|delay150` and
`scripts/netem/clear.sh <iface>`.

## Metrics

| Metric | Description |
|--------|-------------|
| `total_completion_time` | wall-clock time to finish the 1,000-task queue |
| `reassigned_task_count` | tasks re-dispatched after a worker timeout |
| `duplicate_results_dropped` | retransmitted results ignored by the server |
| `worker_idle_time_ms` | time workers spend waiting vs. computing |

Each scenario is repeated ≥ 5 times (min / median / max reported), with pcap traces for
at least two runs per scenario.

## Environment used for results

OS: _fill in_ · Python: _fill in_ · Library versions: see `requirements.txt`

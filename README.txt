RJDAP - Reliable Job Dispatch & Aggregation Protocol
CSE361 Computer Networks - Fall 2026 - Project 2 (Distributed Fleet Defense)

Team members
------------
- <name> (<id>)
- <name> (<id>)
- <name> (<id>)

Demo video links (access: "anyone with the link can view")
-----------------------------------------------------------
Phase 1 demo (5 min):   <link>
Final demo  (<=10 min): <link>

Overview
--------
RJDAP is a UDP-based protocol that sends stateless compute tasks from a central
Command Hub (server) to a pool of worker nodes (clients). Each task is processed
exactly once, even when packets are lost or delayed.

Message types: WORKER_JOIN, HEARTBEAT, TASK_DISPATCH, TASK_RESULT, ACK_RESULT
Constraints:   payload <= 512 bytes, >= 4 workers, >= 1000 tasks, server-defined timeout (e.g. 200 ms)

Repository layout
-----------------
src/rjdap/        Protocol implementation (header packing, server, worker, logging)
scripts/          Run scripts (baseline, all experiments, pcap capture)
scripts/netem/    Scripts that apply/remove tc netem impairments (Linux)
experiments/      Scenario configs (seeds, task counts, netem profiles)
results/          Raw outputs: csv/, pcap/, logs/, plots/ (one folder per run: <timestamp>_seed<N>)
analysis/         Scripts that load the CSVs and reproduce the report plots
tests/            Unit tests (header encode/decode, duplicate suppression)
docs/             Proposal, Mini-RFC, technical report, slides, diagrams

Requirements
------------
- Python 3.10+ (standard library only for the protocol)
- Linux for netem tests (or WSL2 on Windows): iproute2 (tc), tcpdump
- analysis: pip install -r requirements.txt

Running locally
---------------
Server:  python -m rjdap.server --port 9000 --tasks 1000
Worker:  python -m rjdap.worker --server 127.0.0.1:9000 --id 1
(run from the src/ directory, or set PYTHONPATH=src)

Baseline test:     ./scripts/run_baseline.sh
All experiments:   ./scripts/run_experiments.sh

Test scenarios (netem)
----------------------
Baseline (LAN)   none                                 1000 tasks, zero duplicate executions
Worker Crash     hard kill client 1 during execution  tasks reassigned to 2/3/4, 100% complete
Severe Loss      sudo tc qdisc add dev lo root netem loss 10%
Delayed ACKs     sudo tc qdisc add dev lo root netem delay 150ms   (server outbound)
Remove:          sudo tc qdisc del dev lo root

Environment used for results
----------------------------
OS: <fill in>   Python: <fill in>   Library versions: see requirements.txt

# NetGen : Failure-Aware Orchestrator Agents for Analog Netlist Generation

This repository contains the benchmark results and generated outputs from the NetGen framework presented in the paper *NetGen: Failure-Aware Orchestrator Agents for Analog Netlist Generation*. It is intended for reviewing generated SPICE netlists, execution traces, and evaluation artifacts.

The benchmark task set is given in `problem_set.tsv` and contains the 30 problems used in the study. The full experimental setup reported in the paper was executed over all 30 tasks with ten attempts per task and up to three retries per attempt. For the present archival release, we provide one selected run per task under `runs/p01` through `runs/p30`.

Each archived run includes the generated netlist together with run-level metadata and execution records, including manifests, event logs, stage-wise prompts and responses, stdout/stderr logs, and evaluation artifacts.

Repository contents:

- `problem_set.tsv`: benchmark task definitions for all 30 problems.
- `runs/p*/sandbox/*.cir`: generated SPICE netlist for the archived run.
- `runs/p*/run_manifest.json` and `runs/p*/run_events.jsonl`: run-level metadata and trace records.
- `runs/p*/stages/`: stage-level prompts, responses, logs, and event files.
- `runs/p*/artifacts/`: evaluation outputs and retry-specific artifacts.

To preserve anonymity and avoid disclosure of local execution environments, machine-specific file paths and related identifiers in the released artifacts have been redacted or normalized. Placeholders such as `<REDACTED>` are therefore intentional.

This repository is intended as a concise, inspectable benchmark archive accompanying the paper.

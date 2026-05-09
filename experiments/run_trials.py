#!/usr/bin/env python3

import argparse
import csv
import subprocess
import time
from pathlib import Path


PROJECT = Path("/home/cornelius/AF-CDI-MediateLab")
PYTHON = PROJECT / "venv/bin/python"

READ_SCRIPT = PROJECT / "clients/modbus_read.py"
WRITE_SCRIPT = PROJECT / "attacks/modbus_write_attack.py"


def run_cmd(cmd):
    start = time.perf_counter()
    completed = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    end = time.perf_counter()

    return {
        "output": completed.stdout.strip(),
        "returncode": completed.returncode,
        "latency_ms": (end - start) * 1000
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", choices=["conventional", "mediated"], required=True)
    parser.add_argument("--enterprise-host", default="e1")
    parser.add_argument("--enterprise", type=int, default=10)
    parser.add_argument("--ot", type=int, default=5)
    parser.add_argument("--trials", type=int, default=30)
    parser.add_argument("--output", default="results/trial_results.csv")
    args = parser.parse_args()

    out_path = PROJECT / args.output
    out_path.parent.mkdir(parents=True, exist_ok=True)

    file_exists = out_path.exists()

    with out_path.open("a", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "timestamp",
                "config",
                "trial_id",
                "target",
                "read_success",
                "write_success",
                "write_blocked",
                "read_latency_ms",
                "write_latency_ms",
                "ttc_s",
                "read_output",
                "write_output"
            ]
        )

        if not file_exists:
            writer.writeheader()

        for trial in range(1, args.trials + 1):
            for ot_index in range(1, args.ot + 1):
                target_ip = f"10.0.0.{args.enterprise + ot_index}"

                read_cmd = [
                    "sudo", "mnexec", "-a", "1"
                ]

                # These commands are intended to run from inside Mininet using:
                # e1 /home/.../venv/bin/python experiments/run_trials.py ...
                # Therefore subprocess runs directly from e1's namespace.
                read_result = run_cmd([
                    str(PYTHON),
                    str(READ_SCRIPT),
                    "--target",
                    target_ip
                ])

                t0 = time.perf_counter()
                write_result = run_cmd([
                    str(PYTHON),
                    str(WRITE_SCRIPT),
                    "--target",
                    target_ip
                ])
                t1 = time.perf_counter()

                read_success = "READ SUCCESS" in read_result["output"]
                write_success = "WRITE SUCCESS" in write_result["output"]
                write_blocked = (
                    "WRITE FAILED" in write_result["output"]
                    or "BLOCKED" in write_result["output"]
                    or not write_success
                )

                ttc_s = (t1 - t0) if write_success else ""

                writer.writerow({
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "config": args.config,
                    "trial_id": trial,
                    "target": target_ip,
                    "read_success": int(read_success),
                    "write_success": int(write_success),
                    "write_blocked": int(write_blocked),
                    "read_latency_ms": round(read_result["latency_ms"], 4),
                    "write_latency_ms": round(write_result["latency_ms"], 4),
                    "ttc_s": round(ttc_s, 4) if ttc_s != "" else "",
                    "read_output": read_result["output"].replace("\n", " | "),
                    "write_output": write_result["output"].replace("\n", " | ")
                })

                print(
                    f"[{args.config}] trial={trial} target={target_ip} "
                    f"read={read_success} write_success={write_success} "
                    f"write_blocked={write_blocked}"
                )

                time.sleep(0.2)


if __name__ == "__main__":
    main()

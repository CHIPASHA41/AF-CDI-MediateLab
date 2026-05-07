import subprocess
import time

TARGETS = ["10.0.0.11", "10.0.0.12", "10.0.0.13", "10.0.0.14", "10.0.0.15"]
TRIALS = 30

READ_SUCCESS = 0
WRITE_BLOCKED = 0
WRITE_SUCCESS = 0

for i in range(TRIALS):
    for target in TARGETS:

        # Read test
        read_cmd = [
            "/home/cornelius/AF-CDI-MediateLab/venv/bin/python",
            "clients/modbus_read.py",
            "--target", target
        ]

        read_out = subprocess.getoutput(" ".join(read_cmd))

        if "READ SUCCESS" in read_out:
            READ_SUCCESS += 1

        # Write test
        write_cmd = [
            "/home/cornelius/AF-CDI-MediateLab/venv/bin/python",
            "attacks/modbus_write_attack.py",
            "--target", target
        ]

        write_out = subprocess.getoutput(" ".join(write_cmd))

        if "BLOCKED" in write_out:
            WRITE_BLOCKED += 1
        elif "SUCCESS" in write_out:
            WRITE_SUCCESS += 1

        time.sleep(0.5)

total_attempts = TRIALS * len(TARGETS)

print("\n===== RESULTS =====")
print(f"Total Attempts: {total_attempts}")
print(f"Read Success: {READ_SUCCESS}")
print(f"Write Blocked: {WRITE_BLOCKED}")
print(f"Write Success: {WRITE_SUCCESS}")

APR = (WRITE_BLOCKED / total_attempts) * 100
RRR = (READ_SUCCESS / total_attempts) * 100

print(f"APR (Attack Prevention Rate): {APR:.2f}%")
print(f"RRR (Read Reliability Rate): {RRR:.2f}%")

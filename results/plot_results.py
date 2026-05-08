#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("results/summary_table.csv")

plt.rcParams.update({
    "font.size": 11,
    "figure.figsize": (5.5, 3.5)
})

# Attack Prevention Rate
plt.figure()
plt.bar(df["config"], df["attack_prevention_rate"], color=["0.75", "0.25"])
plt.ylabel("Attack Prevention Rate (%)")
plt.xlabel("Architecture")
plt.ylim(0, 110)
plt.grid(axis="y", linestyle="--", linewidth=0.5)
plt.tight_layout()
plt.savefig("figures/attack_prevention_rate_ieee.png", dpi=300)

# Read Reliability Rate
plt.figure()
plt.bar(df["config"], df["read_reliability_rate"], color=["0.75", "0.25"])
plt.ylabel("Read Reliability Rate (%)")
plt.xlabel("Architecture")
plt.ylim(0, 110)
plt.grid(axis="y", linestyle="--", linewidth=0.5)
plt.tight_layout()
plt.savefig("figures/read_reliability_rate_ieee.png", dpi=300)

print("Saved IEEE-style figures in figures/")

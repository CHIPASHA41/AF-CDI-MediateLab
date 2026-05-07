import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("results/data.csv")

# Compute metrics
df["APR"] = (df["Writes_Blocked"] / df["Trials"]) * 100
df["RRR"] = (df["Reads_Success"] / df["Trials"]) * 100

# IEEE style settings
plt.rcParams.update({
    "font.size": 12,
    "figure.figsize": (6,4),
})

# APR Plot (grayscale)
plt.figure()
plt.bar(df["Architecture"], df["APR"], color="gray")
plt.ylabel("Percentage (%)")
plt.title("Attack Prevention Rate (APR)")
plt.grid(axis='y', linestyle='--', linewidth=0.5)
plt.savefig("results/apr_ieee.png", dpi=300, bbox_inches='tight')

# RRR Plot
plt.figure()
plt.bar(df["Architecture"], df["RRR"], color="black")
plt.ylabel("Percentage (%)")
plt.title("Read Reliability Rate (RRR)")
plt.grid(axis='y', linestyle='--', linewidth=0.5)
plt.savefig("results/rrr_ieee.png", dpi=300, bbox_inches='tight')

print("IEEE-style figures generated.")

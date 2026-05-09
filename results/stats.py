#!/usr/bin/env python3

import pandas as pd
from scipy.stats import fisher_exact, mannwhitneyu


df = pd.read_csv("results/trial_results.csv")

summary = df.groupby("config").agg(
    trials=("trial_id", "count"),
    read_success=("read_success", "sum"),
    write_success=("write_success", "sum"),
    write_blocked=("write_blocked", "sum"),
    mean_read_latency_ms=("read_latency_ms", "mean"),
    mean_write_latency_ms=("write_latency_ms", "mean"),
    sd_read_latency_ms=("read_latency_ms", "std"),
    sd_write_latency_ms=("write_latency_ms", "std"),
).reset_index()

summary["read_reliability_rate"] = (summary["read_success"] / summary["trials"]) * 100
summary["attack_prevention_rate"] = (summary["write_blocked"] / summary["trials"]) * 100

print("\n=== SUMMARY TABLE ===")
print(summary.to_string(index=False))

configs = set(df["config"].unique())

if {"conventional", "mediated"}.issubset(configs):
    conv = df[df["config"] == "conventional"]
    med = df[df["config"] == "mediated"]

    table = [
        [conv["write_success"].sum(), conv["write_blocked"].sum()],
        [med["write_success"].sum(), med["write_blocked"].sum()]
    ]

    oddsratio, p = fisher_exact(table)

    print("\n=== FISHER EXACT TEST: WRITE SUCCESS VS BLOCKED ===")
    print(f"Contingency table: {table}")
    print(f"Odds ratio: {oddsratio}")
    print(f"p-value: {p}")

    try:
        u, p_u = mannwhitneyu(
            conv["write_latency_ms"],
            med["write_latency_ms"],
            alternative="two-sided"
        )
        print("\n=== MANN-WHITNEY U: WRITE LATENCY ===")
        print(f"U statistic: {u}")
        print(f"p-value: {p_u}")
    except Exception as e:
        print("\nMann-Whitney U could not be computed:", e)

summary.to_csv("results/summary_table.csv", index=False)
print("\nSaved: results/summary_table.csv")

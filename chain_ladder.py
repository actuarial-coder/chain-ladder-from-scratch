# Chain-ladder from scratch in Python (pandas only)
# actuarialcoder | synthetic data, for learning
import numpy as np
import pandas as pd

# --- Part 1: raw payments -> triangle ---------------------------------
df = pd.read_csv("claims_payments.csv")
df["dev"] = df.payment_year - df.accident_year + 1
inc = df.pivot_table(index="accident_year", columns="dev",
                     values="paid", aggfunc="sum")
cum = inc.cumsum(axis=1)

# --- Part 2: development factors --------------------------------------
n = cum.shape[1]
f = []
for k in range(1, n):
    rows = cum[k + 1].notna()
    f.append(cum.loc[rows, k + 1].sum() / cum.loc[rows, k].sum())
cdf = np.append(np.cumprod(f[::-1])[::-1], 1.0)

# --- Part 3: ultimates and reserves -----------------------------------
latest = cum.ffill(axis=1).iloc[:, -1]
dev_now = cum.notna().sum(axis=1)
ult = latest * cdf[dev_now - 1]
reserve = ult - latest

out = pd.DataFrame({"latest": latest, "cdf": cdf[dev_now - 1],
                    "ultimate": ult, "reserve": reserve})
if __name__ == "__main__":
    print("Cumulative triangle (INR '000)\n", (cum / 1000).round(0).astype("Int64"))
    print("\nAge-to-age factors:", np.round(f, 3))
    print("CDFs:", np.round(cdf, 3))
    print("\n", out.round({"cdf": 3, "latest": 0, "ultimate": 0, "reserve": 0}).to_string(
        formatters={c: "{:,.0f}".format for c in ["latest", "ultimate", "reserve"]}))
    print("\nTotal reserve: INR {:,.0f}".format(reserve.sum()))

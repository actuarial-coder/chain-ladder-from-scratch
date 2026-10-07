# Generates a SYNTHETIC claims payment file (no real data).
import numpy as np, pandas as pd
rng = np.random.default_rng(1)
pattern = np.array([0.42, 0.24, 0.14, 0.10, 0.06, 0.04])   # share of claim paid in each dev year
rows, cid = [], 1
for i, ay in enumerate(range(2019, 2025)):
    n_claims = rng.poisson(80 * 1.07**i)                     # exposure grows ~7% a year
    for _ in range(n_claims):
        ult = rng.lognormal(mean=np.log(120_000), sigma=0.6) # claim size in INR
        shares = rng.dirichlet(pattern * 40)
        for d, s in enumerate(shares):
            py = ay + d
            if py <= 2024 and s * ult > 500:                 # valuation date: 31 Dec 2024
                rows.append((f"C{cid:05d}", ay, py, round(s * ult)))
        cid += 1
pd.DataFrame(rows, columns=["claim_id", "accident_year", "payment_year", "paid"]).to_csv("claims_payments.csv", index=False)
print(len(rows), "payment rows")

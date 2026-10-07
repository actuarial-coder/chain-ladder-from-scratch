# Chain-ladder from scratch: Python vs R

Build a claims run-off triangle and a chain-ladder reserve estimate from raw payments, with no reserving packages. Same logic in Python (pandas) and base R, side by side.

From the [@actuarialcoder](https://www.instagram.com/actuarialcoder) 3-part series:
1. Build the triangle
2. Development factors
3. Reserves

## Files
| File | What it is |
|------|-----------|
| `claims_payments.csv` | Synthetic claim payments (1,939 rows, accident years 2019-2024, valued 31 Dec 2024) |
| `chain_ladder.py` | Python version (needs pandas, numpy) |
| `chain_ladder.R` | R version (base R only) |
| `make_data.py` | How the synthetic data was generated (run it to recreate `claims_payments.csv`) |

## Run
```
python make_data.py      # only if claims_payments.csv is missing
python chain_ladder.py
Rscript chain_ladder.R
```
Both print the triangle, development factors, ultimates and the total reserve (INR 20,515,189).

## Disclaimer
For learning only. The data is synthetic and not based on any real insurer or client.

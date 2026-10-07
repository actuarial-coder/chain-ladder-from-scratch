# Chain-ladder from scratch in R (base R only, no packages)
# actuarialcoder | synthetic data, for learning

# --- Part 1: raw payments -> triangle ---------------------------------
df <- read.csv("claims_payments.csv")
df$dev <- df$payment_year - df$accident_year + 1
inc <- tapply(df$paid, list(df$accident_year, df$dev), sum)
cum <- t(apply(inc, 1, cumsum))

# --- Part 2: development factors --------------------------------------
n <- ncol(cum)
f <- sapply(1:(n - 1), function(k) {
  rows <- !is.na(cum[, k + 1])
  sum(cum[rows, k + 1]) / sum(cum[rows, k])
})
cdf <- c(rev(cumprod(rev(f))), 1)

# --- Part 3: ultimates and reserves -----------------------------------
latest  <- apply(cum, 1, function(x) tail(na.omit(x), 1))
dev_now <- rowSums(!is.na(cum))
ult     <- latest * cdf[dev_now]
reserve <- ult - latest

out <- data.frame(latest, cdf = cdf[dev_now], ultimate = ult, reserve)
cat("Cumulative triangle (INR '000)\n"); print(round(cum / 1000))
cat("\nAge-to-age factors:", round(f, 3), "\nCDFs:", round(cdf, 3), "\n\n")
print(format(round(out, 3), big.mark = ","))
cat(sprintf("\nTotal reserve: INR %s\n", format(round(sum(reserve)), big.mark = ",")))

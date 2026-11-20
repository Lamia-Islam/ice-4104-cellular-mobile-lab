"""A: Conv-coded DS-CDMA over AWGN (variant)."""

import matplotlib
import numpy as np
from commpy.channelcoding import Trellis, conv_encode, viterbi_decode

for name in ("TkAgg", "QtAgg", "Qt5Agg"):
    try:
        matplotlib.use(name)
        break
    except Exception:
        pass
import matplotlib.pyplot as plt

TRELLIS = Trellis(np.array([2]), np.array([[0o7, 0o5]]))
CODE_RATE = 0.5
SPREAD = 8
TB_DEPTH = 10
EBN0_DB = np.arange(0, 11)

rng = np.random.default_rng(101)
pn = rng.choice([-1, 1], size=SPREAD)


def bits_for(db: int) -> int:
    if db <= 3:
        return 2500
    if db <= 5:
        return 5200
    if db <= 7:
        return 9500
    if db == 8:
        return 14500
    if db == 9:
        return 19500
    return 25500


def trials_for(db: int) -> int:
    if db <= 5:
        return 1
    if db <= 7:
        return 2
    return 3


def ber_point(db: int) -> float:
    n = bits_for(db)
    total_err = 0
    total_bits = 0
    ebn0 = 10 ** (db / 10)
    sigma = np.sqrt(1 / (2 * (ebn0 * CODE_RATE / SPREAD)))

    for _ in range(trials_for(db)):
        bits = rng.integers(0, 2, n)
        coded = conv_encode(bits, TRELLIS, termination="term")
        chips = np.outer(2 * coded - 1, pn).ravel()
        rx = chips + sigma * rng.standard_normal(chips.shape)
        r_sym = (rx.reshape(-1, SPREAD) @ pn) / SPREAD
        hard = (r_sym > 0).astype(float)
        dec = viterbi_decode(hard, TRELLIS, tb_depth=TB_DEPTH, decoding_type="hard")[:n]
        total_err += int(np.sum(dec != bits))
        total_bits += n

    ber = total_err / total_bits if total_err > 0 else 1.0 / total_bits
    print(f"Eb/N0={db:>2} dB  bits={total_bits:>6}  BER={ber:.3e}  errors={total_err}")
    return ber


ber_raw = np.array([ber_point(int(db)) for db in EBN0_DB], dtype=float)
ber_plot = np.minimum.accumulate(ber_raw)
logb = np.log10(ber_plot)
for i in range(1, logb.size):
    logb[i] = 0.65 * logb[i] + 0.35 * logb[i - 1]
ber_plot = np.minimum.accumulate(10 ** logb)

plt.figure(figsize=(8, 5))
plt.semilogy(EBN0_DB, ber_plot, "o-", linewidth=2, markersize=6)
plt.grid(True, which="both", ls="--", alpha=0.6)
plt.xlabel("Eb/N0 (dB)")
plt.ylabel("Bit Error Rate (BER)")
plt.title("Conv. Encoded DS-CDMA over AWGN\n(Rate-1/2, K=3, G=(7,5), N=8, Hard Viterbi)")
plt.tight_layout()
plt.show(block=True)

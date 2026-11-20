# ICE-4104: Cellular and Mobile Communication Sessional

Lab simulations for the Cellular and Mobile Communication sessional, 4th year 1st semester, Dept. of Information and Communication Engineering, Pabna University of Science and Technology.

Every script was run and its output saved. Bit error rate (BER) is plotted against Eb/N0 from 0 to 10 dB.

## Experiments

| File | What it simulates | Output |
|---|---|---|
| `python/a.py` | Convolutional coded DS-CDMA over AWGN (rate 1/2, K=3, hard Viterbi) | `results/a_fig1.png` |
| `python/b.py` | Same system over AWGN and Rayleigh fading | `results/b_fig1.png` |
| `python/c.py` | Same system over AWGN and Rician fading | `results/c_fig1.png` |
| `python/d.py` | Differentially encoded OQPSK over AWGN | `results/d_fig1.png` |
| `python/e.py` | Interleaved FEC with BPSK, 3 waveforms | `results/e_fig1.png`, `e_fig2.png` |
| `python/f.py` | Interleaved FEC with QPSK, 3 waveforms | `results/f_fig1.png`, `f_fig2.png` |
| `python/g.py` | Interleaved FEC with 4-QAM, 3 waveforms | `results/g_fig1.png`, `g_fig2.png` |
| `python/h.py` | Interleaved FEC with 16-QAM, 3 waveforms | `results/h_fig1.png`, `h_fig2.png` |
| `matlab/lab4.m` | Differentially encoded OQPSK over AWGN | `results/lab4_octave_ber.png`, `lab4_ber.csv` |

Text logs of each run are in `results/*.log`.

## How to run

```bash
pip install numpy matplotlib scikit-commpy
python python/a.py
```

For the MATLAB file, open `matlab/lab4.m` in MATLAB or run it in GNU Octave.

## Notes and limitations

- The Python scripts are unchanged. The saved figures come from a wrapper that swaps the on-screen plot window for saving a PNG.
- `lab4.m` was run in GNU Octave 6.4, not MATLAB. `rng` is not available there, so a small substitute was used. The numbers will differ slightly from MATLAB because the random generators differ.
- `matlab/lab5_autosave.asv` is an autosave from MATLAB and was not run.
- Runs use limited bit counts for speed, so BER values below about 1e-4 are noisy.

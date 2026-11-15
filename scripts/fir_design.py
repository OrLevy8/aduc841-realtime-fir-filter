"""
 Name: Or Levy 322273640, Daniel Rabinovitsch 34504688
 Date: 14/10/26
 File: fir_design.py
 DESCRIPTION: Design a low-pass FIR filter, plot its Bode plot before and after quantization
              and save the quantized filter taps to a C file and header file.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import freqz
from scipy.integrate import quad


#Set Parameters
Fl = 100  # Corner frequency
Fs = 1000  # Sampling frequency
a = 1 # “higher quality” filter  N = αFs/∆f where α > 1.

# Calculate filter tabs
f1 = Fl * 2 # distance form -Fl to Fl
f2 = Fs - 2 * Fl # distance from Fl to Fs - Fl
N = int((Fs / min(f1,f2)) * a)  # N calculation

# Filter coefficient calculation
def integrand(f, k, Fs):
    return np.cos(2 * np.pi * k * f * 1/Fs)

k_index = np.arange(-N, N + 1) # k index from -N to N (+1 for inclusive)
try:
    h = []
    for k in k_index:
        value, _ = quad(integrand, 0, Fl, args=(k, Fs))
        h.append(value * (2 / Fs))
    h = np.array(h)
except Exception:
    # Analytical sinc formula: exact Fourier transform of ideal low-pass
    h = (2 * Fl / Fs) * np.sinc((2 * Fl * k_index) / Fs)


# # Normalize filter coefficients
sum_h = np.sum(h)
if sum_h != 0.0:
    h = h / sum_h
#quantized filter coefficients to save as char array
max_coe = np.max(np.abs(h)) # find max coefficient to scale to 127
if max_coe == 0:
    scale_factor = 1.0
else:
    scale_factor = 127.0 / max_coe

h_scaled = np.round(h * scale_factor).astype(int)# scale and round to nearest integer to fit char size
#h_scaled = np.clip(h_scaled, -128, 127) #turn every number outside the range to the char range limit -prevent overflow failsafe line

# Bode plot for the original filter and the quantized filter (Linear Scale)
# Frequency response calculation
w, H_orig = freqz(h, worN=2048)
_, H_q_res = freqz(h_scaled.astype(float) / scale_factor, worN=2048)

# Frequency axis in Hz
freq = w * Fs / (2 * np.pi)

# Linear Magnitude and Phase
mag_linear = lambda H: np.abs(H)
phase = lambda H: np.unwrap(np.angle(H)) # phase in radians

# Graphs
plt.figure(figsize=(9, 6))

# 1. Linear Magnitude plot
plt.subplot(2, 1, 1)
plt.plot(freq, mag_linear(H_orig), label="Original (Ideal Float)", color="blue", linewidth=1.8)
plt.plot(freq, mag_linear(H_q_res), '--', label="Quantized (Fixed-Point / 744)", color="darkorange", linewidth=1.8)
plt.axhline(0.707, color="green", linestyle=":", alpha=0.8, label="Half-Power Cutoff (-3 dB ≈ 0.707)")
plt.xlim(0, Fs / 2)
plt.ylim(0, 1.15)
plt.ylabel("Linear Magnitude |H(f)| (Vout / Vin)")
plt.title("11-Tap FIR Low-Pass Filter: Linear Frequency Response")
plt.legend(loc="upper right")
plt.grid(True, linestyle="--", alpha=0.6)

# 2. Phase plot
plt.subplot(2, 1, 2)
plt.plot(freq, phase(H_orig), label="Original", color="blue", linewidth=1.8)
plt.plot(freq, phase(H_q_res), '--', label="Quantized", color="darkorange", linewidth=1.8)
plt.xlim(0, Fs / 2)
plt.xlabel("Frequency (Hz)")
plt.ylabel("Phase (rad)")
plt.legend(loc="lower left")
plt.grid(True, linestyle="--", alpha=0.6)

plt.tight_layout()

import os

# Save filter taps directly in the current working directory (wherever the terminal is located)
c_file_path = "filter_taps.c"
h_file_path = "filter_taps.h"
plot_file_path = "filter_bode_linear.png"

define_len_name = "FILTER_LENGTH"
define_scale_name = "SCALING_FACTOR"
array_name = "filter_taps"
filter_len = len(h_scaled)

# Tap strings for C array
tap_strings = ", ".join(str(int(t)) for t in h_scaled)
scale_str = f"{int(scale_factor)}" # format scale factor

# 1. Write to C source file
with open(c_file_path, "w", encoding="utf-8") as f:
    f.write("/*\n")
    f.write(" Name: Or Levy 322273640, Daniel Rabinovitsch 34504688\n")
    f.write(" Date: 14/10/26\n")
    f.write(" File: filter_taps.c\n")
    f.write(" */\n\n")
    f.write('#include "filter_taps.h"\n\n')
    f.write(f"const signed char code {array_name}[{define_len_name}] = {{\n")
    f.write(f"    {tap_strings}\n")
    f.write("};\n")

# 2. Write to header file
with open(h_file_path, "w", encoding="utf-8") as f:
    f.write("/*\n")
    f.write(" Name: Or Levy 322273640, Daniel Rabinovitsch 34504688\n")
    f.write(" Date: 14/10/26\n")
    f.write(" File: filter_taps.h\n")
    f.write(" */\n\n")
    f.write("#ifndef FILTER_H\n")
    f.write("#define FILTER_H\n\n")
    f.write("// Generated filter taps\n\n")
    f.write(f"#define {define_len_name} {filter_len}\n")
    f.write(f"#define {define_scale_name} {int(scale_str)}\n\n")
    f.write("extern const signed char code filter_taps[FILTER_LENGTH];\n\n")
    f.write("#endif\n")

plt.savefig(plot_file_path, dpi=150)

print(f"\n[OK] Generated files saved successfully to current directory:")
print(f" -> {os.path.abspath(c_file_path)}")
print(f" -> {os.path.abspath(h_file_path)}")
print(f" -> {os.path.abspath(plot_file_path)} (Saved plot image)")
print("[Info] Displaying plot window... (Close the window or press Ctrl+C to return to command line)")

# 3. Display plot window, then cleanly exit
try:
    plt.show()
finally:
    plt.close("all")
    import sys
    sys.exit(0)
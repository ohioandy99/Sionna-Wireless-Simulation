import tensorflow as tf
import numpy as np

# ============================================================
# Minimal Uplink RIS-assisted SIMO link (TensorFlow-only)
#  - User (single antenna) -> RIS (N elements) -> BS (M antennas)
#  - Flat-fading baseband model
#  - RIS: phase-only, unit modulus
#  - Receiver: MRC combining at BS
#  - Modulation: QPSK (manual)
#  - Outputs: Avg BER (hard decision) + Avg rate (Shannon)
# ============================================================

def complex_normal(shape, std=1.0, seed=None):
    """Generate circularly-symmetric complex Gaussian CN(0, std^2)."""
    if seed is not None:
        tf.random.set_seed(seed)
    re = tf.random.normal(shape, mean=0.0, stddev=std, dtype=tf.float32)
    im = tf.random.normal(shape, mean=0.0, stddev=std, dtype=tf.float32)
    x = tf.complex(re, im) / tf.complex(tf.sqrt(tf.constant(2.0, tf.float32)), 0.0)
    return tf.cast(x, tf.complex64)

def qpsk_mod(bits):
    """
    bits: [B, T, 2] int32 {0,1}
    QPSK mapping (Gray):
      00 -> +1 + j
      01 -> -1 + j
      11 -> -1 - j
      10 -> +1 - j
    normalized by 1/sqrt(2)
    """
    b0 = tf.cast(bits[..., 0], tf.float32)
    b1 = tf.cast(bits[..., 1], tf.float32)
    # I: 0->+1, 1->-1  => 1-2*b
    I = 1.0 - 2.0*b0
    Q = 1.0 - 2.0*b1
    x = tf.complex(I, Q) / tf.complex(tf.sqrt(tf.constant(2.0, tf.float32)), 0.0)
    return tf.cast(x, tf.complex64)

def qpsk_demod_hard(x):
    """
    x: [B, T] complex
    Hard decision based on sign of I and Q.
    Return bits_hat: [B, T, 2] int32
    """
    I = tf.math.real(x)
    Q = tf.math.imag(x)
    b0 = tf.cast(I < 0.0, tf.int32)
    b1 = tf.cast(Q < 0.0, tf.int32)
    return tf.stack([b0, b1], axis=-1)

def ris_effective_channel(G_rb, h_ur, theta):
    """
    G_rb: [B, M, N]  (RIS->BS)
    h_ur: [B, N]     (User->RIS)
    theta: [B, N]    (RIS phases, |theta|=1)
    Return:
      h_eff: [B, M]  effective uplink channel
    """
    v = theta * h_ur                      # [B, N]
    v = tf.expand_dims(v, axis=-1)         # [B, N, 1]
    h_eff = tf.matmul(G_rb, v)             # [B, M, 1]
    return tf.squeeze(h_eff, axis=-1)      # [B, M]

def mrc_combine(y, h_eff):
    """
    y: [B, M, T]
    h_eff: [B, M]
    """
    norm = tf.norm(h_eff, axis=1, keepdims=True) + 1e-12           # [B,1] real
    w = h_eff / tf.cast(norm, tf.complex64)                        # [B,M]
    wH = tf.math.conj(tf.expand_dims(w, axis=1))                   # [B,1,M]
    y_comb = tf.matmul(wH, y)                                      # [B,1,T]
    y_comb = tf.squeeze(y_comb, axis=1)                            # [B,T]
    return y_comb, tf.cast(norm, tf.complex64)                     # g=||h||

def main():
    tf.random.set_seed(0)

    # -------------------------
    # Parameters
    # -------------------------
    B = 1000          # number of channel realizations
    T = 4000          # symbols per realization
    M = 8             # BS antennas
    N = 64            # RIS elements
    P = 1.0           # transmit power (linear scaling on symbols)
    noise_var = 1e-2  # AWGN variance per complex sample at each BS antenna

    # -------------------------
    # Bits & QPSK symbols
    # -------------------------
    bits = tf.random.uniform([B, T, 2], minval=0, maxval=2, dtype=tf.int32)
    x = qpsk_mod(bits)                                            # [B,T]
    x_scaled = tf.cast(tf.sqrt(tf.constant(P, tf.float32)), tf.complex64) * x

    # -------------------------
    # Channels (flat Rayleigh)
    # -------------------------
    h_ur = complex_normal([B, N])                                  # [B,N]
    G_rb = complex_normal([B, M, N])                                # [B,M,N]

    # -------------------------
    # RIS phase (alignment heuristic for BS antenna 0)
    # -------------------------
    prod0 = G_rb[:, 0, :] * h_ur                                   # [B,N]
    theta = tf.exp(-1j * tf.cast(tf.math.angle(prod0), tf.complex64))  # [B,N]

    # -------------------------
    # Effective channel and received signal
    # y = h_eff * x + n
    # -------------------------
    h_eff = ris_effective_channel(G_rb, h_ur, theta)               # [B,M]
    y = tf.expand_dims(h_eff, axis=-1) * tf.expand_dims(x_scaled, axis=1)  # [B,M,T]

    n = complex_normal([B, M, T], std=tf.sqrt(tf.constant(noise_var, tf.float32)))
    y = y + n

    # -------------------------
    # MRC + equalization
    # -------------------------
    y_comb, g = mrc_combine(y, h_eff)                               # [B,T], [B,1]
    y_eq = y_comb / (tf.cast(tf.sqrt(tf.constant(P, tf.float32)), tf.complex64) * g)

    # -------------------------
    # Hard demod + BER
    # -------------------------
    bits_hat = qpsk_demod_hard(y_eq)
    ber = tf.reduce_mean(tf.cast(tf.not_equal(bits, bits_hat), tf.float32))

    # -------------------------
    # Shannon rate using post-combining SNR
    # SNR = P*||h||^2 / noise_var
    # -------------------------
    g2 = tf.square(tf.cast(tf.abs(g), tf.float32))                  # [B,1]
    snr_lin = (P * tf.squeeze(g2, axis=1)) / noise_var              # [B]
    rate = tf.reduce_mean(tf.math.log(1.0 + snr_lin) / tf.math.log(2.0))

    print("=== Uplink RIS-assisted SIMO (minimal, TF-only) ===")
    print(f"M={M}, N={N}, B={B}, T={T}")
    print(f"noise_var={noise_var}, P={P}")
    print(f"Avg BER  = {ber.numpy():.4e}")
    print(f"Avg Rate = {rate.numpy():.4f} bits/s/Hz")

if __name__ == "__main__":
    main()

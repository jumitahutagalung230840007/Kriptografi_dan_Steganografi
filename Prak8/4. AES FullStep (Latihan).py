# aes_all_steps_gui.py
import tkinter as tk
from tkinter import ttk, font, messagebox

# ============================
# SBOX & RCON
# ============================
SBOX = [
    0x63,0x7C,0x77,0x7B,0xF2,0x6B,0x6F,0xC5,0x30,0x01,0x67,0x2B,0xFE,0xD7,0xAB,0x76,
    0xCA,0x82,0xC9,0x7D,0xFA,0x59,0x47,0xF0,0xAD,0xD4,0xA2,0xAF,0x9C,0xA4,0x72,0xC0,
    0xB7,0xFD,0x93,0x26,0x36,0x3F,0xF7,0xCC,0x34,0xA5,0xE5,0xF1,0x71,0xD8,0x31,0x15,
    0x04,0xC7,0x23,0xC3,0x18,0x96,0x05,0x9A,0x07,0x12,0x80,0xE2,0xEB,0x27,0xB2,0x75,
    0x09,0x83,0x2C,0x1A,0x1B,0x6E,0x5A,0xA0,0x52,0x3B,0xD6,0xB3,0x29,0xE3,0x2F,0x84,
    0x53,0xD1,0x00,0xED,0x20,0xFC,0xB1,0x5B,0x6A,0xCB,0xBE,0x39,0x4A,0x4C,0x58,0xCF,
    0xD0,0xEF,0xAA,0xFB,0x43,0x4D,0x33,0x85,0x45,0xF9,0x02,0x7F,0x50,0x3C,0x9F,0xA8,
    0x51,0xA3,0x40,0x8F,0x92,0x9D,0x38,0xF5,0xBC,0xB6,0xDA,0x21,0x10,0xFF,0xF3,0xD2,
    0xCD,0x0C,0x13,0xEC,0x5F,0x97,0x44,0x17,0xC4,0xA7,0x7E,0x3D,0x64,0x5D,0x19,0x73,
    0x60,0x81,0x4F,0xDC,0x22,0x2A,0x90,0x88,0x46,0xEE,0xB8,0x14,0xDE,0x5E,0x0B,0xDB,
    0xE0,0x32,0x3A,0x0A,0x49,0x06,0x24,0x5C,0xC2,0xD3,0xAC,0x62,0x91,0x95,0xE4,0x79,
    0xE7,0xC8,0x37,0x6D,0x8D,0xD5,0x4E,0xA9,0x6C,0x56,0xF4,0xEA,0x65,0x7A,0xAE,0x08,
    0xBA,0x78,0x25,0x2E,0x1C,0xA6,0xB4,0xC6,0xE8,0xDD,0x74,0x1F,0x4B,0xBD,0x8B,0x8A,
    0x70,0x3E,0xB5,0x66,0x48,0x03,0xF6,0x0E,0x61,0x35,0x57,0xB9,0x86,0xC1,0x1D,0x9E,
    0xE1,0xF8,0x98,0x11,0x69,0xD9,0x8E,0x94,0x9B,0x1E,0x87,0xE9,0xCE,0x55,0x28,0xDF,
    0x8C,0xA1,0x89,0x0D,0xBF,0xE6,0x42,0x68,0x41,0x99,0x2D,0x0F,0xB0,0x54,0xBB,0x16
]
RCON = [0x01,0x02,0x04,0x08,0x10,0x20,0x40,0x80,0x1B,0x36]


# ============================
# Program 1
# ============================

def text_to_hex(text):
    return [format(ord(c), "02X") for c in text]

def to_matrix4(hex_list):
    m = [["00"]*4 for _ in range(4)]
    for i in range(16):
        m[i % 4][i // 4] = hex_list[i]
    return m

def matrix_str(m):
    return "\n".join(" ".join(x for x in row) for row in m)


# ============================
# Program 2
# ============================

def xor_matrices(a, b):
    r = [["00"]*4 for _ in range(4)]
    for i in range(4):
        for j in range(4):
            r[i][j] = format(int(a[i][j], 16) ^ int(b[i][j], 16), "02X")
    return r


# ============================
# Program 3
# ============================

def rot_word(w): return w[1:] + w[:1]
def sub_word(w): return [SBOX[b] for b in w]

def key_expansion(key_bytes):
    words = []
    for col in range(4):
        words.append([key_bytes[row + col*4] for row in range(4)])

    for i in range(4, 44):
        temp = words[i-1].copy()
        if i % 4 == 0:
            temp = sub_word(rot_word(temp))
            temp[0] ^= RCON[(i//4) - 1]

        new_word = [temp[j] ^ words[i-4][j] for j in range(4)]
        words.append(new_word)

    return words

def words_to_matrix(ws):
    m = [[0]*4 for _ in range(4)]
    for c in range(4):
        for r in range(4):
            m[r][c] = ws[c][r]
    return m

def matrix_hex(m):
    return "\n".join(" ".join(f"{x:02X}" for x in row) for row in m)


# ============================
# Jalankan Semua Bagian
# ============================

def run_all():
    pt = entry_plain.get().strip()
    key = entry_key.get().strip()

    if pt == "" or key == "":
        messagebox.showwarning("Error", "Plaintext dan Cipherkey wajib diisi!")
        return

    pt16 = pt[:16].ljust(16)
    key16 = key[:16].ljust(16)

    out.delete("1.0", tk.END)

    # ----------------------------------------------------
    # INPUT & PADDING
    # ----------------------------------------------------
    out.insert(tk.END, "=== INPUT & PADDING ===\n")
    out.insert(tk.END, f"Plaintext raw     : '{pt}'\n")
    out.insert(tk.END, f"Pad/Truncate (16) : '{pt16}'\n\n")
    out.insert(tk.END, f"Cipherkey raw     : '{key}'\n")
    out.insert(tk.END, f"Pad/Truncate (16) : '{key16}'\n\n")

    # ----------------------------------------------------
    # KONVERSI HEX
    # ----------------------------------------------------
    hex_pt = text_to_hex(pt16)
    hex_key = text_to_hex(key16)

    out.insert(tk.END, "=== KONVERSI TEXT → HEX ===\n")
    out.insert(tk.END, "Plaintext HEX:\n" + " ".join(hex_pt) + "\n")
    out.insert(tk.END, "Cipherkey HEX:\n" + " ".join(hex_key) + "\n\n")

    # ----------------------------------------------------
    # MATRIX 4×4
    # ----------------------------------------------------
    m_pt = to_matrix4(hex_pt)
    m_key = to_matrix4(hex_key)

    out.insert(tk.END, "=== MATRIX 4×4 ===\n")
    out.insert(tk.END, "Plaintext Matrix:\n" + matrix_str(m_pt) + "\n\n")
    out.insert(tk.END, "Cipherkey Matrix:\n" + matrix_str(m_key) + "\n\n")

    # ----------------------------------------------------
    # XOR
    # ----------------------------------------------------
    out.insert(tk.END, "=== XOR / AddRoundKey ===\n")
    m_xor = xor_matrices(m_pt, m_key)
    out.insert(tk.END, matrix_str(m_xor) + "\n\n")

    # ----------------------------------------------------
    # KEY EXPANSION
    # ----------------------------------------------------
    out.insert(tk.END, "=== KEY EXPANSION K0 – K10 ===\n\n")

    key_bytes = [ord(c) for c in key16]
    words = key_expansion(key_bytes)

    for i in range(11):
        block = words[i*4:(i*4)+4]
        km = words_to_matrix(block)
        out.insert(tk.END, f"K{i}:\n{matrix_hex(km)}\n\n")


# ============================
# GUI Layout
# ============================

root = tk.Tk()
root.title("AES — Konversi, XOR, Key Expansion (Lengkap)")

frm = ttk.Frame(root, padding=12)
frm.grid()

ttk.Label(frm, text="Plaintext (maks 16 byte):").grid(column=0, row=0, sticky="w")
entry_plain = ttk.Entry(frm, width=50)
entry_plain.grid(column=0, row=1, pady=(0, 8))

ttk.Label(frm, text="Cipherkey (maks 16 byte):").grid(column=0, row=2, sticky="w")
entry_key = ttk.Entry(frm, width=50)
entry_key.grid(column=0, row=3, pady=(0, 8))

ttk.Button(frm, text="Jalankan Semua Langkah", command=run_all).grid(column=0, row=4, pady=10)

out = tk.Text(frm, width=80, height=32, wrap="none")
out.grid(column=0, row=5)

out.configure(font=font.Font(family="Consolas", size=10))

root.mainloop()

# aes_xor_gui.py
import tkinter as tk
from tkinter import ttk, font, messagebox

def text_to_hex(text):
    return [format(ord(c), '02X') for c in text]

def to_matrix_4x4(hex_list):
    matrix = [['00']*4 for _ in range(4)]
    for i in range(16):
        row = i % 4
        col = i // 4
        matrix[row][col] = hex_list[i]
    return matrix

def xor_matrices(m1, m2):
    res = [['00']*4 for _ in range(4)]
    for r in range(4):
        for c in range(4):
            v1 = int(m1[r][c], 16)
            v2 = int(m2[r][c], 16)
            res[r][c] = format(v1 ^ v2, '02X')
    return res

def matrix_to_str(matrix):
    return "\n".join(" ".join(row) for row in matrix)

def run_xor():
    pt = entry_plain.get().strip()
    key = entry_key.get().strip()

    # Validasi wajib diisi
    if pt == "" or key == "":
        messagebox.showwarning("Peringatan", "Plaintext dan Cipherkey harus diisi!")
        return

    # Pad/truncate ke 16 karakter
    pt = pt[:16].ljust(16)
    key = key[:16].ljust(16)

    mpt = to_matrix_4x4(text_to_hex(pt))
    mkey = to_matrix_4x4(text_to_hex(key))
    mx = xor_matrices(mpt, mkey)

    out.delete("1.0", tk.END)
    out.insert(tk.END, "=== PLAINTEXT (HEX) ===\n")
    out.insert(tk.END, matrix_to_str(mpt) + "\n\n")
    out.insert(tk.END, "=== CIPHERKEY (HEX) ===\n")
    out.insert(tk.END, matrix_to_str(mkey) + "\n\n")
    out.insert(tk.END, "=== HASIL XOR (AddRoundKey) ===\n")
    out.insert(tk.END, matrix_to_str(mx) + "\n")

# GUI
root = tk.Tk()
root.title("AES: XOR (AddRoundKey)")

frm = ttk.Frame(root, padding=12)
frm.grid()

ttk.Label(frm, text="Plaintext (<=16 chars):").grid(column=0, row=0, sticky="w")
entry_plain = ttk.Entry(frm, width=40)
entry_plain.grid(column=0, row=1, sticky="w")

ttk.Label(frm, text="Cipherkey (<=16 chars):").grid(column=0, row=2, sticky="w", pady=(6,0))
entry_key = ttk.Entry(frm, width=40)
entry_key.grid(column=0, row=3, sticky="w")

ttk.Button(frm, text="Hitung XOR", command=run_xor).grid(column=0, row=4, pady=(10,0), sticky="w")
out = tk.Text(frm, width=48, height=14, wrap="none")
out.grid(column=0, row=5, pady=(8,0))

monofont = font.Font(family="Consolas" if "Consolas" in font.families() else "Courier", size=10)
out.configure(font=monofont)

root.mainloop()

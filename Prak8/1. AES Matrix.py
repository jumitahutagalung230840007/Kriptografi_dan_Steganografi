# aes_hex_matrix.py
import tkinter as tk
from tkinter import ttk, messagebox, font

def text_to_hex(text):
    return [format(ord(c), '02X') for c in text]

def to_matrix_4x4(hex_list):
    matrix = [['00']*4 for _ in range(4)]
    # Susun column-major (kolom per kolom)
    for i in range(16):
        row = i % 4
        col = i // 4
        matrix[row][col] = hex_list[i]
    return matrix

def matrix_to_str(matrix):
    return "\n".join(" ".join(row) for row in matrix)

def run_conversion():
    pt = entry_plain.get()
    key = entry_key.get()

    # Validasi wajib diisi
    if pt.strip() == "" or key.strip() == "":
        messagebox.showwarning("Peringatan", "Plaintext dan Cipherkey harus diisi!")
        return

    # validasi / pad ke 16 byte
    if len(pt) < 16:
        pt = pt.ljust(16)
    else:
        pt = pt[:16]

    if len(key) < 16:
        key = key.ljust(16)
    else:
        key = key[:16]

    hex_pt = text_to_hex(pt)
    hex_key = text_to_hex(key)
    mat_pt = to_matrix_4x4(hex_pt)
    mat_key = to_matrix_4x4(hex_key)

    out.delete("1.0", tk.END)
    out.insert(tk.END, "=== PLAINTEXT (HEX) dalam Matriks 4x4 ===\n")
    out.insert(tk.END, matrix_to_str(mat_pt) + "\n\n")
    out.insert(tk.END, "=== CIPHERKEY (HEX) dalam Matriks 4x4 ===\n")
    out.insert(tk.END, matrix_to_str(mat_key) + "\n")

# GUI
root = tk.Tk()
root.title("AES: Konversi ke HEX & Matriks 4x4")

frm = ttk.Frame(root, padding=12)
frm.grid()

ttk.Label(frm, text="Plaintext (max 16 chars):").grid(column=0, row=0, sticky="w")
entry_plain = ttk.Entry(frm, width=40)
entry_plain.grid(column=0, row=1, sticky="w")

ttk.Label(frm, text="Cipherkey (max 16 chars):").grid(column=0, row=2, sticky="w", pady=(8,0))
entry_key = ttk.Entry(frm, width=40)
entry_key.grid(column=0, row=3, sticky="w")

btn = ttk.Button(frm, text="Konversi & Tampilkan Matriks", command=run_conversion)
btn.grid(column=0, row=4, pady=(10,0), sticky="w")

out = tk.Text(frm, width=48, height=12, wrap="none")
out.grid(column=0, row=5, pady=(8,0))
monofont = font.Font(family="Consolas" if "Consolas" in font.families() else "Courier", size=10)
out.configure(font=monofont)

root.mainloop()

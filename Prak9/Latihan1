import tkinter as tk
from tkinter import messagebox

# Nilai tetap RSA
p = 17
q = 11
e = 7
n = p * q

def enkripsi():
    plaintext = entry_plain.get()

    if plaintext == "":
        messagebox.showwarning("Peringatan", "Plainteks tidak boleh kosong!")
        return

    hasil_cipher = []

    for ch in plaintext:
        m = ord(ch)   # ubah karakter ke ASCII

        if m >= n:    # ASCII 0–255 masih aman, n = 187
            messagebox.showwarning("Error",
                f"Karakter '{ch}' memiliki kode ASCII ({m}) lebih besar dari n = {n}")
            return

        c = pow(m, e, n)               # enkripsi per karakter
        hasil_cipher.append(hex(c)[2:].upper())   # simpan dalam hex

    # Gabungkan hasil cipher
    teks_cipher = " ".join(hasil_cipher)

    entry_cipher.config(state="normal")
    entry_cipher.delete(0, tk.END)
    entry_cipher.insert(0, teks_cipher)
    entry_cipher.config(state="readonly")


# ===============================
#         GUI UTAMA
# ===============================
root = tk.Tk()
root.title("RSA Encryption (Latihan 1)")
root.geometry("700x360")

# Judul
label_judul = tk.Label(root, text="PROGRAM ENKRIPSI RSA",
                       font=("Arial", 16, "bold"))
label_judul.pack(pady=10)

tk.Label(root, text="______________________________________________________________").pack()

frame = tk.Frame(root)
frame.pack(pady=10)

# PLAINTEXT TIDAK LAGI ANGKA
tk.Label(frame, text="Plainteks:").grid(row=0, column=0, sticky="w", pady=8)
entry_plain = tk.Entry(frame, width=40)
entry_plain.grid(row=0, column=1, pady=8)

# e (public key) textbox
tk.Label(frame, text="e (public key):").grid(row=1, column=0, sticky="w", pady=8)
entry_e = tk.Entry(frame, width=40)
entry_e.grid(row=1, column=1, pady=8)
entry_e.insert(0, str(e))
entry_e.config(state="readonly")

# n (p*q) textbox
tk.Label(frame, text="n (p * q):").grid(row=2, column=0, sticky="w", pady=8)
entry_n = tk.Entry(frame, width=40)
entry_n.grid(row=2, column=1, pady=8)
entry_n.insert(0, str(n))
entry_n.config(state="readonly")

# Tombol
btn = tk.Button(root, text="Enkripsi", width=15, command=enkripsi)
btn.pack(pady=10)

# Ciphertext textbox
tk.Label(root, text="Cipherteks (heksadesimal):").pack()

entry_cipher = tk.Entry(root, width=50, font=("Arial", 12))
entry_cipher.pack(pady=5)
entry_cipher.config(state="readonly")

root.mainloop()

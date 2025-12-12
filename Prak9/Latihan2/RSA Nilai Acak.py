import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
import random
import math


# ============================================================
#              FUNGSI PEMBANTU RSA
# ============================================================

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True


def generate_random_prime():
    while True:
        num = random.randint(50, 200)
        if is_prime(num):
            return num


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def mod_inverse(e, phi):
    for d in range(1, phi):
        if (d * e) % phi == 1:
            return d
    return None


# ============================================================
#              LOGIKA GUI + RSA
# ============================================================

root = tk.Tk()
root.title("RSA Latihan 2 — Simple & Clean")
root.geometry("950x650")
root.configure(bg="white")

main = tk.Frame(root, bg="white", padx=20, pady=20)
main.pack(fill="both", expand=True)

# ================== TITLE ==================
title = tk.Label(main,
                 text="🔐 RSA ENKRIPSI — RANDOM PRIME (Simple Edition)",
                 font=("Segoe UI", 16, "bold"),
                 bg="white")
title.pack(pady=5)

# ================== INPUT PLAINTEXT ==================
frame_input = tk.Frame(main, bg="white")
frame_input.pack(fill="x", pady=10)

lbl_plain = tk.Label(frame_input, text="Plainteks:", font=("Segoe UI", 11), bg="white")
lbl_plain.grid(row=0, column=0, sticky="w")

entry_plain = tk.Entry(frame_input, width=40, font=("Segoe UI", 11))
entry_plain.grid(row=0, column=1, padx=10)


lbl_length = tk.Label(frame_input, text="Length: 0 chars | 0 bytes",
                      font=("Segoe UI", 9), bg="white")
lbl_length.grid(row=1, column=1, sticky="w")


def update_length(event=None):
    txt = entry_plain.get()
    lbl_length.config(text=f"Length: {len(txt)} chars | {len(txt.encode())} bytes")


entry_plain.bind("<KeyRelease>", update_length)

# ============================================================
#              VARIABEL RSA
# ============================================================
p = q = n = phi = e = d = None
cipher_list = []


# ============================================================
#              TOMBOL FUNGSI
# ============================================================

def generate_key():
    global p, q, n, phi, e, d

    debug_box.delete(1.0, tk.END)

    p = generate_random_prime()
    q = generate_random_prime()
    n = p * q
    phi = (p - 1) * (q - 1)

    # pilih e acak
    while True:
        e = random.randint(3, phi - 1)
        if gcd(e, phi) == 1:
            break

    d = mod_inverse(e, phi)

    debug_box.insert(tk.END, f"p = {p}\n")
    debug_box.insert(tk.END, f"q = {q}\n")
    debug_box.insert(tk.END, f"n = p*q = {n}\n")
    debug_box.insert(tk.END, f"φ(n) = {phi}\n")
    debug_box.insert(tk.END, f"e = {e}\n")
    debug_box.insert(tk.END, f"d = {d}\n\n")
    debug_box.insert(tk.END, f"Public key: ({e}, {n})\n")
    debug_box.insert(tk.END, f"Private key: ({d}, {n})\n")


def encrypt():
    global cipher_list
    txt = entry_plain.get()

    if not txt:
        messagebox.showerror("Error", "Plainteks tidak boleh kosong!")
        return

    if not n:
        messagebox.showerror("Error", "Generate key dulu!")
        return

    cipher_list = []
    debug_box.insert(tk.END, "\n---- ENKRIPSI ----\n")

    for ch in txt:
        m = ord(ch)
        c = pow(m, e, n)
        cipher_list.append(c)
        debug_box.insert(tk.END, f"{m}^{e} mod {n} = {c}\n")

    debug_box.insert(tk.END, f"\nCipher = {cipher_list}\n")

    hex_text = " ".join([hex(c)[2:].upper() for c in cipher_list])
    debug_box.insert(tk.END, "\nASCII : " + str([ord(c) for c in txt]) + "\n")
    debug_box.insert(tk.END, "HEX    : " + hex_text + "\n")


def decrypt():
    global cipher_list
    if not cipher_list:
        messagebox.showerror("Error", "Belum ada ciphertext!")
        return

    debug_box.insert(tk.END, "\n---- DEKRIPSI ----\n")

    hasil = ""
    for c in cipher_list:
        m = pow(c, d, n)
        hasil += chr(m)
        debug_box.insert(tk.END, f"{c}^{d} mod {n} = {m}\n")

    debug_box.insert(tk.END, f"\nHasil Dekripsi = {hasil}\n")


def copy_cipher():
    if cipher_list:
        cipher_str = " ".join(map(str, cipher_list))
        root.clipboard_clear()
        root.clipboard_append(cipher_str)
        messagebox.showinfo("Copied", "Cipher berhasil disalin")


def clear_log():
    debug_box.delete(1.0, tk.END)


def reset_all():
    global p, q, n, phi, e, d, cipher_list
    p = q = n = phi = e = d = None
    cipher_list = []
    entry_plain.delete(0, tk.END)
    update_length()
    debug_box.delete(1.0, tk.END)


def save_debug():
    file = filedialog.asksaveasfilename(defaultextension=".txt",
                                        filetypes=[("Text Files", "*.txt")])
    if file:
        with open(file, "w") as f:
            f.write(debug_box.get(1.0, tk.END))
        messagebox.showinfo("Saved", "Debug berhasil disimpan!")


# ============================================================
#              BUTTON AREA
# ============================================================

frame_btn = tk.Frame(main, bg="white")
frame_btn.pack(pady=5)

btn_key = tk.Button(frame_btn, text="Generate Key", width=15, command=generate_key)
btn_encrypt = tk.Button(frame_btn, text="Encrypt", width=15, command=encrypt)
btn_decrypt = tk.Button(frame_btn, text="Decrypt", width=15, command=decrypt)

btn_copy = tk.Button(frame_btn, text="Copy Cipher", width=15, command=copy_cipher)
btn_clear = tk.Button(frame_btn, text="Clear Log", width=15, command=clear_log)
btn_reset = tk.Button(frame_btn, text="Reset", width=15, command=reset_all)

btn_key.grid(row=0, column=0, padx=5)
btn_encrypt.grid(row=0, column=1, padx=5)
btn_decrypt.grid(row=0, column=2, padx=5)

btn_copy.grid(row=1, column=0, padx=5, pady=5)
btn_clear.grid(row=1, column=1, padx=5)
btn_reset.grid(row=1, column=2, padx=5)

btn_save = tk.Button(main, text="Save Debug to TXT", width=20, command=save_debug)
btn_save.pack(pady=5)

# ============================================================
#              DEBUG TEXTBOX
# ============================================================

lbl_debug = tk.Label(main, text="▶ Debug / Proses Perhitungan:",
                     font=("Segoe UI", 11, "bold"), bg="white")
lbl_debug.pack(anchor="w")

debug_box = scrolledtext.ScrolledText(main, width=120, height=20, font=("Consolas", 10))
debug_box.pack(pady=5)

root.mainloop()

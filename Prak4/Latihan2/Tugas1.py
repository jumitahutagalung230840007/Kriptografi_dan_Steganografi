import tkinter as tk
from tkinter import ttk, messagebox

# --- Fungsi Cipher ---
def substitusi_cipher(plaintext, aturan):
    ciphertext = ""
    for char in plaintext.upper():
        if char in aturan:
            ciphertext += aturan[char]
        else:
            ciphertext += char
    return ciphertext

def transposisi_cipher(teks, blok):
    teks = teks.replace(" ", "")
    hasil = ""
    for i in range(blok):
        hasil += teks[i::blok]
    return hasil


# --- Fungsi utama enkripsi ---
def enkripsi():
    plaintext = entry_plaintext.get().upper().strip()
    if not plaintext:
        messagebox.showwarning("Peringatan", "Masukkan plaintext terlebih dahulu!")
        return

    # Aturan substitusi (bisa dimodifikasi sesuai kebutuhan)
    aturan = {
        'U': 'K',
        'N': 'N',
        'I': 'I',
        'K': 'K',
        'A': 'B',
        'S': 'U',
        'T': 'T',
        'O': 'A',
        'H': 'H',
        'M': 'M'
    }

    hasil_substitusi = substitusi_cipher(plaintext, aturan)
    hasil_transposisi = transposisi_cipher(hasil_substitusi, 4)

    # Tampilkan hasil
    label_substitusi_hasil.config(text=hasil_substitusi)
    label_transposisi_hasil.config(text=hasil_transposisi)

    # Simpan hasil ke messagebox
    messagebox.showinfo("Hasil Enkripsi",
        f"Plaintext : {plaintext}\n"
        f"Substitusi Cipher : {hasil_substitusi}\n"
        f"Substitusi + Transposisi : {hasil_transposisi}"
    )


# --- Tampilan GUI ---
root = tk.Tk()
root.title("✨ Substitusi + Transposisi Cipher ✨")
root.geometry("580x450")
root.configure(bg="#EAE6F8")  # Warna lembut ungu muda

style = ttk.Style()
style.configure("TLabel", background="#EAE6F8", font=("Poppins", 11))
style.configure("TButton", font=("Poppins", 10, "bold"), padding=6)
style.configure("TEntry", padding=5)

# Judul
judul = tk.Label(root, text="🔐 PROGRAM ENKRIPSI CIPHER 🔐", font=("Poppins", 16, "bold"), bg="#EAE6F8", fg="#6A5ACD")
judul.pack(pady=15)

# Frame utama
frame = ttk.Frame(root)
frame.pack(pady=10)

# Input plaintext
ttk.Label(frame, text="Masukkan Plaintext:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
entry_plaintext = ttk.Entry(frame, width=40, font=("Poppins", 11))
entry_plaintext.grid(row=0, column=1, padx=10, pady=5)

# Tombol enkripsi
btn_enkripsi = ttk.Button(root, text="🔁 ENKRIPSI SEKARANG", command=enkripsi)
btn_enkripsi.pack(pady=15)

# Hasil substitusi
ttk.Label(root, text="Ciphertext (Substitusi Cipher):", font=("Poppins", 11, "bold"), foreground="#4B0082").pack(pady=(10,0))
label_substitusi_hasil = tk.Label(root, text="-", bg="#EAE6F8", fg="#2E2E2E", font=("Consolas", 11))
label_substitusi_hasil.pack()

# Hasil transposisi
ttk.Label(root, text="Ciphertext (Substitusi + Transposisi):", font=("Poppins", 11, "bold"), foreground="#4B0082").pack(pady=(10,0))
label_transposisi_hasil = tk.Label(root, text="-", bg="#EAE6F8", fg="#2E2E2E", font=("Consolas", 11))
label_transposisi_hasil.pack()

# Footer
footer = tk.Label(root, text="Made with 💜 using Python + Tkinter", font=("Poppins", 9, "italic"), bg="#EAE6F8", fg="#7D7D7D")
footer.pack(side="bottom", pady=10)

root.mainloop()

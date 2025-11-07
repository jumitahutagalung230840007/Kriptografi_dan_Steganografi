import tkinter as tk
from tkinter import ttk, messagebox


# ===============================================================
# CLASS VigenereCipher
# ===============================================================
class VigenereCipher:
    def __init__(self, key):
        self.key = key.upper()

    def _format_key(self, text):
        """Menyesuaikan panjang kunci dengan panjang teks"""
        key = self.key
        if len(key) < len(text):
            key = (key * ((len(text) // len(key)) + 1))[:len(text)]
        return key

    def _shift(self, char, key_char, mode="encrypt"):
        """Proses pergeseran huruf"""
        base = ord('A')
        char_val = ord(char) - base
        key_val = ord(key_char) - base

        if mode == "encrypt":
            return chr((char_val + key_val) % 26 + base)
        else:
            return chr((char_val - key_val + 26) % 26 + base)

    def encrypt(self, plaintext):
        plaintext = plaintext.replace(" ", "").upper()
        key = self._format_key(plaintext)

        detail = []
        detail.append("=== DETAIL PROSES ENKRIPSI ===")
        detail.append(f"Plaintext : {plaintext}")
        detail.append(f"Kunci     : {key}\n")

        ciphertext = ""
        for p, k in zip(plaintext, key):
            c = self._shift(p, k, "encrypt")
            detail.append(f"{p} + {k} -> ({ord(p)-65} + {ord(k)-65}) mod 26 = {ord(c)-65} -> {c}")
            ciphertext += c

        detail.append(f"\nCiphertext : {ciphertext}\n")
        return ciphertext, "\n".join(detail)

    def decrypt(self, ciphertext):
        ciphertext = ciphertext.replace(" ", "").upper()
        key = self._format_key(ciphertext)

        detail = []
        detail.append("=== DETAIL PROSES DEKRIPSI ===")
        detail.append(f"Ciphertext : {ciphertext}")
        detail.append(f"Kunci      : {key}\n")

        plaintext = ""
        for c, k in zip(ciphertext, key):
            p = self._shift(c, k, "decrypt")
            detail.append(f"{c} - {k} -> ({ord(c)-65} - {ord(k)-65}) mod 26 = {ord(p)-65} -> {p}")
            plaintext += p

        detail.append(f"\nPlaintext : {plaintext}\n")
        return plaintext, "\n".join(detail)


# ===============================================================
# CLASS GUI
# ===============================================================
class VigenereGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Vigenere Cipher - Praktikum 5")
        self.master.geometry("750x600")
        self.master.config(bg="#E6E6FA")

        # Judul
        ttk.Label(
            master, text="🔐 VIGENERE CIPHER ENKRIPSI & DEKRIPSI",
            font=("Segoe UI", 16, "bold"), background="#E6E6FA"
        ).pack(pady=10)

        # Frame Input
        frame_input = ttk.Frame(master)
        frame_input.pack(pady=10)

        ttk.Label(frame_input, text="Kunci:", font=("Segoe UI", 11)).grid(row=0, column=0, sticky="w")
        self.entry_key = ttk.Entry(frame_input, width=40)
        self.entry_key.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(frame_input, text="Teks:", font=("Segoe UI", 11)).grid(row=1, column=0, sticky="w")
        self.entry_text = ttk.Entry(frame_input, width=40)
        self.entry_text.grid(row=1, column=1, padx=10, pady=5)

        # Tombol Aksi
        frame_button = ttk.Frame(master)
        frame_button.pack(pady=5)

        self.btn_encrypt = ttk.Button(frame_button, text="🔒 Enkripsi", command=self.encrypt_text)
        self.btn_encrypt.grid(row=0, column=0, padx=10)

        self.btn_decrypt = ttk.Button(frame_button, text="🔓 Dekripsi", command=self.decrypt_text)
        self.btn_decrypt.grid(row=0, column=1, padx=10)

        self.btn_clear = ttk.Button(frame_button, text="🧹 Bersihkan", command=self.clear_output)
        self.btn_clear.grid(row=0, column=2, padx=10)

        # Hasil Output
        ttk.Label(master, text="Hasil & Detail Proses:", font=("Segoe UI", 11, "bold"),
                  background="#E6E6FA").pack(pady=5)

        self.text_output = tk.Text(master, height=20, width=85, wrap="word", font=("Consolas", 10))
        self.text_output.pack(padx=10, pady=5)
        self.text_output.insert("end", "Masukkan teks dan kunci, lalu pilih Enkripsi atau Dekripsi.\n")

    # -----------------------------------------------------------
    # Fungsi Enkripsi
    # -----------------------------------------------------------
    def encrypt_text(self):
        key = self.entry_key.get().strip()
        text = self.entry_text.get().strip()

        if not key or not text:
            messagebox.showwarning("Peringatan", "Kunci dan teks tidak boleh kosong!")
            return

        cipher = VigenereCipher(key)
        result, detail = cipher.encrypt(text)

        self.text_output.delete("1.0", "end")
        self.text_output.insert("end", detail)

    # -----------------------------------------------------------
    # Fungsi Dekripsi
    # -----------------------------------------------------------
    def decrypt_text(self):
        key = self.entry_key.get().strip()
        text = self.entry_text.get().strip()

        if not key or not text:
            messagebox.showwarning("Peringatan", "Kunci dan teks tidak boleh kosong!")
            return

        cipher = VigenereCipher(key)
        result, detail = cipher.decrypt(text)

        self.text_output.delete("1.0", "end")
        self.text_output.insert("end", detail)

    # -----------------------------------------------------------
    # Fungsi Bersihkan
    # -----------------------------------------------------------
    def clear_output(self):
        self.entry_text.delete(0, "end")
        self.text_output.delete("1.0", "end")
        self.text_output.insert("end", "Masukkan teks dan kunci, lalu pilih Enkripsi atau Dekripsi.\n")


# ===============================================================
# MAIN PROGRAM
# ===============================================================
if __name__ == "__main__":
    root = tk.Tk()
    app = VigenereGUI(root)
    root.mainloop()

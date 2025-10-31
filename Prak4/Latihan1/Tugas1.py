import tkinter as tk
from tkinter import ttk, messagebox

# ================= Helper Cipher =================
def substitusi_cipher(plaintext, aturan):
    out = ""
    for ch in plaintext.upper():
        if ch == " ":
            out += " "
        elif ch in aturan:
            out += aturan[ch]
        else:
            out += ch
    return out

def transposisi_cipher(teks, blok=4, pad_char="X"):
    # remove spaces, uppercase
    s = teks.replace(" ", "").upper()
    # pad supaya len % blok == 0
    rem = len(s) % blok
    if rem != 0:
        s += pad_char * (blok - rem)
    # baca per kolom: hasil = s[0::blok] + s[1::blok] + ...
    hasil = ""
    for i in range(blok):
        hasil += s[i::blok]
    return hasil, s  # kembalikan transposisi dan versi tanpa pad untuk grid

# ================= GUI =================
class CipherApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("✨ Substitusi + Transposisi Cipher (tkinter) ✨")
        self.configure(bg="#F3F0FF")
        self.geometry("820x600")
        self.resizable(False, False)

        self.aturan = {}  # dict substitusi

        self._make_widgets()

    def _make_widgets(self):
        header = tk.Label(self, text="🔐 Substitusi + Transposisi Cipher", 
                          font=("Segoe UI", 18, "bold"), bg="#F3F0FF", fg="#4B0082")
        header.pack(pady=(12,6))

        top_frame = ttk.Frame(self)
        top_frame.pack(fill="x", padx=18)

        # ===== Aturan Substitusi =====
        aturan_box = ttk.LabelFrame(top_frame, text="Aturan Substitusi (A=B)", padding=12)
        aturan_box.grid(row=0, column=0, sticky="nw", padx=(0,12), pady=6)

        tk.Label(aturan_box, text="Masukkan aturan (format A=B):").grid(row=0, column=0, sticky="w")
        self.entry_aturan = ttk.Entry(aturan_box, width=10, font=("Consolas", 11))
        self.entry_aturan.grid(row=0, column=1, padx=6)
        btn_tambah = ttk.Button(aturan_box, text="Tambah", command=self.tambah_aturan)
        btn_tambah.grid(row=0, column=2, padx=6)

        btn_hapus = ttk.Button(aturan_box, text="Hapus terpilih", command=self.hapus_aturan)
        btn_hapus.grid(row=1, column=2, pady=(6,0))

        self.listbox_aturan = tk.Listbox(aturan_box, height=8, width=22, font=("Consolas", 11))
        self.listbox_aturan.grid(row=1, column=0, columnspan=2, pady=(6,0), sticky="w")

        # ===== Plaintext & Controls =====
        kontrol_box = ttk.LabelFrame(top_frame, text="Plaintext & Kontrol", padding=12)
        kontrol_box.grid(row=0, column=1, sticky="ne", pady=6)

        tk.Label(kontrol_box, text="Plaintext:").grid(row=0, column=0, sticky="w")
        self.entry_plain = ttk.Entry(kontrol_box, width=48, font=("Segoe UI", 11))
        self.entry_plain.insert(0, "UNIKA SANTO THOMAS")
        self.entry_plain.grid(row=0, column=1, padx=6, pady=3)

        tk.Label(kontrol_box, text="Blok Transposisi:").grid(row=1, column=0, sticky="w", pady=(6,0))
        self.spin_blok = tk.Spinbox(kontrol_box, from_=2, to=10, width=4, font=("Consolas", 10))
        self.spin_blok.grid(row=1, column=1, sticky="w", padx=6, pady=(6,0))

        btn_encrypt = ttk.Button(kontrol_box, text="🔁 Encrypt", command=self.encrypt_all)
        btn_encrypt.grid(row=2, column=0, columnspan=2, pady=(10,0), sticky="ew")

        btn_reset = ttk.Button(kontrol_box, text="🔄 Reset", command=self.reset_all)
        btn_reset.grid(row=3, column=0, columnspan=2, pady=(8,0), sticky="ew")

        # ===== Hasil =====
        hasil_frame = ttk.Frame(self)
        hasil_frame.pack(fill="both", padx=18, pady=(10,12))

        # Substitusi hasil
        sub_frame = ttk.LabelFrame(hasil_frame, text="Ciphertext (Substitusi)", padding=10)
        sub_frame.grid(row=0, column=0, padx=(0,10), sticky="n")

        self.txt_sub = tk.Text(sub_frame, width=48, height=4, wrap="word", font=("Consolas", 11))
        self.txt_sub.pack()
        sub_btn_frame = ttk.Frame(sub_frame)
        sub_btn_frame.pack(fill="x", pady=(6,0))
        ttk.Button(sub_btn_frame, text="Copy", command=lambda: self._copy_text(self.txt_sub)).pack(side="left")
        ttk.Button(sub_btn_frame, text="Clear", command=lambda: self._clear_text(self.txt_sub)).pack(side="left", padx=6)

        # Substitusi+Transposisi hasil
        trans_frame = ttk.LabelFrame(hasil_frame, text="Ciphertext (Substitusi + Transposisi)", padding=10)
        trans_frame.grid(row=0, column=1, sticky="n")

        self.txt_trans = tk.Text(trans_frame, width=36, height=4, wrap="word", font=("Consolas", 11))
        self.txt_trans.pack()
        trans_btn_frame = ttk.Frame(trans_frame)
        trans_btn_frame.pack(fill="x", pady=(6,0))
        ttk.Button(trans_btn_frame, text="Copy", command=lambda: self._copy_text(self.txt_trans)).pack(side="left")
        ttk.Button(trans_btn_frame, text="Clear", command=lambda: self._clear_text(self.txt_trans)).pack(side="left", padx=6)

        # Grid blok
        grid_frame = ttk.LabelFrame(self, text="Visualisasi 4-Blok (Grid)", padding=10)
        grid_frame.pack(padx=18, pady=(6,12), fill="x")
        self.grid_frame_inner = ttk.Frame(grid_frame)
        self.grid_frame_inner.pack()

        # Footer
        foot = tk.Label(self, text="Made with ❤️  — Substitution + Transposition (pad dengan 'X' bila perlu)",
                        font=("Segoe UI", 9), bg="#F3F0FF", fg="#6d6a6a")
        foot.pack(side="bottom", pady=8)

    # ===== Actions =====
    def tambah_aturan(self):
        s = self.entry_aturan.get().strip().upper()
        if not s:
            messagebox.showwarning("Peringatan", "Masukkan aturan terlebih dahulu (contoh A=B).")
            return
        if '=' not in s or len(s) != 3:
            messagebox.showerror("Format Salah", "Gunakan format A=B (satu huruf = satu huruf).")
            return
        a, b = s.split('=')
        if not (a.isalpha() and b.isalpha() and len(a)==1 and len(b)==1):
            messagebox.showerror("Format Salah", "Gunakan huruf tunggal (A=B).")
            return
        self.aturan[a] = b
        self._refresh_listbox()
        self.entry_aturan.delete(0, 'end')

    def hapus_aturan(self):
        sel = self.listbox_aturan.curselection()
        if not sel:
            messagebox.showwarning("Peringatan", "Pilih aturan di daftar untuk dihapus.")
            return
        item = self.listbox_aturan.get(sel[0])
        k = item.split(" → ")[0]
        if k in self.aturan:
            del self.aturan[k]
        self._refresh_listbox()

    def _refresh_listbox(self):
        self.listbox_aturan.delete(0, 'end')
        for k, v in sorted(self.aturan.items()):
            self.listbox_aturan.insert('end', f"{k} → {v}")

    def encrypt_all(self):
        if not self.aturan:
            if not messagebox.askyesno("Konfirmasi", "Belum ada aturan substitusi. Lanjutkan tanpa aturan?"):
                return
        plaintext = self.entry_plain.get().strip()
        if plaintext == "":
            messagebox.showwarning("Peringatan", "Masukkan plaintext.")
            return
        try:
            blok = int(self.spin_blok.get())
            if blok < 2:
                raise ValueError
        except Exception:
            messagebox.showerror("Error", "Nilai blok harus angka >= 2.")
            return

        # 1) substitusi (spasi dipertahankan)
        hasil_sub = substitusi_cipher(plaintext, self.aturan)
        # 2) transposisi
        hasil_transposisi, ohne_pad = transposisi_cipher(hasil_sub, blok=blok, pad_char="X")

        # tampil di text widgets
        self._set_text(self.txt_sub, hasil_sub)
        self._set_text(self.txt_trans, hasil_transposisi)

        # visualisasi grid: tampilkan matriks kolom=blok dengan baris = len(ohne_pad)/blok (+pad jika ada)
        self._draw_grid(ohne_pad, blok)

    def reset_all(self):
        if messagebox.askyesno("Reset", "Reset semua input dan aturan?"):
            self.aturan.clear()
            self._refresh_listbox()
            self.entry_plain.delete(0, 'end')
            self.entry_plain.insert(0, "UNIKA SANTO THOMAS")
            self._clear_text(self.txt_sub)
            self._clear_text(self.txt_trans)
            for wid in self.grid_frame_inner.winfo_children():
                wid.destroy()

    # ===== Utilities =====
    def _set_text(self, widget, txt):
        widget.configure(state="normal")
        widget.delete("1.0", "end")
        widget.insert("1.0", txt)
        widget.configure(state="disabled")

    def _clear_text(self, widget):
        widget.configure(state="normal")
        widget.delete("1.0", "end")
        widget.configure(state="disabled")

    def _copy_text(self, widget):
        widget.configure(state="normal")
        txt = widget.get("1.0", "end").strip()
        widget.configure(state="disabled")
        if txt:
            self.clipboard_clear()
            self.clipboard_append(txt)
            messagebox.showinfo("Copied", "Teks berhasil disalin ke clipboard.")
        else:
            messagebox.showwarning("Kosong", "Tidak ada teks untuk disalin.")

    def _draw_grid(self, s_no_spaces, blok):
        # clear
        for wid in self.grid_frame_inner.winfo_children():
            wid.destroy()
        s = s_no_spaces.upper()
        # pad display to full rectangle
        rem = len(s) % blok
        pad = 0 if rem==0 else (blok-rem)
        display = s + ("X"*pad)
        rows = len(display) // blok

        # buat grid rows x blok; isi by row like:
        # row0 = display[0:blok], row1 = display[blok:2*blok], ...
        for r in range(rows):
            for c in range(blok):
                ch = display[r*blok + c]
                lbl = tk.Label(self.grid_frame_inner, text=ch, width=4, height=2,
                               font=("Consolas", 12, "bold"),
                               bg="#FFFFFF", relief="ridge", borderwidth=1)
                lbl.grid(row=r, column=c, padx=2, pady=2)

# ============ Run app ============
if __name__ == "__main__":
    app = CipherApp()
    app.mainloop()

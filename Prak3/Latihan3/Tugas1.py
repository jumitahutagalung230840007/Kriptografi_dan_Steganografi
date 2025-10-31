import itertools
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# ===== Helper =====
def faktorial(x):
    if x == 0 or x == 1:
        return 1
    hasil = 1
    for i in range(2, x + 1):
        hasil *= i
    return hasil

def kombinasi_count(n, r):
    if r > n:
        return 0
    return faktorial(n) // (faktorial(r) * faktorial(n - r))

# ===== GUI App =====
class KombinasiApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("✨ Program Kombinasi (Inisial Huruf) ✨")
        self.geometry("820x600")
        self.configure(bg="#F6F5FF")
        self._build_ui()

    def _build_ui(self):
        header = tk.Label(self, text="🔢 Kombinasi dengan Inisial Huruf",
                          font=("Segoe UI", 18, "bold"), bg="#F6F5FF", fg="#5B2C6F")
        header.pack(pady=12)

        main = ttk.Frame(self)
        main.pack(fill="both", expand=True, padx=16, pady=8)

        left = ttk.Frame(main)
        left.grid(row=0, column=0, sticky="nw", padx=(0,12))

        # Input n,r
        ttk.Label(left, text="Jumlah total objek (n):").grid(row=0, column=0, sticky="w")
        self.spin_n = ttk.Spinbox(left, from_=1, to=26, width=6, font=("Consolas", 11))
        self.spin_n.set(5)
        self.spin_n.grid(row=1, column=0, pady=6, sticky="w")

        ttk.Label(left, text="Jumlah dipilih (r):").grid(row=2, column=0, sticky="w", pady=(8,0))
        self.spin_r = ttk.Spinbox(left, from_=1, to=26, width=6, font=("Consolas", 11))
        self.spin_r.set(3)
        self.spin_r.grid(row=3, column=0, pady=6, sticky="w")

        # Custom letters
        ttk.Label(left, text="Gunakan huruf kustom? (pisah spasi)").grid(row=4, column=0, sticky="w", pady=(8,0))
        self.entry_custom = ttk.Entry(left, width=26, font=("Consolas", 11))
        self.entry_custom.grid(row=5, column=0, pady=6)
        ttk.Label(left, text="(Contoh: A B C D E atau kosong untuk A..)").grid(row=6, column=0, sticky="w")

        # Options
        ttk.Label(left, text="Opsi tampilan:").grid(row=7, column=0, sticky="w", pady=(8,0))
        self.show_mode = tk.StringVar(value="all")
        ttk.Radiobutton(left, text="Tampilkan semua (jika wajar)", variable=self.show_mode, value="all").grid(row=8, column=0, sticky="w")
        ttk.Radiobutton(left, text="Tampilkan ringkasan + preview (100)", variable=self.show_mode, value="preview").grid(row=9, column=0, sticky="w")

        # Buttons
        ttk.Button(left, text="▶ Hitung & Tampilkan", command=self.run_kombinasi).grid(row=10, column=0, pady=(12,6), sticky="ew")
        ttk.Button(left, text="💾 Ekspor .txt", command=self.export_txt).grid(row=11, column=0, pady=(6,0), sticky="ew")

        # Right: results
        right = ttk.Frame(main)
        right.grid(row=0, column=1, sticky="nsew")
        main.columnconfigure(1, weight=1)

        info_frame = ttk.Frame(right)
        info_frame.pack(fill="x")
        self.lbl_count = ttk.Label(info_frame, text="Jumlah kombinasi: -", font=("Segoe UI", 11, "bold"))
        self.lbl_count.pack(anchor="w", pady=(0,6))

        self.txt = tk.Text(right, wrap="none", font=("Consolas", 11))
        self.txt.pack(fill="both", expand=True)
        ysb = ttk.Scrollbar(right, orient="vertical", command=self.txt.yview)
        self.txt.configure(yscrollcommand=ysb.set)
        ysb.pack(side="right", fill="y")
        xsb = ttk.Scrollbar(right, orient="horizontal", command=self.txt.xview)
        self.txt.configure(xscrollcommand=xsb.set)
        xsb.pack(fill="x")

        btn_row = ttk.Frame(right)
        btn_row.pack(fill="x", pady=8)
        ttk.Button(btn_row, text="Copy Hasil", command=self.copy_result).pack(side="left")
        ttk.Button(btn_row, text="Clear", command=self.clear_result).pack(side="left", padx=8)

        footer = tk.Label(self, text="Made with ❤️ — Kombinasi & Daftar Inisial Huruf", font=("Segoe UI", 9), bg="#F6F5FF", fg="#6d6a6a")
        footer.pack(side="bottom", pady=8)

    def _get_letters(self, n):
        custom = self.entry_custom.get().strip()
        if custom:
            parts = custom.split()
            if len(parts) < n:
                messagebox.showwarning("Peringatan", f"Kamu memasukkan {len(parts)} huruf kustom, namun n={n}. Menggunakan {len(parts)} sebagai n.")
            return parts[:n]
        else:
            # default A..Z
            return [chr(65 + i) for i in range(n)]

    def run_kombinasi(self):
        try:
            n = int(self.spin_n.get())
            r = int(self.spin_r.get())
        except Exception:
            messagebox.showerror("Error", "Masukkan nilai n dan r valid (angka).")
            return
        if n < 1 or r < 1:
            messagebox.showerror("Error", "n dan r harus >= 1.")
            return
        letters = self._get_letters(n)
        n_used = len(letters)
        if r > n_used:
            messagebox.showerror("Error", f"r ({r}) tidak boleh > jumlah huruf ({n_used}).")
            return

        total = kombinasi_count(n_used, r)
        self.lbl_count.config(text=f"Jumlah kombinasi C({n_used}, {r}) = {total:,}")

        self.txt.configure(state="normal")
        self.txt.delete("1.0", "end")

        # prepare combinations
        combos = itertools.combinations(letters, r)
        mode = self.show_mode.get()
        if mode == "all" and total > 50000:
            proceed = messagebox.askyesno("Peringatan", f"Ada {total:,} kombinasi — menampilkan semua bisa berat. Tampilkan 1000 teratas?")
            if not proceed:
                self.txt.insert("end", "(Penampilan dibatalkan oleh pengguna)\n")
                self.txt.configure(state="disabled")
                return
            limit = 1000
        elif mode == "preview":
            limit = min(total, 100)
        else:
            limit = total

        for i, combo in enumerate(itertools.islice(combos, limit), start=1):
            self.txt.insert("end", f"{i:>4}. " + ", ".join(combo) + "\n")

        if total > limit:
            self.txt.insert("end", f"\n... (menampilkan {limit} dari {total:,})\n")

        self.txt.configure(state="disabled")

    def copy_result(self):
        txt = self.txt.get("1.0", "end").strip()
        if not txt:
            messagebox.showwarning("Kosong", "Tidak ada hasil untuk disalin.")
            return
        self.clipboard_clear()
        self.clipboard_append(txt)
        messagebox.showinfo("Copied", "Hasil berhasil disalin ke clipboard.")

    def clear_result(self):
        self.txt.configure(state="normal")
        self.txt.delete("1.0", "end")
        self.lbl_count.config(text="Jumlah kombinasi: -")
        self.txt.configure(state="disabled")

    def export_txt(self):
        txt = self.txt.get("1.0", "end").strip()
        if not txt:
            messagebox.showwarning("Kosong", "Tidak ada hasil untuk diekspor. Jalankan dulu.")
            return
        fn = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files","*.txt")])
        if not fn:
            return
        with open(fn, "w", encoding="utf-8") as f:
            f.write(txt)
        messagebox.showinfo("Sukses", f"Hasil diekspor ke:\n{fn}")

if __name__ == "__main__":
    app = KombinasiApp()
    app.mainloop()

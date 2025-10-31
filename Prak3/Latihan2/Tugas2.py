import itertools
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# ---------- Fungsi logika ----------
def generate_penataan(n, r):
    buku = [f"B{i+1}" for i in range(n)]
    rak = [f"Rak{j+1}" for j in range(r)]
    for product in itertools.product(rak, repeat=n):
        yield [f"{buku[j]} -> {product[j]}" for j in range(n)]

# ---------- GUI ----------
class PenataanApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("📚 Penataan Buku di Rak — Visual")
        self.geometry("880x640")
        self.configure(bg="#FBFAFF")
        self._build_ui()

    def _build_ui(self):
        header = tk.Label(self, text="📚 PROGRAM PENATAAN BUKU DI RAK", 
                          font=("Segoe UI", 18, "bold"), bg="#FBFAFF", fg="#4B0082")
        header.pack(pady=(12,6))

        container = ttk.Frame(self)
        container.pack(fill="both", expand=True, padx=16, pady=10)

        left = ttk.Frame(container)
        left.grid(row=0, column=0, sticky="nw", padx=(0,12))

        ttk.Label(left, text="Masukkan jumlah buku (n):").grid(row=0, column=0, sticky="w")
        self.ent_n = ttk.Spinbox(left, from_=1, to=12, width=6, font=("Consolas", 11))
        self.ent_n.set(3)
        self.ent_n.grid(row=1, column=0, pady=6, sticky="w")

        ttk.Label(left, text="Masukkan jumlah rak (r):").grid(row=2, column=0, sticky="w", pady=(8,0))
        self.ent_r = ttk.Spinbox(left, from_=1, to=8, width=6, font=("Consolas", 11))
        self.ent_r.set(2)
        self.ent_r.grid(row=3, column=0, pady=6, sticky="w")

        ttk.Label(left, text="Pilihan tampilan:").grid(row=4, column=0, sticky="w", pady=(8,0))
        self.show_mode = tk.StringVar(value="full")
        ttk.Radiobutton(left, text="Tampilkan semua (jika jumlah wajar)", variable=self.show_mode, value="full").grid(row=5, column=0, sticky="w")
        ttk.Radiobutton(left, text="Tampilkan ringkasan + preview", variable=self.show_mode, value="preview").grid(row=6, column=0, sticky="w")
        ttk.Label(left, text="(Preview = 100 teratas)").grid(row=7, column=0, sticky="w", pady=(0,6))

        btn_frame = ttk.Frame(left)
        btn_frame.grid(row=8, column=0, pady=(10,0), sticky="ew")
        ttk.Button(btn_frame, text="▶ Generate", command=self.on_generate).grid(row=0, column=0, padx=(0,6))
        ttk.Button(btn_frame, text="✖ Clear", command=self.clear_result).grid(row=0, column=1)

        ttk.Button(left, text="💾 Export .txt", command=self.export_txt).grid(row=9, column=0, pady=(12,0), sticky="ew")

        # Right: hasil
        right = ttk.Frame(container)
        right.grid(row=0, column=1, sticky="nsew")
        container.columnconfigure(1, weight=1)

        top_info = ttk.Frame(right)
        top_info.pack(fill="x")
        self.lbl_count = ttk.Label(top_info, text="Jumlah total cara: -", font=("Segoe UI", 11, "bold"))
        self.lbl_count.pack(anchor="w", pady=(0,6))

        # text area with scrollbar
        text_frame = ttk.Frame(right)
        text_frame.pack(fill="both", expand=True)
        self.txt = tk.Text(text_frame, wrap="none", font=("Consolas", 11))
        self.txt.pack(side="left", fill="both", expand=True)
        ysb = ttk.Scrollbar(text_frame, orient="vertical", command=self.txt.yview)
        self.txt.configure(yscrollcommand=ysb.set)
        ysb.pack(side="right", fill="y")
        xsb = ttk.Scrollbar(right, orient="horizontal", command=self.txt.xview)
        self.txt.configure(xscrollcommand=xsb.set)
        xsb.pack(fill="x")

        # footer
        footer = tk.Label(self, text="Made with ❤️  — menampilkan kombinasi penempatan buku", 
                          font=("Segoe UI", 9), bg="#FBFAFF", fg="#6d6a6a")
        footer.pack(side="bottom", pady=8)

    def on_generate(self):
        try:
            n = int(self.ent_n.get())
            r = int(self.ent_r.get())
        except Exception:
            messagebox.showerror("Input Error", "Masukkan nilai n dan r yang valid (angka).")
            return
        # hitung jumlah total cara = r^n
        total = r ** n
        self.lbl_count.config(text=f"Jumlah total cara: {total:,}")

        self.txt.configure(state="normal")
        self.txt.delete("1.0", "end")

        mode = self.show_mode.get()
        gen = generate_penataan(n, r)

        # safety limit untuk tampil
        if mode == "full":
            if total > 20000:
                proceed = messagebox.askyesno("Peringatan", 
                    f"Ada {total:,} cara — menampilkan semua bisa sangat lama/makan memori.\nTampilkan 1000 teratas saja?")
                if not proceed:
                    self.txt.insert("end", "Tampilan dibatalkan oleh pengguna.\n")
                    self.txt.configure(state="disabled")
                    return
                limit = 1000
            else:
                limit = total
        else:
            limit = min(total, 100)

        for i, penataan in enumerate(itertools.islice(gen, limit), start=1):
            self.txt.insert("end", f"Cara {i:>6}: " + ", ".join(penataan) + "\n")

        if total > limit:
            self.txt.insert("end", f"\n... (menampilkan {limit} dari {total:,} total)\n")

        self.txt.configure(state="disabled")

    def clear_result(self):
        self.txt.configure(state="normal")
        self.txt.delete("1.0", "end")
        self.lbl_count.config(text="Jumlah total cara: -")
        self.txt.configure(state="disabled")

    def export_txt(self):
        try:
            n = int(self.ent_n.get())
            r = int(self.ent_r.get())
        except Exception:
            messagebox.showerror("Input Error", "Masukkan nilai n dan r yang valid (angka).")
            return
        total = r ** n
        if total > 2000000:
            if not messagebox.askyesno("Peringatan", "Jumlah sangat besar — ekspor mungkin memakan waktu. Lanjutkan?"):
                return

        fn = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files","*.txt")], title="Simpan hasil ke")
        if not fn:
            return

        # tulis ke file streaming (agar hemat memori)
        with open(fn, "w", encoding="utf-8") as f:
            f.write(f"Penataan buku: n={n}, r={r}\n")
            f.write(f"Jumlah total cara: {total}\n\n")
            buku = [f"B{i+1}" for i in range(n)]
            rak = [f"Rak{j+1}" for j in range(r)]
            for idx, prod in enumerate(itertools.product(rak, repeat=n), start=1):
                hasil = [f"{buku[j]} -> {prod[j]}" for j in range(n)]
                f.write(f"Cara {idx}: {', '.join(hasil)}\n")

        messagebox.showinfo("Sukses", f"Hasil berhasil diekspor ke:\n{fn}")

if __name__ == "__main__":
    app = PenataanApp()
    app.mainloop()

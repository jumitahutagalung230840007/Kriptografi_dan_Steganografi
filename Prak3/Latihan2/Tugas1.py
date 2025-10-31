import tkinter as tk
from tkinter import ttk, messagebox
import itertools

# ===== Permutation functions (original) =====
def permutasi_menyeluruh(data):
    return list(itertools.permutations(data))

def permutasi_sebagian(data, k):
    return list(itertools.permutations(data, k))

def permutasi_keliling(data):
    if len(data) <= 1:
        return [data]
    pertama = data[0]
    sisa = list(itertools.permutations(data[1:]))
    return [[pertama] + list(p) for p in sisa]

def permutasi_berkelompok(grup):
    hasil = [[]]
    for kelompok in grup:
        hasil_baru = []
        for h in hasil:
            for perm in itertools.permutations(kelompok):
                hasil_baru.append(h + list(perm))
        hasil = hasil_baru
    return hasil

# ===== GUI App =====
class PermApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("✨ Permutasi Interaktif ✨")
        self.geometry("820x600")
        self.configure(bg="#F8F7FF")
        self._build_ui()

    def _build_ui(self):
        # Header
        header = tk.Label(self, text="🔁 PROGRAM PERMUTASI (Interaktif)", 
                          font=("Segoe UI", 18, "bold"), bg="#F8F7FF", fg="#4B0082")
        header.pack(pady=12)

        main = ttk.Frame(self)
        main.pack(fill="both", expand=True, padx=16, pady=8)

        # Left: pilihan & input
        left = ttk.Frame(main)
        left.grid(row=0, column=0, sticky="n")

        ttk.Label(left, text="Pilih Jenis Permutasi:", font=("Segoe UI", 11)).grid(row=0, column=0, sticky="w")
        self.jenis = tk.StringVar(value="1")
        options = [("1 - Menyeluruh", "1"), ("2 - Sebagian", "2"),
                   ("3 - Keliling", "3"), ("4 - Berkelompok", "4")]
        for i, (txt, val) in enumerate(options):
            ttk.Radiobutton(left, text=txt, variable=self.jenis, value=val, command=self._on_mode_change).grid(row=1+i, column=0, sticky="w", pady=2)

        # input elemen single-line (for mode 1-3)
        ttk.Label(left, text="Elemen (pisah spasi):", font=("Segoe UI", 10)).grid(row=6, column=0, sticky="w", pady=(10,0))
        self.entry_elemen = ttk.Entry(left, width=32, font=("Consolas", 11))
        self.entry_elemen.grid(row=7, column=0, pady=6)

        # input k (for permutasi sebagian)
        self.k_frame = ttk.Frame(left)
        self.k_frame.grid(row=8, column=0, sticky="w")
        ttk.Label(self.k_frame, text="k (untuk Sebagian):").grid(row=0, column=0, sticky="w")
        self.spin_k = tk.Spinbox(self.k_frame, from_=1, to=20, width=6, font=("Consolas", 10))
        self.spin_k.grid(row=0, column=1, padx=6)

        # kelompok input (for mode 4)
        ttk.Label(left, text="(Untuk Berkelompok) - masukkan jumlah kelompok:").grid(row=9, column=0, sticky="w", pady=(12,0))
        self.btn_group_input = ttk.Button(left, text="Masukkan Kelompok...", command=self._prompt_groups)
        self.btn_group_input.grid(row=10, column=0, pady=6, sticky="w")

        # Buttons
        ttk.Button(left, text="▶ Jalankan Permutasi", command=self._run_permutasi).grid(row=12, column=0, pady=(12,0), sticky="ew")
        ttk.Button(left, text="✖ Bersihkan Hasil", command=self._clear_result).grid(row=13, column=0, pady=8, sticky="ew")

        # Right: hasil
        right = ttk.Frame(main)
        right.grid(row=0, column=1, padx=(16,0), sticky="nsew")
        main.columnconfigure(1, weight=1)

        ttk.Label(right, text="Hasil Permutasi:", font=("Segoe UI", 11)).pack(anchor="w")
        self.txt_result = tk.Text(right, width=60, height=24, font=("Consolas", 11), wrap="none")
        self.txt_result.pack(fill="both", expand=True)
        # scrollbar
        ysb = ttk.Scrollbar(right, orient="vertical", command=self.txt_result.yview)
        self.txt_result.configure(yscrollcommand=ysb.set)
        ysb.pack(side="right", fill="y")

        # footer note
        footer = tk.Label(self, text="Made with ❤️  — Permutasi Menyeluruh/Sebagian/Keliling/Berkelompok",
                          font=("Segoe UI", 9), bg="#F8F7FF", fg="#6d6a6a")
        footer.pack(side="bottom", pady=8)

        # state
        self.groups = None
        self._on_mode_change()

    def _on_mode_change(self):
        mode = self.jenis.get()
        if mode == "2":
            self.k_frame.grid()
        else:
            self.k_frame.grid_remove()

    def _prompt_groups(self):
        # popup untuk input kelompok: user memasukkan N baris (setiap baris grup), finish dengan OK
        popup = tk.Toplevel(self)
        popup.title("Input Kelompok")
        popup.geometry("480x320")
        ttk.Label(popup, text="Masukkan setiap kelompok di baris baru (pisah elemen dengan spasi):").pack(anchor="w", padx=12, pady=8)
        txt = tk.Text(popup, width=56, height=12, font=("Consolas", 11))
        txt.pack(padx=12)
        def ok():
            raw = txt.get("1.0","end").strip()
            if not raw:
                messagebox.showwarning("Peringatan", "Masukkan minimal satu kelompok.")
                return
            lines = [line.strip().split() for line in raw.splitlines() if line.strip()]
            self.groups = lines
            popup.destroy()
            messagebox.showinfo("Sukses", f"{len(lines)} kelompok disimpan.")
        ttk.Button(popup, text="OK", command=ok).pack(pady=8)
        ttk.Button(popup, text="Batal", command=popup.destroy).pack()

    def _run_permutasi(self):
        mode = self.jenis.get()
        self.txt_result.configure(state="normal")
        self.txt_result.delete("1.0", "end")

        try:
            if mode in ("1","2","3"):
                raw = self.entry_elemen.get().strip()
                if not raw:
                    messagebox.showwarning("Peringatan", "Masukkan elemen (pisahkan dengan spasi).")
                    return
                data = raw.split()
                if mode == "1":
                    hasil = permutasi_menyeluruh(data)
                    self._print_permutations(hasil, label="Permutasi Menyeluruh")
                elif mode == "2":
                    k = int(self.spin_k.get())
                    if k < 1 or k > len(data):
                        messagebox.showerror("Error", "k harus antara 1 dan jumlah elemen.")
                        return
                    hasil = permutasi_sebagian(data, k)
                    self._print_permutations(hasil, label=f"Permutasi Sebagian (k={k})")
                else:  # mode 3
                    hasil = permutasi_keliling(data)
                    self._print_permutations(hasil, label="Permutasi Keliling")
            else:  # mode 4
                if not self.groups:
                    messagebox.showwarning("Peringatan", "Masukkan kelompok dulu lewat 'Masukkan Kelompok...'.")
                    return
                hasil = permutasi_berkelompok(self.groups)
                self._print_permutations(hasil, label=f"Permutasi Berkelompok ({len(self.groups)} kelompok)")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            self.txt_result.configure(state="disabled")

    def _print_permutations(self, hasil, label="Hasil"):
        # tampil header
        total = len(hasil)
        header = f"{label} — Total: {total}\n\n"
        self.txt_result.insert("end", header)
        # batasi output kalau sangat besar: tanya user
        if total > 10000:
            proceed = messagebox.askyesno("Peringatan", f"Ada {total} hasil — menampilkan semua mungkin lama. Tampilkan 1000 teratas?")
            if not proceed:
                self.txt_result.insert("end", "(Menampilkan dibatasi — tidak ada yang ditampilkan.)\n")
                return
            limit = 1000
        else:
            limit = total
        for i, p in enumerate(hasil[:limit], start=1):
            # format output rapi: jika tuple/or list, gabung dengan spasi
            if isinstance(p, (tuple, list)):
                line = f"{i:>5}. " + ", ".join(map(str, p)) + "\n"
            else:
                line = f"{i:>5}. {p}\n"
            self.txt_result.insert("end", line)
        if total > limit:
            self.txt_result.insert("end", f"\n... (menampilkan {limit} dari {total})\n")

    def _clear_result(self):
        self.txt_result.configure(state="normal")
        self.txt_result.delete("1.0", "end")
        self.txt_result.configure(state="disabled")

if __name__ == "__main__":
    app = PermApp()
    app.mainloop()

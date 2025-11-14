import tkinter as tk
from tkinter import messagebox, ttk

# === Fungsi Konversi ===
def konversi_biner():
    biner = entry_biner.get().strip()
    if not biner:
        messagebox.showwarning("Peringatan", "Masukkan bilangan biner terlebih dahulu!")
        return
    try:
        # Konversi
        desimal = int(biner, 2)
        heksa = hex(desimal).upper().replace("0X", "")
        # Tampilkan hasil
        label_hasil_desimal_val.config(text=str(desimal))
        label_hasil_heksa_val.config(text=heksa)
    except ValueError:
        messagebox.showerror("Error", "Input bukan bilangan biner yang valid! Gunakan hanya 0 dan 1.")

# Fungsi reset input
def reset():
    entry_biner.delete(0, tk.END)
    label_hasil_desimal_val.config(text="-")
    label_hasil_heksa_val.config(text="-")

# === GUI ===
root = tk.Tk()
root.title("Konversi Bilangan Biner ke Desimal & Heksadesimal")
root.geometry("460x400")
root.config(bg="#E9F0FB")

# ===== Frame utama =====
frame_main = tk.Frame(root, bg="#FFFFFF", bd=3, relief="groove")
frame_main.place(relx=0.5, rely=0.5, anchor="center", width=420, height=360)

# ===== Judul =====
judul = tk.Label(frame_main, text="💡 Konversi Biner ke Desimal & Heksadesimal", 
                 bg="#FFFFFF", fg="#333", font=("Segoe UI", 14, "bold"))
judul.pack(pady=15)

# ===== Input =====
label_biner = tk.Label(frame_main, text="Masukkan Bilangan Biner:", bg="#FFFFFF", font=("Segoe UI", 11))
label_biner.pack(pady=(10, 0))

entry_biner = tk.Entry(frame_main, width=25, font=("Consolas", 14), justify="center", bg="#F3F7FA", relief="flat")
entry_biner.pack(pady=5, ipady=5)

# ===== Tombol =====
frame_button = tk.Frame(frame_main, bg="#FFFFFF")
frame_button.pack(pady=15)

btn_konversi = tk.Button(frame_button, text="Konversi", command=konversi_biner,
                         bg="#4CAF50", fg="white", font=("Segoe UI", 11, "bold"), width=12, relief="flat")
btn_konversi.grid(row=0, column=0, padx=5)

btn_reset = tk.Button(frame_button, text="Reset", command=reset,
                      bg="#E53935", fg="white", font=("Segoe UI", 11, "bold"), width=12, relief="flat")
btn_reset.grid(row=0, column=1, padx=5)

# ===== Garis Pemisah =====
ttk.Separator(frame_main, orient="horizontal").pack(fill="x", pady=10)

# ===== Hasil =====
style_label = ("Segoe UI", 11, "bold")
style_value = ("Consolas", 13)

label_hasil_desimal = tk.Label(frame_main, text="Desimal:", bg="#FFFFFF", font=style_label)
label_hasil_desimal.pack(pady=2)
label_hasil_desimal_val = tk.Label(frame_main, text="-", bg="#FFFFFF", font=style_value, fg="#333")
label_hasil_desimal_val.pack(pady=2)

label_hasil_heksa = tk.Label(frame_main, text="Heksadesimal:", bg="#FFFFFF", font=style_label)
label_hasil_heksa.pack(pady=2)
label_hasil_heksa_val = tk.Label(frame_main, text="-", bg="#FFFFFF", font=style_value, fg="#333")
label_hasil_heksa_val.pack(pady=2)

# ===== Footer =====
footer = tk.Label(root, text="Dibuat oleh: Jumita Hutagalung", bg="#E9F0FB", fg="#666", font=("Segoe UI", 9))
footer.pack(side="bottom", pady=5)

# Jalankan program
root.mainloop
import tkinter as tk
from tkinter import ttk, messagebox

# === Fungsi Konversi ===
def konversi_oktal():
    oktal = entry_oktal.get().strip()
    if not oktal:
        messagebox.showwarning("Peringatan", "Masukkan bilangan oktal terlebih dahulu!")
        return

    try:
        # Konversi ke desimal
        desimal = int(oktal, 8)
        # Konversi ke bentuk lain
        biner = bin(desimal).replace("0b", "")
        heksa = hex(desimal).upper().replace("0X", "")

        # Tampilkan hasil
        label_desimal_val.config(text=str(desimal))
        label_biner_val.config(text=biner)
        label_heksa_val.config(text=heksa)

    except ValueError:
        messagebox.showerror("Error", "Masukkan bilangan oktal yang valid (0-7)!")

# === Fungsi Reset ===
def reset():
    entry_oktal.delete(0, tk.END)
    label_desimal_val.config(text="-")
    label_biner_val.config(text="-")
    label_heksa_val.config(text="-")

# === GUI Utama ===
root = tk.Tk()
root.title("Konversi Bilangan Oktal ke Desimal, Biner, dan Heksadesimal")
root.geometry("470x420")
root.config(bg="#E8F0FE")

# === Frame Utama ===
frame_main = tk.Frame(root, bg="#FFFFFF", bd=3, relief="groove")
frame_main.place(relx=0.5, rely=0.5, anchor="center", width=430, height=380)

# === Judul ===
judul = tk.Label(frame_main, text="💡 Konversi Oktal ke Desimal, Biner & Heksadesimal",
                 bg="#FFFFFF", fg="#2E2E2E", font=("Segoe UI", 13, "bold"))
judul.pack(pady=15)

# === Input ===
label_oktal = tk.Label(frame_main, text="Masukkan Bilangan Oktal:", bg="#FFFFFF", font=("Segoe UI", 11))
label_oktal.pack(pady=(10, 0))

entry_oktal = tk.Entry(frame_main, width=25, font=("Consolas", 14), justify="center", bg="#F3F7FA", relief="flat")
entry_oktal.pack(pady=8, ipady=5)

# === Tombol Aksi ===
frame_button = tk.Frame(frame_main, bg="#FFFFFF")
frame_button.pack(pady=15)

btn_konversi = tk.Button(frame_button, text="Konversi", command=konversi_oktal,
                         bg="#4CAF50", fg="white", font=("Segoe UI", 11, "bold"), width=12, relief="flat")
btn_konversi.grid(row=0, column=0, padx=5)

btn_reset = tk.Button(frame_button, text="Reset", command=reset,
                      bg="#E53935", fg="white", font=("Segoe UI", 11, "bold"), width=12, relief="flat")
btn_reset.grid(row=0, column=1, padx=5)

# === Garis Pemisah ===
ttk.Separator(frame_main, orient="horizontal").pack(fill="x", pady=10)

# === Hasil Konversi ===
style_label = ("Segoe UI", 11, "bold")
style_value = ("Consolas", 13)

label_desimal = tk.Label(frame_main, text="Desimal:", bg="#FFFFFF", font=style_label)
label_desimal.pack(pady=2)
label_desimal_val = tk.Label(frame_main, text="-", bg="#FFFFFF", font=style_value, fg="#333")
label_desimal_val.pack(pady=2)

label_biner = tk.Label(frame_main, text="Biner:", bg="#FFFFFF", font=style_label)
label_biner.pack(pady=2)
label_biner_val = tk.Label(frame_main, text="-", bg="#FFFFFF", font=style_value, fg="#333")
label_biner_val.pack(pady=2)

label_heksa = tk.Label(frame_main, text="Heksadesimal:", bg="#FFFFFF", font=style_label)
label_heksa.pack(pady=2)
label_heksa_val = tk.Label(frame_main, text="-", bg="#FFFFFF", font=style_value, fg="#333")
label_heksa_val.pack(pady=2)

# === Footer ===
footer = tk.Label(root, text="Dibuat oleh: Jumita Hutagalung", bg="#E8F0FE", fg="#555", font=("Segoe UI", 9))
footer.pack(side="bottom", pady=6)

# Jalankan GUI
root.mainloop()

import tkinter as tk
from tkinter import ttk, messagebox

# === Fungsi Konversi ===
def konversi_heksa():
    heksa = entry_heksa.get().strip()
    if not heksa:
        messagebox.showwarning("Peringatan", "Masukkan bilangan heksadesimal terlebih dahulu!")
        return

    try:
        # Konversi ke desimal
        desimal = int(heksa, 16)
        # Konversi ke bentuk lain
        biner = bin(desimal).replace("0b", "")
        oktal = oct(desimal).replace("0o", "")

        # Tampilkan hasil
        label_desimal_val.config(text=str(desimal))
        label_biner_val.config(text=biner)
        label_oktal_val.config(text=oktal)

    except ValueError:
        messagebox.showerror("Error", "Masukkan bilangan heksadesimal yang valid (0-9, A-F)!")

# === Fungsi Reset ===
def reset():
    entry_heksa.delete(0, tk.END)
    label_desimal_val.config(text="-")
    label_biner_val.config(text="-")
    label_oktal_val.config(text="-")

# === GUI Utama ===
root = tk.Tk()
root.title("Konversi Bilangan Heksadesimal ke Desimal, Biner, dan Oktal")
root.geometry("480x420")
root.config(bg="#E6F0FA")

# === Frame Utama ===
frame_main = tk.Frame(root, bg="#FFFFFF", bd=3, relief="groove")
frame_main.place(relx=0.5, rely=0.5, anchor="center", width=440, height=380)

# === Judul ===
judul = tk.Label(
    frame_main,
    text="💡 Konversi Heksadesimal ke Desimal, Biner & Oktal",
    bg="#FFFFFF",
    fg="#222",
    font=("Segoe UI", 13, "bold")
)
judul.pack(pady=15)

# === Input ===
label_heksa = tk.Label(frame_main, text="Masukkan Bilangan Heksadesimal:", bg="#FFFFFF", font=("Segoe UI", 11))
label_heksa.pack(pady=(10, 0))

entry_heksa = tk.Entry(frame_main, width=25, font=("Consolas", 14), justify="center", bg="#F3F7FA", relief="flat")
entry_heksa.pack(pady=8, ipady=5)

# === Tombol Aksi ===
frame_button = tk.Frame(frame_main, bg="#FFFFFF")
frame_button.pack(pady=15)

btn_konversi = tk.Button(
    frame_button, text="Konversi", command=konversi_heksa,
    bg="#4CAF50", fg="white", font=("Segoe UI", 11, "bold"),
    width=12, relief="flat", cursor="hand2"
)
btn_konversi.grid(row=0, column=0, padx=5)

btn_reset = tk.Button(
    frame_button, text="Reset", command=reset,
    bg="#E53935", fg="white", font=("Segoe UI", 11, "bold"),
    width=12, relief="flat", cursor="hand2"
)
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

label_oktal = tk.Label(frame_main, text="Oktal:", bg="#FFFFFF", font=style_label)
label_oktal.pack(pady=2)
label_oktal_val = tk.Label(frame_main, text="-", bg="#FFFFFF", font=style_value, fg="#333")
label_oktal_val.pack(pady=2)

# === Footer ===
footer = tk.Label(
    root,
    text="Dibuat oleh: Jumita Hutagalung",
    bg="#E6F0FA", fg="#666", font=("Segoe UI", 9)
)
footer.pack(side="bottom", pady=6)

# Jalankan GUI
root.mainloop()

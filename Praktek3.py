import tkinter as tk
from tkinter import messagebox

def konversi():
    try:
        desimal = int(entry_desimal.get())
        biner = bin(desimal)[2:]
        oktal = oct(desimal)[2:]
        heksa = hex(desimal)[2:].upper()

        label_biner_val.config(text=biner)
        label_oktal_val.config(text=oktal)
        label_heksa_val.config(text=heksa)
    except ValueError:
        messagebox.showerror("Error", "Masukkan bilangan desimal yang valid!")

# Membuat jendela utama
root = tk.Tk()
root.title("Kalkulator Konversi Bilangan")
root.geometry("380x280")
root.configure(bg="#e8ebf0")

# Judul
judul = tk.Label(root, text="KALKULATOR KONVERSI DESIMAL", font=("Segoe UI", 12, "bold"), bg="#e8ebf0")
judul.pack(pady=10)

# Input bilangan desimal
frame_input = tk.Frame(root, bg="#e8ebf0")
frame_input.pack(pady=10)

tk.Label(frame_input, text="Masukkan Bilangan Desimal:", bg="#e8ebf0", font=("Segoe UI", 10)).grid(row=0, column=0)
entry_desimal = tk.Entry(frame_input, width=15, font=("Segoe UI", 10))
entry_desimal.grid(row=0, column=1, padx=10)

# Tombol konversi
btn_konversi = tk.Button(root, text="Konversi", command=konversi, font=("Segoe UI", 10, "bold"), bg="#4a7dfc", fg="white", relief="ridge")
btn_konversi.pack(pady=8)

# Hasil konversi
frame_hasil = tk.Frame(root, bg="#e8ebf0")
frame_hasil.pack(pady=10)

tk.Label(frame_hasil, text="Biner:", bg="#e8ebf0", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky="w")
label_biner_val = tk.Label(frame_hasil, text="-", bg="#ffffff", width=20, relief="sunken", anchor="w")
label_biner_val.grid(row=0, column=1, pady=3)

tk.Label(frame_hasil, text="Oktal:", bg="#e8ebf0", font=("Segoe UI", 10, "bold")).grid(row=1, column=0, sticky="w")
label_oktal_val = tk.Label(frame_hasil, text="-", bg="#ffffff", width=20, relief="sunken", anchor="w")
label_oktal_val.grid(row=1, column=1, pady=3)

tk.Label(frame_hasil, text="Heksadesimal:", bg="#e8ebf0", font=("Segoe UI", 10, "bold")).grid(row=2, column=0, sticky="w")
label_heksa_val = tk.Label(frame_hasil, text="-", bg="#ffffff", width=20, relief="sunken", anchor="w")
label_heksa_val.grid(row=2, column=1, pady=3)

# Jalankan aplikasi
root.mainloop()

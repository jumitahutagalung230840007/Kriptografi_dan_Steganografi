import tkinter as tk
from tkinter import messagebox

def proses_elgamal():
    try:
        p = int(entry_p.get())
        g = int(entry_g.get())
        m = int(entry_m.get())

        # Nilai tetap agar mudah dipahami (sesuai praktikum)
        x = 6   # private key
        k = 7   # bilangan acak

        # Pembentukan kunci
        y = pow(g, x, p)

        # Enkripsi
        a = pow(g, k, p)
        b = (m * pow(y, k, p)) % p

        # Dekripsi
        s = pow(a, x, p)
        s_inv = pow(s, -1, p)
        m_decrypt = (b * s_inv) % p

        # Tampilkan proses
        text_output.delete("1.0", tk.END)
        text_output.insert(tk.END, "=== ALGORITMA ELGAMAL ===\n\n")

        text_output.insert(tk.END, "1. Parameter Awal\n")
        text_output.insert(tk.END, f"p (prima)        = {p}\n")
        text_output.insert(tk.END, f"g (generator)   = {g}\n")
        text_output.insert(tk.END, f"x (private key) = {x}\n\n")

        text_output.insert(tk.END, "2. Pembentukan Kunci Publik\n")
        text_output.insert(tk.END, f"y = g^x mod p = {g}^{x} mod {p} = {y}\n\n")

        text_output.insert(tk.END, "3. Proses Enkripsi\n")
        text_output.insert(tk.END, f"Pesan (m) = {m}\n")
        text_output.insert(tk.END, f"k (acak)  = {k}\n")
        text_output.insert(tk.END, f"a = g^k mod p = {a}\n")
        text_output.insert(tk.END, f"b = m × y^k mod p = {b}\n")
        text_output.insert(tk.END, f"Ciphertext = ({a}, {b})\n\n")

        text_output.insert(tk.END, "4. Proses Dekripsi\n")
        text_output.insert(tk.END, f"s = a^x mod p = {s}\n")
        text_output.insert(tk.END, f"s⁻¹ mod p = {s_inv}\n")
        text_output.insert(tk.END, f"m = b × s⁻¹ mod p = {m_decrypt}\n\n")

        text_output.insert(tk.END, f"HASIL AKHIR: {m_decrypt}")

    except:
        messagebox.showerror("Error", "Input tidak valid!")

# GUI
root = tk.Tk()
root.title("Algoritma ElGamal Cryptosystem")
root.geometry("520x420")

tk.Label(root, text="Algoritma ElGamal Cryptosystem",
         font=("Arial", 12, "bold")).pack(pady=5)

frame_input = tk.Frame(root)
frame_input.pack(pady=5)

tk.Label(frame_input, text="Bilangan Prima (p)").grid(row=0, column=0, sticky="w")
entry_p = tk.Entry(frame_input, width=20)
entry_p.grid(row=0, column=1)

tk.Label(frame_input, text="Generator (g)").grid(row=1, column=0, sticky="w")
entry_g = tk.Entry(frame_input, width=20)
entry_g.grid(row=1, column=1)

tk.Label(frame_input, text="Plaintext (m)").grid(row=2, column=0, sticky="w")
entry_m = tk.Entry(frame_input, width=20)
entry_m.grid(row=2, column=1)

tk.Button(root, text="Proses ElGamal",
          command=proses_elgamal).pack(pady=5)

text_output = tk.Text(root, height=12, width=60)
text_output.pack(padx=10, pady=5)

root.mainloop()
  
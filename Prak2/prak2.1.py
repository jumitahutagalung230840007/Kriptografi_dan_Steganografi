import tkinter as tk
from tkinter import messagebox

# =====================================
#   ULTRA MODERN STYLE (GLASS UI)
# =====================================

BG_MAIN = "#c6d2ff"     # background lembut biru-ungu
CARD_BG = "#ffffff"      # card putih
BTN_BG = "#6a5acd"       # tombol ungu lembut
BTN_HOVER = "#5346a8"    # hover lebih gelap
RED_BTN = "#ff4f4f"
RED_HOVER = "#d93636"

FONT_TITLE = ("Segoe UI Semibold", 15)
FONT_TEXT = ("Segoe UI", 11)


def make_button(parent, text, color, color_hover, cmd):
    btn = tk.Label(
        parent,
        text=text,
        bg=color,
        fg="white",
        font=("Segoe UI", 11, "bold"),
        bd=0,
        padx=20,
        pady=10,
        cursor="hand2"
    )

    # Rounded button effect
    btn.pack_propagate(False)
    btn.bind("<Button-1>", lambda e: cmd())

    # Hover effect
    btn.bind("<Enter>", lambda e: btn.config(bg=color_hover))
    btn.bind("<Leave>", lambda e: btn.config(bg=color))
    return btn


# =====================================
#   KALKULATOR WINDOW
# =====================================
def buka_kalkulator():
    kalk = tk.Toplevel(root)
    kalk.title("Kalkulator Sederhana")
    kalk.geometry("420x360")
    kalk.config(bg=BG_MAIN)

    # Frosted card style
    card = tk.Frame(
        kalk,
        bg=CARD_BG,
        bd=0,
        highlightbackground="#a8b2ff",
        highlightthickness=2
    )
    card.place(relx=0.5, rely=0.5, anchor="center", width=370, height=310)

    tk.Label(card, text="Kalkulator Sederhana", font=FONT_TITLE, bg=CARD_BG).pack(pady=15)

    # Inputs
    tk.Label(card, text="Nilai A:", font=FONT_TEXT, bg=CARD_BG).pack()
    entry_a = tk.Entry(card, font=("Segoe UI", 11), width=28, relief="solid", bd=1)
    entry_a.pack(pady=5)

    tk.Label(card, text="Nilai B:", font=FONT_TEXT, bg=CARD_BG).pack()
    entry_b = tk.Entry(card, font=("Segoe UI", 11), width=28, relief="solid", bd=1)
    entry_b.pack(pady=5)

    tk.Label(card, text="Operator (+, -, *, /):", font=FONT_TEXT, bg=CARD_BG).pack()
    entry_op = tk.Entry(card, font=("Segoe UI", 11), width=15, relief="solid", bd=1)
    entry_op.pack(pady=5)

    # Perhitungan
    def hitung():
        try:
            a = float(entry_a.get())
            b = float(entry_b.get())
            op = entry_op.get()

            if op == '+':
                hasil = a + b
            elif op == '-':
                hasil = a - b
            elif op == '*':
                hasil = a * b
            elif op == '/':
                hasil = a / b if b != 0 else "Tidak bisa dibagi 0"
            else:
                hasil = "Operator tidak dikenal!"

            lanjut = messagebox.askquestion("Hasil", f"Hasil: {hasil}\n\nHitung lagi?")
            if lanjut == "yes":
                entry_a.delete(0, tk.END)
                entry_b.delete(0, tk.END)
                entry_op.delete(0, tk.END)
                entry_a.focus()
            else:
                kalk.destroy()

        except ValueError:
            messagebox.showerror("Error", "Masukkan angka yang valid!")

    # Button Modern
    btn_hitung = make_button(card, "Hitung", BTN_BG, BTN_HOVER, hitung)
    btn_hitung.pack(pady=15)


# =====================================
#   MENU UTAMA
# =====================================
root = tk.Tk()
root.title("Menu Utama Program IF & Kalkulator")
root.geometry("430x360")
root.config(bg=BG_MAIN)

# Card utama
menu_card = tk.Frame(
    root,
    bg=CARD_BG,
    highlightbackground="#a8b2ff",
    highlightthickness=2
)
menu_card.place(relx=0.5, rely=0.5, anchor="center", width=380, height=300)

# Title
tk.Label(menu_card, text="MENU UTAMA", font=FONT_TITLE, bg=CARD_BG).pack(pady=20)

# Buttons
btn_kalk = make_button(menu_card, "Kalkulator Sederhana", BTN_BG, BTN_HOVER, buka_kalkulator)
btn_kalk.pack(pady=10)

btn_keluar = make_button(menu_card, "Keluar", RED_BTN, RED_HOVER, root.destroy)
btn_keluar.pack(pady=10)

root.mainloop()

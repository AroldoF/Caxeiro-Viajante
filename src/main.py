import tkinter as tk


def main():
    root = tk.Tk()
    root.title("Caixeiro Viajante")
    root.geometry("500x500")
    root.resizable(False, False)

    label = tk.Label(
        root,
        text="Olá, Tkinter!",
        font=("Arial", 18),
    )
    label.pack(pady=50)

    def submit():
        i = city_input.get()

        cities.append(i)
        l.config(text=f"{[city for city in cities]}")
        city_input.set("")

    cities = []

    city_input = tk.StringVar()

    city_entry = tk.Entry(root,textvariable = city_input)

    city_entry.pack()

    l = tk.Label(root, text=f" {cities} ")
    l.pack()

    b = tk.Button(root, text="submit", command=submit, width=15)
    b.pack()

    root.mainloop()


if __name__ == "__main__":
    main()

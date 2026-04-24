from tkinter import *
from textblob import TextBlob
import webbrowser
import requests

root = Tk()
root.title("Spell Right ✨")
root.geometry("900x600")

dark_mode = False


def create_rounded_rect(self, x1, y1, x2, y2, radius=20, **kwargs):
    points = [
        x1+radius, y1,
        x2-radius, y1,
        x2, y1,
        x2, y1+radius,
        x2, y2-radius,
        x2, y2,
        x2-radius, y2,
        x1+radius, y2,
        x1, y2,
        x1, y2-radius,
        x1, y1+radius,
        x1, y1
    ]
    return self.create_polygon(points, smooth=True, **kwargs)

Canvas.create_rounded_rect = create_rounded_rect


class RoundedEntry(Frame):
    def __init__(self, parent, command):
        super().__init__(parent)

        self.command = command
        self.width = 460
        self.height = 48

        self.canvas = Canvas(self, width=self.width, height=self.height,
                             highlightthickness=0, bd=0)
        self.canvas.pack()

        self.entry = Entry(self.canvas,
                           font=("Helvetica", 14),
                           relief="flat",
                           justify="center")

        self.icon = Button(self.canvas,
                           text="🔍",
                           font=("Helvetica", 12),
                           bd=0,
                           relief="flat",
                           command=self.command)

        self.draw()

    def draw(self):
        self.canvas.delete("all")

        bg_root = root.cget("bg")
        self.config(bg=bg_root)
        self.canvas.config(bg=bg_root)

        if dark_mode:
            fill = "#1E1E2E"
            outline = "#14B8A6"
            text = "#E5E7EB"
        else:
            fill = "white"
            outline = "#C0608F"
            text = "#C0608F"

        self.canvas.create_rounded_rect(
            4, 4, self.width-4, self.height-4,
            radius=22,
            fill=fill,
            outline=outline,
            width=2
        )

        self.canvas.create_window(
            self.width//2 - 20,
            self.height//2,
            window=self.entry,
            width=self.width - 80,
            height=28
        )

        self.canvas.create_window(
            self.width - 30,
            self.height//2,
            window=self.icon
        )

        self.entry.config(bg=fill, fg=text, insertbackground=outline)
        self.icon.config(bg=fill, fg=outline, activebackground=fill)

    def get(self):
        return self.entry.get()

    def update_colors(self):
        self.draw()


def open_suggestions_window(event=None):
    text = search_entry.get().strip()
    if not text:
        return

    corrected = str(TextBlob(text).correct())

    try:
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{corrected}"
        response = requests.get(url)
        data = response.json()

        meaning = data[0]['meanings'][0]['definitions'][0]['definition']
    except:
        meaning = "Meaning not found."

    try:
        syn_url = f"https://api.datamuse.com/words?rel_syn={corrected}"
        syn_res = requests.get(syn_url)
        syn_data = syn_res.json()

        synonyms_list = [word['word'] for word in syn_data[:5]]
        synonyms = ", ".join(synonyms_list) if synonyms_list else "No synonyms found."
    except:
        synonyms = "No synonyms found."

    win = Toplevel(root)
    win.geometry("520x400")

    bg = "#121212" if dark_mode else "#FFF4C2"
    accent = "#14B8A6" if dark_mode else "#C0608F"
    text_color = "#E5E7EB" if dark_mode else "#444"

    win.config(bg=bg)

    Label(win,
          text=f"Word: {corrected}",
          font=("Helvetica", 18, "bold"),
          bg=bg,
          fg=accent).pack(pady=10)

    Label(win,
          text="📖 Meaning",
          font=("Helvetica", 14, "bold"),
          bg=bg,
          fg=accent).pack(anchor="w", padx=20)

    Label(win,
          text=meaning,
          font=("Helvetica", 13),
          wraplength=460,
          justify="left",
          bg=bg,
          fg=text_color).pack(anchor="w", padx=20, pady=5)

    Label(win,
          text="🔁 Synonyms",
          font=("Helvetica", 14, "bold"),
          bg=bg,
          fg=accent).pack(anchor="w", padx=20, pady=(10, 0))

    Label(win,
          text=synonyms,
          font=("Helvetica", 13),
          wraplength=460,
          justify="left",
          bg=bg,
          fg=text_color).pack(anchor="w", padx=20, pady=5)


def open_dictionary():
    webbrowser.open("https://www.dictionary.com")


def toggle_dark_mode():
    global dark_mode

    if not dark_mode:
        bg = "#121212"
        surface = "#1E1E2E"
        accent = "#14B8A6"

        root.config(bg=bg)
        top_frame.config(bg=bg)
        center_frame.config(bg=bg)
        search_frame.config(bg=bg)
        dict_frame.config(bg=bg)

        heading.config(bg=bg, fg=accent)

        dict_btn.config(bg=surface, fg=accent)
        dark_btn.config(text="☀", bg=surface, fg=accent)

        dark_mode = True
    else:
        bg = "#FFF4C2"
        accent = "#C0608F"

        root.config(bg=bg)
        top_frame.config(bg=bg)
        center_frame.config(bg=bg)
        search_frame.config(bg=bg)
        dict_frame.config(bg=bg)

        heading.config(bg=bg, fg=accent)

        dict_btn.config(bg="#FFD6E0", fg=accent)
        dark_btn.config(text="🌙", bg="#FFD6E0", fg=accent)

        dark_mode = False

    search_entry.update_colors()
    root.update_idletasks()


root.config(bg="#FFF4C2")

top_frame = Frame(root, bg="#FFF4C2")
top_frame.pack(fill=X)

dark_btn = Button(top_frame,
                  text="🌙",
                  font=("Helvetica", 14),
                  bd=0,
                  bg="#FFD6E0",
                  fg="#C0608F",
                  command=toggle_dark_mode)
dark_btn.pack(side=RIGHT, padx=15, pady=10)

center_frame = Frame(root, bg="#FFF4C2")
center_frame.pack(expand=True)

heading = Label(center_frame,
                text="Spell Right ✨",
                font=("Helvetica", 30, "bold"),
                bg="#FFF4C2",
                fg="#C0608F")
heading.pack(pady=20)

search_frame = Frame(center_frame, bg="#FFF4C2")
search_frame.pack(pady=10)

search_entry = RoundedEntry(search_frame, command=open_suggestions_window)
search_entry.pack()

root.bind("<Return>", open_suggestions_window)

dict_frame = Frame(center_frame, bg="#FFF4C2")
dict_frame.pack(pady=15)

dict_btn = Button(dict_frame,
                  text="📖 Open Dictionary",
                  font=("Helvetica", 13, "bold"),
                  padx=20,
                  pady=8,
                  bd=0,
                  relief="flat",
                  bg="#FFD6E0",
                  fg="#C0608F",
                  command=open_dictionary)
dict_btn.pack()

root.mainloop()

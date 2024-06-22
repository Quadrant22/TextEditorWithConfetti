import tkinter as tk
# filedialog module in tkinter provides classes and functions 
# filedialog is used when user needs to search a directory from the system
from tkinter import filedialog
from tkinter import messagebox
import pygame
import random

class YaldaFileEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Yalda File Editor")
        
        # The text widget that will fill the entire window
        self.text_widget = tk.Text(root, bg="white", fg="purple")
        self.text_widget.pack(expand="yes", fill="both")
        
        self.menu = tk.Menu(root)
        root.config(menu=self.menu)
        
        # A menu that holds three labels, Open, Save and Exit.
        # add_command(options) adds a menu item to the menu
        # add_cascade(options) creates a new hierarchical menu and associates it to a parent manu
        self.file_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=root.quit)
        
        # Edit menu holds Cut, Copy, Paste
        self.edit_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Cut", command=self.cut_text)
        self.edit_menu.add_command(label="Copy", command=self.copy_text)
        self.edit_menu.add_command(label="Paste", command=self.paste_text)

        # Encouragement button
        self.encouragement_button = tk.Button(root, text="Get Encouragement", command=self.get_encouragement, bg='purple')
        self.encouragement_button.pack()

        self.confetti_canvas = tk.Canvas(root, bg="white", width=root.winfo_width(), height=root.winfo_height())
        self.confetti_canvas.pack(fill="both", expand=True)
        self.confetti_task = None
    
    # Using filedialog.askopenfilename(extentions) from the filedialog module 
    # Inside the open_file() function. 
    # "r" open in read mode
    # delete(0, END) to clear the content of entry widget, deletes all the content in that range
    def open_file(self):
        file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("All Files", "*.*"), ("Text Files", "*.txt"), ("Python Scripts", "*.py"), ("HTML Documents", "*.html")])
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
                self.text_widget.delete(1.0, tk.END)
                self.text_widget.insert(tk.END, content)
    # .write() will write the content to file which is saving it to that file. 
    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("All Files", "*.*"), ("Text Files", "*.txt"), ("Python Scripts", "*.py"), ("HTML Documents", "*.html")])
        if file_path:
            with open(file_path, "w") as file:
                content = self.text_widget.get(1.0, tk.END)
                file.write(content)
    # tk.SEL_FIRST and tk.SEL_LAT
    # tk doesn't have a function to return a selected text but tk.SEL_FIRST and tk.SEL_LAT
    # retrieves the first and end of of selection
    def cut_text(self):
        selected_text = self.text_widget.get(tk.SEL_FIRST, tk.SEL_LAST)
        self.text_widget.delete(tk.SEL_FIRST, tk.SEL_LAST)
        self.root.clipboard_clear()
        self.root.clipboard_append(selected_text)
    
    def copy_text(self):
        selected_text = self.text_widget.get(tk.SEL_FIRST, tk.SEL_LAST)
        self.root.clipboard_clear()
        self.root.clipboard_append(selected_text)
    
    def paste_text(self):
        clipboard_text = self.root.clipboard_get()
        self.text_widget.insert(tk.INSERT, clipboard_text)

    # Display words of encourgement using the random generator
    # Using pygame to play music
    def get_encouragement(self):
        pygame.mixer.init()  # Initialize the mixer
        pygame.mixer.music.load('inspiring-minimalistic-ambient.mp3')  
        pygame.mixer.music.play()
        encouragements = [
            "You're doing great!",
            "Keep up the good work!",
            "You've got this!",
            "Believe in yourself!",
            "You're making progress!",
            "It's worth a shot!"
        ]
        encouragement = random.choice(encouragements)
        messagebox.showinfo("Encouragement", encouragement)

    def start_confetti(self):
        if self.confetti_task is None:
            self.confetti_task = self.root.after(100, self.create_confetti)

    def stop_confetti(self):
        if self.confetti_task:
            self.root.after_cancel(self.confetti_task)
            self.confetti_task = None

    def create_confetti(self):
        colors = ["red", "green", "blue", "orange", "purple"]
        x = random.randint(0, self.root.winfo_width())
        y = 0
        size = random.randint(10, 30)
        color = random.choice(colors)
        self.confetti_canvas.create_oval(x, y, x + size, y + size, fill=color)
        
        if y < self.root.winfo_height():
            self.confetti_canvas.move(tk.ALL, 0, 2)
            self.confetti_task = self.root.after(100, self.create_confetti)
        else:
            self.confetti_task = None


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    editor = YaldaFileEditor(root)

    # Add a button to start the confetti animation
    start_confetti_button = tk.Button(root, text="Start Confetti", command=editor.start_confetti, bg='purple')
    start_confetti_button.pack()
    
    # Add a button to stop the confetti animation
    stop_confetti_button = tk.Button(root, text="Stop Confetti", command=editor.stop_confetti, bg='purple')
    stop_confetti_button.pack()

    root.mainloop()
 

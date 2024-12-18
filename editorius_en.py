import tkinter as tk
from tkinter import filedialog, messagebox
import sys
import os

class TextEditor:
    def __init__(self, root, filename=None):
        self.root = root
        self.root.title("Editorius ver. 1.2 (EN)")
        self.text = tk.Text(root)
        self.text.pack(expand=True, fill='both')

        # Command entry field
        self.command_entry = tk.Entry(root)
        self.command_entry.pack(fill='x')
        self.command_entry.bind('<Return>', self.process_command)
        self.command_entry.config(state='disabled')  # Initially disabled

        # Setting up hotkeys
        self.root.bind('<Control-p>', self.show_command_entry)
        self.root.bind('<Control-s>', self.save_file)
        self.root.bind('<Control-a>', self.save_file_and_exit)
        self.root.bind('<Control-d>', self.exit_without_saving)
        self.root.bind('<Control-o>', self.open_file_dialog)  # Added for opening a file

        # Open file if specified
        if filename:
            self.open_file(filename)

    def show_command_entry(self, event=None):
        self.command_entry.config(state='normal')  # Enable the entry field
        self.command_entry.focus()  # Set focus on the entry field

    def process_command(self, event=None):
        command = self.command_entry.get().strip().lower()
        self.command_entry.delete(0, tk.END)  # Clear the entry field after input

        if command == 's':
            self.save_file()
        elif command == 'a':
            self.save_file_and_exit()
        elif command == 'd':
            self.exit_without_saving()
        elif command == 'y':
            self.exit_without_saving(confirm=True)
        elif command == 'n':
            messagebox.showinfo("Cancelled", "Exit cancelled.")
        else:
            messagebox.showwarning("Invalid command", "Enter 's' to save, 'a' to exit with saving, 'd' to exit without saving, 'y' to confirm exit without saving, 'n' to cancel.")

    def open_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                self.text.delete(1.0, tk.END)
                self.text.insert(tk.END, file.read())
        except FileNotFoundError:
            messagebox.showwarning("File not found", f"File '{file_path}' not found. A new file has been created.")
            self.new_file()

    def open_file_dialog(self, event=None):
        file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            self.open_file(file_path)

    def new_file(self):
        self.text.delete(1.0, tk.END)

    def save_file(self, event=None):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.text.get(1.0, tk.END))
            messagebox.showinfo("Saving", "File saved successfully!")

    def save_file_and_exit(self, event=None):
        self.save_file()
        self.root.quit()

    def exit_without_saving(self, event=None, confirm=False):
        if confirm or messagebox.askokcancel("Exit", "Are you sure you want to exit without saving?"):
            self.root.quit()

if __name__ == "__main__":
    filename = None
    if len(sys.argv) > 1:
        filename = sys.argv[1]  # Get the filename from command line arguments
    root = tk.Tk()
    editor = TextEditor(root, filename)
    root.mainloop()


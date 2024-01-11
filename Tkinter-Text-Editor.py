import tkinter as tk
from tkinter import filedialog
from typing import Optional

class TextEditor:
    def __init__(self, root: tk.Tk) -> None:
        self.root: tk.Tk = root
        self.root.title('Text Pad for Lesson ')
        self.root.geometry('1200x660')

        self.open_status_name: Optional[str] = None

        self.create_widgets()

    def create_widgets(self) -> None:
        # Create the main frame
        my_frame: tk.Frame = tk.Frame(self.root)
        my_frame.pack(pady=5)

        # Create a Scrollbar
        text_scroll: tk.Scrollbar = tk.Scrollbar(my_frame)
        text_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Create Text Box
        self.my_text: tk.Text = tk.Text(my_frame, width=97, height=25, font=('Helvetica', 16),
                                       selectbackground='blue', selectforeground='red',
                                       undo=True, yscrollcommand=text_scroll.set)
        self.my_text.pack()

        # Configure Scrollbar
        text_scroll.config(command=self.my_text.yview)

        # Create Menu
        my_menu: tk.Menu = tk.Menu(self.root)
        self.root.config(menu=my_menu)

        # Add File Menu
        file_menu: tk.Menu = tk.Menu(my_menu, tearoff=False)
        my_menu.add_cascade(label='File', menu=file_menu)
        file_menu.add_command(label='Open', command=self.open_file)
        file_menu.add_command(label='Save', command=self.save_file)
        file_menu.add_command(label='Save As', command=self.save_as_file)
        file_menu.add_command(label='New', command=self.new_file)
        file_menu.add_separator()
        file_menu.add_command(label='Go Out', command=self.root.quit)

        # Add Edit Menu
        edit_menu: tk.Menu = tk.Menu(my_menu, tearoff=False)
        my_menu.add_cascade(label='Edit', menu=edit_menu)
        edit_menu.add_command(label='Cut', command=lambda: self.cut_copy_paste('cut'))
        edit_menu.add_command(label='Copy', command=lambda: self.cut_copy_paste('copy'))
        edit_menu.add_command(label='Paste', command=lambda: self.cut_copy_paste('paste'))
        edit_menu.add_separator()
        edit_menu.add_command(label='Undo', command=self.my_text.edit_undo)
        edit_menu.add_command(label='Redo', command=self.my_text.edit_redo)

        # Add Status Bar
        self.status_bar: tk.Label = tk.Label(self.root, text='Ready     ', anchor=tk.E)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM, ipady=5)

    def new_file(self) -> None:
        self.my_text.delete('1.0', tk.END)
        self.root.title('New File - TextPad for Lesson')
        self.status_bar.config(text='New File.......')
        self.open_status_name = None

    def open_file(self) -> None:
        self.my_text.delete('1.0', tk.END)
        text_file: Optional[str] = filedialog.askopenfilename(initialdir='~/Desktop', title='Open File',
                                                              filetypes=(('Text Files', '*.txt'),
                                                                         ('Python Files', '*.py'),
                                                                         ('All Files', '*.*')))
        if text_file:
            self.open_status_name = text_file
            self.root.title(f'{text_file} - TextPad for Lesson')
            with open(text_file, 'r') as file:
                stuff: str = file.read()
                self.my_text.insert(tk.END, stuff)
            self.status_bar.config(text=f'Opened: {text_file}')
        else:
            self.status_bar.config(text='No file selected')

    def save_as_file(self) -> None:
        text_file: Optional[str] = filedialog.asksaveasfilename(defaultextension='.*', initialdir='~/Desktop', title='Save File',
                                                                filetypes=(('Text Files', '*.txt'),
                                                                           ('Python Files', '*.py'),
                                                                           ('All Files', '*.*')))
        if text_file:
            with open(text_file, 'w') as file:
                file.write(self.my_text.get(1.0, tk.END))
            self.status_bar.config(text=f'Saved: {text_file}')
            self.open_status_name = text_file

    def save_file(self) -> None:
        if self.open_status_name:
            with open(self.open_status_name, 'w') as file:
                file.write(self.my_text.get(1.0, tk.END))
            self.status_bar.config(text=f'Saved: {self.open_status_name}')
        else:
            self.save_as_file()

    def cut_copy_paste(self, action: str) -> None:
        if action == 'cut':
            self.my_text.event_generate("<<Cut>>")
        elif action == 'copy':
            self.my_text.event_generate("<<Copy>>")
        elif action == 'paste':
            self.my_text.event_generate("<<Paste>>")

if __name__ == '__main__':
    root: tk.Tk = tk.Tk()
    app: TextEditor = TextEditor(root)
    root.mainloop()

#Python audio converter

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import sv_ttk
from pydub import AudioSegment
import os

# Supported formats
AUDIO_FORMATS = ['mp3', 'wav', 'ogg', 'flac']
INPUT_FORMATS = ['All'] + AUDIO_FORMATS

class AudioConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Bulk Audio Converter')
        self.files = []
        self.input_format = tk.StringVar(value=INPUT_FORMATS[0])
        self.output_format = tk.StringVar(value=AUDIO_FORMATS[0])
        self.output_folder = ''
        self.create_widgets()

    def create_widgets(self):
        # File selection
        file_frame = tk.Frame(self.root)
        file_frame.pack(padx=10, pady=5, fill='x')
        ttk.Button(file_frame, text='Select Audio Files', command=self.select_files).pack(side='left')
        self.file_label = tk.Label(file_frame, text='No files selected')
        self.file_label.pack(side='left', padx=10)

        # Convert from (input format)
        from_frame = tk.Frame(self.root)
        from_frame.pack(padx=10, pady=5, fill='x')
        tk.Label(from_frame, text='Convert from:').pack(side='left')
        from_menu = ttk.Combobox(from_frame, textvariable=self.input_format, values=INPUT_FORMATS, state='readonly', width=8)
        from_menu.pack(side='left', padx=5)

        # Output format
        format_frame = tk.Frame(self.root)
        format_frame.pack(padx=10, pady=5, fill='x')
        tk.Label(format_frame, text='Convert to:').pack(side='left')
        format_menu = ttk.Combobox(format_frame, textvariable=self.output_format, values=AUDIO_FORMATS, state='readonly')
        format_menu.pack(side='left', padx=5)

        # Output folder
        out_frame = tk.Frame(self.root)
        out_frame.pack(padx=10, pady=5, fill='x')
        ttk.Button(out_frame, text='Select Output Folder', command=self.select_output_folder).pack(side='left')
        self.out_label = tk.Label(out_frame, text='No folder selected')
        self.out_label.pack(side='left', padx=10)

        # Convert button
        ttk.Button(self.root, text='Convert', style="Accent.TButton", command=self.start_conversion_thread).pack(pady=10)

        # Progress bar
        self.progress = ttk.Progressbar(self.root, orient='horizontal', length=300, mode='determinate')
        self.progress.pack(pady=5)

        # Terminal-like output
        terminal_frame = tk.Frame(self.root)
        terminal_frame.pack(padx=10, pady=5, fill='both', expand=True)
        self.terminal = tk.Text(terminal_frame, height=10, state='disabled', bg='black', fg='lime', font=('Consolas', 10))
        self.terminal.pack(side='left', fill='both', expand=True)
        scrollbar = ttk.Scrollbar(terminal_frame, command=self.terminal.yview)
        scrollbar.pack(side='right', fill='y')
        self.terminal['yscrollcommand'] = scrollbar.set

        # Status
        self.status = tk.Label(self.root, text='', fg='#57C8FF', font=("Arial", 15) )
        self.status.pack(pady=5)
        self.status.config(text='Waiting...', height=6)

    def select_files(self):
        # Filter filetypes based on input_format
        ext = self.input_format.get()
        if ext == 'All':
            filetypes = [('Audio Files', '*.mp3 *.wav *.ogg *.flac *.aac *.m4a *.wma *.aiff *.alac')]
        else:
            filetypes = [(f'{ext.upper()} Files', f'*.{ext}')]
        files = filedialog.askopenfilenames(title='Select Audio Files', filetypes=filetypes)
        if files:
            self.files = list(files)
            self.file_label.config(text=f'{len(self.files)} files selected')
        else:
            self.files = []
            self.file_label.config(text='No files selected')

    def select_output_folder(self):
        folder = filedialog.askdirectory(title='Select Output Folder')
        if folder:
            self.output_folder = folder
            self.out_label.config(text=folder)
        else:
            self.output_folder = ''
            self.out_label.config(text='No folder selected')

    def start_conversion_thread(self):
        import threading
        thread = threading.Thread(target=self.convert_files, daemon=True)
        thread.start()

    def log_terminal(self, message):
        self.terminal.config(state='normal')
        self.terminal.insert('end', message + '\n')
        self.terminal.see('end')
        self.terminal.config(state='disabled')

    def convert_files(self):
        if not self.files:
            messagebox.showwarning('No Files', 'Please select audio files to convert.')
            return
        if not self.output_folder:
            messagebox.showwarning('No Output Folder', 'Please select an output folder.')
            return
        fmt = self.output_format.get()
        self.status.config(text='Converting...', height=6)
        self.progress['value'] = 0
        self.progress['maximum'] = len(self.files)
        self.terminal.config(state='normal')
        self.terminal.delete('1.0', 'end')
        self.terminal.config(state='disabled')
        self.root.update()
        success, failed = 0, 0
        for idx, file in enumerate(self.files, 1):
            try:
                audio = AudioSegment.from_file(file)
                base = os.path.splitext(os.path.basename(file))[0]
                out_path = os.path.join(self.output_folder, f'{base}.{fmt}')
                audio.export(out_path, format=fmt)
                success += 1
                self.root.after(0, self.log_terminal, f"[SUCCESS] {os.path.basename(file)} -> {fmt}")
            except Exception as e:
                failed += 1
                self.root.after(0, self.log_terminal, f"[FAILED]  {os.path.basename(file)}: {e}")
            self.root.after(0, self.progress.step, 1)
            self.root.update()
        self.status.config(text=f'Conversion complete: {success} succeeded, {failed} failed.', height=6)

import ctypes as ct
#dark titlebar - ONLY WORKS IN WINDOWS 11!!
def dark_title_bar(window):
    """
    MORE INFO:
    https://learn.microsoft.com/en-us/windows/win32/api/dwmapi/ne-dwmapi-dwmwindowattribute
    """
    window.update()
    DWMWA_USE_IMMERSIVE_DARK_MODE = 20
    set_window_attribute = ct.windll.dwmapi.DwmSetWindowAttribute
    get_parent = ct.windll.user32.GetParent
    hwnd = get_parent(window.winfo_id())
    rendering_policy = DWMWA_USE_IMMERSIVE_DARK_MODE
    value = 2
    value = ct.c_int(value)
    set_window_attribute(hwnd, rendering_policy, ct.byref(value), ct.sizeof(value))


if __name__ == '__main__':


    root = tk.Tk()

    dark_title_bar(root)

    #trying to get the taskbar icon to work
    myappid = 'Excel.File.Parser.V2' # arbitrary string
    ct.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)


    # Theme
    sv_ttk.set_theme("dark")
    app = AudioConverterApp(root)
    root.mainloop()

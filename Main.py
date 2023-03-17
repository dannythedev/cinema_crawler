import threading
import time
import tkinter as tk
import tkinter.ttk as ttk
import json
from Archive import Archive
from Parser import regexify


class LoadingScreen(tk.Toplevel):
    def __init__(self, master, max_value=100):
        super().__init__(master)
        self.title('Retrieving movies...')
        self.geometry('300x80')
        self.resizable(False, False)
        self.max_value = max_value
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self, text='Retrieving Movies...\n This may take awhile.')
        self.label.pack(pady=5)

        self.progressbar = ttk.Progressbar(self, orient='horizontal', length=200, mode='determinate')
        self.progressbar.pack(pady=5)

    def set_progress(self, value):
        self.progressbar['value'] = value

class RecursiveJSONViewer(tk.Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.master = master
        self.create_widgets()
        self.archive = None
        self.loading_screen = None

    def destroy_widgets(self):
        self.tree.destroy()
        self.load_button.destroy()
        self.collapse_button.destroy()
        self.expand_button.destroy()
        self.loading_screen.destroy()
        [button.destroy() for button in self.checklist_buttons]
        self.loading_screen = None

    def create_widgets(self):
        self.tree = ttk.Treeview(self)
        self.tree.pack(fill='both', expand=True)
        self.tree.heading('#0', text='Results')
        self.pack(fill='both', expand=True)

        self.tree.pack(side='top', fill='both', expand=True)

        self.pack(fill='both', expand=True)

        self.load_button = ttk.Button(self, text='Retrieve Movies', command=self.start)
        self.load_button.pack(side='left')

        self.expand_button = ttk.Button(self, text='Expand all', command=self.expand_all)
        self.expand_button.pack(side='left')

        self.collapse_button = ttk.Button(self, text='Collapse all', command=self.collapse_all)
        self.collapse_button.pack(side='left')

        style = ttk.Style(self.master)
        # Set style for modern look
        style.theme_use('clam')
        style.configure('Treeview', font=('Arial', 12))

        # Set new colors for the treeview widget
        style.configure('Treeview', background='#333', fieldbackground='#333', foreground='white')
        style.map('Treeview', background=[('selected', '#555')], foreground=[('selected', 'white')])

        self.add_checklist(['RottenTomatoes', 'Metacritic', 'IMDB'])

        # Define a new button style for dark mode
        style.configure('DarkButton.TButton', background='#555', foreground='white', borderwidth=0, focuscolor='#555')

        self.tree.bind('<Button-3>', self.popup)

    def load_json(self, data, parent=''):
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, (dict, list)):
                    node = self.tree.insert(parent, 'end', text=f'{key}:')
                    self.load_json(value, node)
                else:
                    self.tree.insert(parent, 'end', text=f'{key}: {value}')

        elif isinstance(data, list):
            for idx, item in enumerate(data):
                if isinstance(item, (dict, list)):
                    index = '{0} | {1}'.format(str(item['total_rating'])[:4], item['title']) if 'title' in item else f'[{idx}]:'
                    node = self.tree.insert(parent, 'end', text=index)
                    self.load_json(item, node)
                else:
                    self.tree.insert(parent, 'end', text=f'[{idx}]: {item}')
        else:
            self.tree.insert(parent, 'end', text=str(data))

    def expand_all(self):
        def _expand_all(parent):
            for child in self.tree.get_children(parent):
                self.tree.item(child, open=True)
                _expand_all(child)
        _expand_all('')

    def collapse_all(self):
        def _collapse_all(parent):
            for child in self.tree.get_children(parent):
                _collapse_all(child)
                self.tree.item(child, open=False)
        _collapse_all('')

    def refresh(self):
        self.master.update()
        self.master.after(1000,self.refresh)
        if self.loading_screen is not None:
            if self.archive is not None:
                self.loading_screen.set_progress(self.archive.get_progress())
                self.master.update_idletasks()

    def start(self):
        self.refresh()

        def get_json():
            self.load_button["state"] = tk.DISABLED
            print("Starting.")
            start = time.time()
            self.archive = Archive(reviewers=self.get_checked_items())
            self.archive.initialize()
            self.destroy_widgets()
            self.create_widgets()
            self.load_json(read_json())
            self.load_button["state"] = tk.NORMAL
            print('Time:', time.time() - start)

        threading.Thread(target=get_json).start()
        self.loading_screen = LoadingScreen(self.master)


    def popup(self, event):
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label='Copy Value', command=self.copy_value)
        menu.post(event.x_root, event.y_root)

    def copy_value(self):
        text = regexify(regex=':(.*)',data=self.tree.item(self.tree.focus(), 'text'))
        if text:
            self.master.clipboard_clear()
            self.master.clipboard_append(text)

    def get_checked_items(self):
        checked_items = []
        for item in self.checklist:
            if item[1].get() == 1:
                checked_items.append(item[0])
        return checked_items

    def add_checklist(self, items):
        self.checklist = []
        self.checklist_buttons = []
        for item in items:
            var = tk.IntVar()
            checkbutton = ttk.Checkbutton(self.master, text=item, variable=var)
            checkbutton.pack(side='left', padx=5, pady=2)
            self.checklist.append((item, var))
            self.checklist_buttons.append(checkbutton)

def read_json():
    f = open('movies.json', 'r')
    try:
        json_data = json.loads(f.read())

    except:
        json_data = {}
    f.close()
    return json_data

if __name__ == '__main__':
    json_data = read_json()
    root = tk.Tk()
    root.title('Movie Rating Scrapper')
    root.geometry('400x600')
    viewer = RecursiveJSONViewer(root)

    viewer.load_json(json_data)
    root.mainloop()
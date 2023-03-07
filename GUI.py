import tkinter as tk
import tkinter.ttk as ttk
import json
from Parser import regexify
from main import get_json


class RecursiveJSONViewer(tk.Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        self.tree = ttk.Treeview(self)
        self.tree.pack(fill='both', expand=True)
        self.tree.heading('#0', text='Results')
        self.pack(fill='both', expand=True)

        self.scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side='left', fill='y')
        self.tree.pack(side='left', fill='both', expand=True)

        self.pack(fill='both', expand=True)


        self.expand_button = ttk.Button(self, text='Expand all', command=self.expand_all)
        self.expand_button.pack(side='bottom')

        self.collapse_button = ttk.Button(self, text='Collapse all', command=self.collapse_all)
        self.collapse_button.pack(side='bottom')

        self.load_button = ttk.Button(self, text='Load JSON', command=get_json)
        self.load_button.pack(side='bottom')

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
                    index = item['title'] if 'title' in item else f'[{idx}]:'
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

    def popup(self, event):
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label='Copy Value', command=self.copy_value)
        menu.post(event.x_root, event.y_root)

    def copy_value(self):
        text = regexify(regex=':(.*)',data=self.tree.item(self.tree.focus(), 'text'))
        if text:
            self.master.clipboard_clear()
            self.master.clipboard_append(text)


if __name__ == '__main__':
    f = open('movies.json', 'r')
    json_data = json.loads(f.read())
    f.close()
    root = tk.Tk()
    root.title('Movie Rating Scrapper')
    viewer = RecursiveJSONViewer(root)
    viewer.load_json(json_data)
    root.mainloop()
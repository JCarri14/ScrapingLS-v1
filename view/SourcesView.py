from tkinter import *
from tkinter import ttk
from functools import partial
from model.SourceFilter import SourceFilter
from view.SourcesAddView import SourceAddView
from utils.Constants import *


class SourcesView(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, bg=COLOR_WHITE)
        self.srcItems = []
        self.data_container = None
        self.aux_container = None
        self.btnAdd = None

    def init_view(self):
        self.place(relx=0, rely=0.1, relwidth=1, relheight=0.9)
        header = Frame(self, bg=COLOR_DARK)
        header.place(relx=0, rely=0, relwidth=1, relheight=0.1)

        self.btnAdd = Button(header, text=ADD_SRC_LABEL, fg=COLOR_WHITE, bg=COLOR_PRIMARY)
        self.btnAdd.place(relx=0.05, rely=0.1, relwidth=0.4, relheight=0.7)
        self.aux_container = Frame(self, bg=COLOR_WHITE)
        self.aux_container.place(relx=0, rely=0.1, relwidth=1, relheight=0.9)
        self.reset_data_container(self.aux_container, False)
        self.init_content_view(self.data_container)

    def reset_data_container(self, master, destroy: bool):
        if destroy:
            self.data_container.destroy()
        canvas = Canvas(master)
        canvas.config(bg=COLOR_WHITE, width=SCREEN_WIDTH*0.9)
        scrollbar = ttk.Scrollbar(master, orient="vertical", command=canvas.yview)
        self.data_container = ttk.Frame(canvas)
        self.data_container.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.data_container, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="y", expand=True)
        scrollbar.pack(side="right", fill="y")

        #self.data_container = Frame(self.data_container, bg=COLOR_WHITE)
        #self.data_container.place(relx=0, rely=0.1, relwidth=1, relheight=0.9)

    def hide_data_container(self):
        self.data_container.destroy()
        self.aux_container.destroy()
        self.aux_container = Frame(self, bg=COLOR_WHITE)
        self.aux_container.place(relx=0, rely=0.1, relwidth=1, relheight=0.9)

    def init_content_view(self, master):
        for item in self.srcItems:
            itemFrame = Frame(master, bg=COLOR_DARK)
            itemFrame.config(width=SCREEN_WIDTH * 0.9, height=70)
            itemFrame.pack(side=TOP, fill=X, pady=5)
            title = Label(itemFrame, bg=COLOR_DARK, anchor="w", fg=COLOR_WHITE, text=item.name)
            title.place(relx=0, rely=0, relwidth=0.5, relheight=0.5)
            url = Label(itemFrame, bg=COLOR_DARK, anchor="w", fg=COLOR_WHITE, text=item.url)
            url.place(relx=0, rely=0.5, relwidth=0.5, relheight=0.5)
            btnUpdate = Button(itemFrame, bg=COLOR_WHITE, fg=COLOR_DARK, text=UPDATE_LABEL)
            btnUpdate.place(relx=0.65, rely=0.25, relwidth=0.15, relheight=0.5)
            btnDelete = Button(itemFrame, bg=COLOR_ERROR, fg=COLOR_DARK, text=DELETE_LABEL)
            btnDelete.place(relx=0.8, rely=0.25, relwidth=0.15, relheight=0.5)

    def clearListFrame(self):
        # destroy all widgets from frame
        for widget in self.data_container.winfo_children():
            widget.destroy()

    def update_src_items(self, items):
        self.srcItems = items
        self.clearListFrame()
        self.init_content_view(self.data_container)

    def config_btns_listener(self):
        compt = 0
        for widget in self.data_container.winfo_children():
            update_with_arg = partial(self.updateBtnListener, compt)
            delete_with_arg = partial(self.deleteBtnListener, compt)
            widget.children['!button'].config(command=update_with_arg)
            widget.children['!button2'].config(command=delete_with_arg)
            compt += 1

    def set_list_listener(self, update_funct, delete_func):
        self.updateBtnListener = update_funct
        self.deleteBtnListener = delete_func
        self.config_btns_listener()



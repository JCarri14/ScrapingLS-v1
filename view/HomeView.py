from tkinter import *
from tkinter.font import Font
from tkinter import ttk
from utils.Constants import *

class HomeView(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, bg=COLOR_WHITE)
        self.srcItems = []
        self.newsItems = []
        self.filteredNews = []
        self.news_container = None
        self.searchInput = None
        self.btnSearch = None

    def init_frame(self):
        self.place(relx=0, rely=0.1, relwidth=1, relheight=0.9)
        header = Frame(self, bg=COLOR_DARK)
        header.place(relx=0, rely=0, relwidth=1, relheight=0.1)
        self.searchInput = Entry(header, bg=COLOR_WHITE, fg=COLOR_BLACK)
        self.searchInput.place(relx=0.05, rely=0.1, relwidth=0.3, relheight=0.7)

        self.btnSearch = Button(header, text=SEARCH_LABEL, fg=COLOR_WHITE, bg=COLOR_PRIMARY)
        self.btnSearch.place(relx=0.35, rely=0.1, relwidth=0.1, relheight=0.7)

        content = Frame(self, bg=COLOR_WHITE)
        content.place(relx=0, rely=0.1, relwidth=1, relheight=0.9)

        boldFont = Font(weight="bold")
        srcLabel = Label(content, text=SRC_LABEL, bg=COLOR_WHITE, font=boldFont)
        srcLabel.config(anchor="w")
        srcLabel.place(relx=0.02, rely=0.05, relwidth=0.4, relheight=0.1)

        self.aux_container = Frame(content, bg=COLOR_WHITE)
        self.aux_container.place(relx=0.02, rely=0.15, relwidth=0.4, relheight=0.8)

        self.reset_src_container(self.aux_container, False)
        self.display_src_items(self.src_container)

        self.aux_news_container = Frame(content, bg=COLOR_DARK)
        self.aux_news_container.place(relx=0.5, rely=0.05, relwidth=0.48, relheight=0.9)
        self.reset_news_container(self.aux_news_container, False)

    def destroy_view(self):
        self.destroy()

    def reset_src_container(self, master, destroy: bool):
        if destroy:
            self.src_container.destroy()
        canvas = Canvas(master)
        canvas.config(bg=COLOR_WHITE)
        scrollbar = ttk.Scrollbar(master, orient="vertical", command=canvas.yview)
        self.src_container = ttk.Frame(canvas)
        self.src_container.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.src_container, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="y", expand=True)
        scrollbar.pack(side="right", fill="y")

    def reset_news_container(self, master, destroy: bool):
        if destroy:
            self.news_container.destroy()
        canvas = Canvas(master)
        canvas.config(bg=COLOR_DARK, width=SCREEN_WIDTH*0.46)
        scrollbar = ttk.Scrollbar(master, orient="vertical", command=canvas.yview)
        self.news_container = ttk.Frame(canvas)
        self.news_container.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.news_container, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="y", expand=True)
        scrollbar.pack(side="right", fill="y")

    def display_src_items(self, master):
        for item in self.srcItems:
            itemContainer = Frame(master, bg=COLOR_DARK)
            itemContainer.config(width=400, height=60)
            itemTitle = Label(itemContainer, text=item.name, fg=COLOR_WHITE, bg=COLOR_DARK)
            itemTitle.place(relx=0, rely=0.3, relwidth=0.5, relheight=0.4)
            btnSwitch = Button(itemContainer, text="Disable", bg=COLOR_ERROR, fg=COLOR_WHITE)
            btnSwitch.place(relx=0.6, rely=0.2, relwidth=0.3, relheight=0.6)
            itemContainer.pack(fill=X, side=TOP, pady=5)

    def display_news_items(self, master):
        for item in self.newsItems:
            itemContainer = Frame(master, bg=COLOR_DARK)
            itemContainer.config(width=500, height=80)

            itemTitle = Label(itemContainer, text=item.title, fg=COLOR_WHITE, bg=COLOR_DARK)
            itemTitle.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.6)

            itemData = Label(itemContainer, anchor="w", text="Created at: " + str(item.created_at), fg=COLOR_WHITE, bg=COLOR_DARK)
            itemData.place(relx=0.1, rely=0.7, relwidth=0.3, relheight=0.3)

            itemShared = Label(itemContainer, anchor="w", text="Shared: " + str(item.times_shared), fg=COLOR_WHITE, bg=COLOR_DARK)
            itemShared.place(relx=0.5, rely=0.7, relwidth=0.3, relheight=0.3)

            itemComments = Label(itemContainer, anchor="w", text="Comments:" + str(item.comments), fg=COLOR_WHITE, bg=COLOR_DARK)
            itemComments.place(relx=0.7, rely=0.7, relwidth=0.2, relheight=0.3)
            itemContainer.pack(fill=X, side=TOP, pady=5)

    def clearSrcListFrame(self):
        # destroy all widgets from frame
        for widget in self.src_container.winfo_children():
            widget.destroy()

    def clearNewsListFrame(self):
        # destroy all widgets from frame
        for widget in self.news_container.winfo_children():
            widget.destroy()

    def update_src_items(self, items):
        self.srcItems = items
        self.clearSrcListFrame()
        self.display_src_items(self.src_container)

    def update_news_items(self, items):
        self.newsItems = items
        self.clearNewsListFrame()
        self.display_news_items(self.news_container)


    def add_news_item(self,item):
        self.newsItems.append(item)

    def add_src_item(self, item):
        self.srcItems.append(item)



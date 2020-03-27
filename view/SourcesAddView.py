from tkinter import *
from tkinter import ttk
from utils.Constants import *


class SourceAddView(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.parentView = master
        self.source_name = None
        self.source_url = None
        self.filtersList = None
        self.filterReference = None
        self.filterResult = None
        self.filterValue = None
        self.filters = []

    def init_view(self):
        Frame.__init__(self, self.parentView)

        leftContent = Frame(self.parentView, bg=COLOR_WHITE)
        leftContent.place(relx=0, rely=0.05, relwidth=0.5, relheight=0.9)
        self.init_left_side(leftContent)

        rightContent = Frame(self.parentView, bg=COLOR_WHITE)
        rightContent.place(relx=0.5, rely=0.05, relwidth=0.5, relheight=0.9)
        self.init_right_side(rightContent)

    def destroy_view(self):
        self.destroy()

    def update_view(self, name, url, filters):
        self.source_name.insert("end-1c", name)
        self.source_url.insert("end-1c", url)
        self.update_filters_list(filters)
        self.btnAccept.config(text=UPDATE_LABEL)

    def clearListFrame(self):
        # destroy all widgets from frame
        for widget in self.filtersList.winfo_children():
            widget.destroy()

    def add_filter_item(self, filter):
        self.filters.append(filter)

    def display_filters(self):
        for item in self.filters:
            itemFrame = Frame(self.filtersList, bg=COLOR_DARK)
            itemFrame.config(width=300, height=40)
            itemFrame.pack(side=TOP, fill=X, pady=5)
            title = Label(itemFrame, bg=COLOR_DARK, anchor="center", fg=COLOR_WHITE, text=item.expected_result)
            title.place(relx=0, rely=0, relwidth=1, relheight=0.7)

    def update_filters_list(self, list):
        self.filters = list
        self.clearListFrame()
        self.display_filters()

    def init_left_side(self, master):
        nameContainer = Frame(master, bg=COLOR_WHITE)
        nameContainer.place(relx=0, rely=0, relwidth=0.8, relheight=0.2)
        self.get_name_form(nameContainer)

        urlContainer = Frame(master, bg=COLOR_WHITE)
        urlContainer.place(relx=0, rely=0.20, relwidth=0.8, relheight=0.2)
        self.get_url_form(urlContainer)

        listContainer = Frame(master, bg=COLOR_WHITE)
        listContainer.place(relx=0, rely=0.40, relwidth=0.8, relheight=0.6)
        self.get_filter_list(listContainer)

    def init_right_side(self, master):
        resultContainer = Frame(master, bg=COLOR_WHITE)
        resultContainer.place(relx=0, rely=0, relwidth=0.8, relheight=0.2)
        self.get_filter_result_form(resultContainer)

        nameContainer = Frame(master, bg=COLOR_WHITE)
        nameContainer.place(relx=0, rely=0.20, relwidth=0.8, relheight=0.2)
        self.get_filter_reference_form(nameContainer)

        valueContainer = Frame(master, bg=COLOR_WHITE)
        valueContainer.place(relx=0, rely=0.40, relwidth=0.8, relheight=0.2)
        self.get_filter_value_form(valueContainer)

        addContainer = Frame(master, bg=COLOR_WHITE)
        addContainer.place(relx=0, rely=0.6, relwidth=0.8, relheight=0.2)
        self.get_btn_add_filter(addContainer)

        btnContainer = Frame(master, bg=COLOR_WHITE)
        btnContainer.place(relx=0, rely=0.8, relwidth=0.8, relheight=0.2)
        self.get_btn_form(btnContainer)

    def get_name_form(self, master: Frame):
        nameLabel = Label(master, text=NAME_LABEL, fg=COLOR_DARK, bg=COLOR_WHITE)
        nameLabel.config(anchor="w")
        nameLabel.place(relx=0.1, rely=0.05, relwidth=1, relheight=0.4)
        self.source_name = Text(master, fg=COLOR_WHITE, bg=COLOR_DARK)
        self.source_name.place(relx=0.1, rely=0.5, relwidth=1, relheight=0.4)

    def get_url_form(self, master: Frame):
        urlLabel = Label(master, text=URL_LABEL, fg=COLOR_DARK, bg=COLOR_WHITE)
        urlLabel.config(anchor="w")
        urlLabel.place(relx=0.1, rely=0.05, relwidth=1, relheight=0.4)
        self.source_url = Text(master, fg=COLOR_WHITE, bg=COLOR_DARK)
        self.source_url.place(relx=0.1, rely=0.5, relwidth=1, relheight=0.4)

    def get_filter_result_form(self, master: Frame):
        filterLabel = Label(master, text=FILTER_RESULT, fg=COLOR_DARK, bg=COLOR_WHITE)
        filterLabel.config(anchor="w")
        filterLabel.place(relx=0.1, rely=0.05, relwidth=0.8, relheight=0.4)
        self.filterResult = ttk.Combobox(master, values=RESULT_VALUES, state="readonly")
        self.filterResult.current(1)
        self.filterResult.place(relx=0.1, rely=0.5, relwidth=0.9, relheight=0.4)

    def get_filter_reference_form(self, master: Frame):
        filterLabel = Label(master, text=FILTER_LABEL, fg=COLOR_DARK, bg=COLOR_WHITE)
        filterLabel.config(anchor="w")
        filterLabel.place(relx=0.1, rely=0.05, relwidth=1, relheight=0.4)
        self.filterReference = Text(master, fg=COLOR_WHITE, bg=COLOR_DARK)
        self.filterReference.place(relx=0.1, rely=0.5, relwidth=1, relheight=0.4)

    def get_filter_value_form(self, master: Frame):
        filterLabel = Label(master, text=VALUE_LABEL, fg=COLOR_DARK, bg=COLOR_WHITE)
        filterLabel.config(anchor="w")
        filterLabel.place(relx=0.1, rely=0.05, relwidth=1, relheight=0.4)
        self.filterValue = Text(master, fg=COLOR_WHITE, bg=COLOR_DARK)
        self.filterValue.place(relx=0.1, rely=0.5, relwidth=1, relheight=0.4)

    def get_filter_list(self, master: Frame):
        filtersLabel = Label(master, text=FILTERS_LABEL, fg=COLOR_DARK, bg=COLOR_WHITE)
        filtersLabel.config(anchor="w")
        filtersLabel.place(relx=0.1, rely=0.05, relwidth=1, relheight=0.1)

        canvas = Canvas(master)
        canvas.config(bg=COLOR_WHITE, width=310)
        scrollbar = ttk.Scrollbar(master, orient="vertical", command=canvas.yview)
        self.filtersList = ttk.Frame(canvas)

        self.filtersList.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.filtersList, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="y", expand=True)
        scrollbar.pack(side="right", fill="y")

        #self.filtersList = Frame(master, bg=COLOR_WHITE)
        #self.filtersList.place(relx=0.1, rely=0.15, relwidth=0.9, relheight=0.8)

    def get_btn_add_filter(self, master):
        self.btnAddFilter = Button(master, text=ADD_LABEL, bg=COLOR_PRIMARY, fg=COLOR_WHITE)
        self.btnAddFilter.place(relx=0.1, rely=0, relwidth=0.9, relheight=0.4)

    def get_btn_form(self, master):
        self.btnAccept = Button(master, text=ADD_SRC_LABEL, bg=COLOR_PRIMARY, fg=COLOR_WHITE)
        self.btnAccept.place(relx=0.1, rely=0.3, relwidth=0.45, relheight=0.4)
        self.btnDecline = Button(master, text=CANCEL_LABEL, bg=COLOR_ERROR, fg=COLOR_DARK)
        self.btnDecline.place(relx=0.55, rely=0.3, relwidth=0.45, relheight=0.4)
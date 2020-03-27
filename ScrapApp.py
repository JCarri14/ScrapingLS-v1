from view.MainView import *
from controller.MainController import Controller


if __name__ == '__main__':
    root = Tk()
    root.withdraw()
    app = Controller(root)
    root.mainloop()

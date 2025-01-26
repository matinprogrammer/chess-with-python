from core import Chess
from windows_gui.main import WindowsGui

gui = WindowsGui(Chess())
gui.create_chess_board()
gui.show()

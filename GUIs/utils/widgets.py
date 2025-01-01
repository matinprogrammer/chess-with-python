from tkinter import Frame, Label, PhotoImage


class ChessCell(Frame):
    def __init__(self, cell_id: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = cell_id


class ChessLabel(Label):
    def __init__(self, label_id: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = label_id
        self.image: PhotoImage

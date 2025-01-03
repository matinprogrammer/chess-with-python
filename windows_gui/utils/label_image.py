from tkinter import PhotoImage, Label


def set_label_image(label: Label, picture_path: str) -> None:
    piece_image = PhotoImage(file=picture_path)
    label.config(image=piece_image)
    label.image = piece_image


def remove_label_image(label: Label) -> None:
    label.config(image="")
    label.image = None

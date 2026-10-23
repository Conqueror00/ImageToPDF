#print("Image to PDF Converter")

#Pillow library to convert the images to pdf
#from PIL import Image

#images =[
#    Image.open("photo1.jpg"),
#   Image.open("photo2.jpg"),
#    Image.open("photo3.png"),
#    Image.open("photo4.jpeg")
#]
#images[0].save(
#   "output.pdf",
#    save_all = True,
#    append_images = images[1:]
#)
#print("pdf created successfully!")


import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk,ImageOps, UnidentifiedImageError
#Image lets us work with images.
#ImageTk lets us use Pillow images inside Tkinter.
import os


window = tk.Tk()

window.title("Image to PDF")
window.geometry("800x600")

selected_files=[]

selected_preview = None

preview_labels=[]

def select_images():
    global selected_files

    selected_files = list(filedialog.askopenfilenames(
    title="Select Images",
    filetypes=[
        ("Image files", "*.jpg *.jpeg *.png")
    ]
))


    image_list.delete(0, tk.END)

    update_list()
    update_previews()
    status_label.config(
    text=f"{len(selected_files)} image(s) selected"
)


def remove_selected():
    selected_indexes = image_list.curselection()

    if selected_indexes:
        for index in reversed(selected_indexes):
            selected_files.pop(index)

        update_list()
        update_previews()

        status_label.config(
            text=f"{len(selected_files)} image(s) selected"
        )

def update_list():
    image_list.delete(0, tk.END)

    for file in selected_files:
        filename = os.path.basename(file)
        image_list.insert(tk.END, filename)


def move_up():
    selected_index = image_list.curselection()

    if selected_index:
        index = selected_index[0]

        if index > 0:
            #does this mean the photo 3 was ahead of photo 2 in the list
                     #photo 3                  photo 2
            selected_files[index],selected_files[index - 1] =(
                #photo2
                selected_files[index -1],
                #photo 3
                selected_files[index]

                #is this the area where the swap takes place

                #so now photo 2 is ahead of 3 after the swap?
            )

            update_list()
            update_previews()

            image_list.selection_set(index - 1)
            image_list.activate(index - 1)

            highlight_preview(index - 1)


def move_down():
    selected_index = image_list.curselection()

    if selected_index:
        index = selected_index[0]

        if index < len(selected_files) -1:
            selected_files[index],selected_files[index + 1] = (
                selected_files[index + 1],
                selected_files[index]
            )

            update_list()
            update_previews()

            image_list.selection_set(index + 1)
            image_list.activate(index + 1)

            highlight_preview(index + 1)



def convert_to_pdf():
    if not selected_files:
        status_label.config(
            text="Please select at least one image"
        )
        return

    save_path = filedialog.asksaveasfilename(
        title="Save PDF",
        defaultextension=".pdf",
        filetypes=[
            ("PDF files", "*.pdf")
        ]
    )

    if not save_path:
        return

    images = []


    progress_bar["value"] = 0
    progress_bar["maximum"] = len(selected_files)
    for file in selected_files:
        try:
            image = Image.open(file)
            image = ImageOps.exif_transpose(image)
            image = image.convert("RGB")
            images.append(image)


            progress_bar["value"] += 1
            window.update_idletasks()
            
        except(UnidentifiedImageError,OSError):
            status_label.config(
                text=f"Cant open: {os.path.basename(file)}"
            )
            return

    images[0].save(
        save_path,
        save_all=True,
        append_images=images[1:]
    )

    print("PDF created successfully!")
    status_label.config(
    text="PDF created successfully!"
    )

    window.after(2000,reset_app)

def reset_app():
    global selected_files, selected_preview, preview_labels

    selected_files = []
    selected_preview = None
    preview_labels = []

    image_list.delete(0, tk.END)

    for widget in preview_frame.winfo_children():
        widget.destroy()

    progress_bar["value"] = 0

    status_label.config(
        text="No images selected"
    )


def select_preview(index):
    image_list.selection_clear(0, tk.END)
    image_list.selection_set(index)
    image_list.activate(index)

    highlight_preview(index)

    if selected_preview:
        selected_preview.config(relief="flat")

    selected_preview = preview_labels[index]
    selected_preview.config(relief="solid")





def update_previews():
    global preview_labels, selected_preview

    for widget in preview_frame.winfo_children():
        widget.destroy()

    preview_labels = []
    selected_preview = None

    for index, file in enumerate(selected_files):
        image = Image.open(file)
        image.thumbnail((100, 100))

        photo = ImageTk.PhotoImage(image)

        frame = tk.Frame(preview_frame)
        frame.pack(side="left", padx=5)

        number_label = tk.Label(
            frame,
            text=f"{index + 1}"
        )
        number_label.pack()

        label = tk.Label(frame, image=photo)
        label.pack()

        label.image = photo

        label.bind(
            "<Button-1>",
            lambda event, index=index: select_preview(index)
        )

        preview_labels.append(label)

def highlight_preview(index):
    global selected_preview

    if selected_preview:
        selected_preview.config(relief="flat")

    selected_preview = preview_labels[index]
    selected_preview.config(relief="solid")









title = tk.Label(
    window,
    text="Image to PDF Converter",
    font= ("Arial",18,"bold")
)
title.pack(pady=15)

image_list=tk.Listbox(
    window,
    width=60,
    height=10,
    selectmode=tk.EXTENDED
)
image_list.pack(pady=10)

preview_frame = tk.Frame(window)
preview_frame.pack(pady=10)



button_frame = tk.Frame(window)
button_frame.pack(pady=5)




button = tk.Button(
    button_frame,
    text="Add Image(s)",
    command=select_images
)

button.pack(side="left", padx=5, pady=5)

remove_button = tk.Button(
    button_frame,
    text="Remove Image(s)",
    command = remove_selected
)

remove_button.pack(side="left", padx=5, pady=5)


move_up_button = tk.Button(
    button_frame,
    text="↑ Move Up",
    command=move_up
)

move_up_button.pack(side="left", padx=5, pady=5)

move_down_button = tk.Button(
    button_frame,
    text="↓ Move Down",
    command=move_down
)

move_down_button.pack(side="left", padx=5, pady=5)


convert_button = tk.Button(
    window,
    text="Convert To PDF",
    command=convert_to_pdf,
    font=("Arial",11,"bold"),
    padx=15,
    pady=5,
)

convert_button.pack(pady=10)


status_label = tk.Label(
    window,
    text="Ready — no images selected",
    font=("Arial", 10)
)

status_label.pack(pady=10)


progress_bar = ttk.Progressbar(
    window,
    orient="horizontal",
    length=400,
    mode="determinate"
)
progress_bar.pack(pady=5)


window.mainloop()
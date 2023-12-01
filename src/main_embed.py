import tkinter as tk
from tkinter import filedialog
import customtkinter
import cv2
import os
from PIL import Image

from encoder import encode_image

## Tkinter setup

app = customtkinter.CTk()
app.geometry("1100x700")
app.title("Watermark App by 18221121 Rozan Ghosani")

customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("../data/theme.json")

## Global variables
target_file = ""
result_dir = ""
seed = "18221121"

result_image = None
save_button_state = False

target = customtkinter.CTkImage(light_image=Image.open("../data/target.png"), dark_image=Image.open("../data/target.png"), size=(500, 500))
result = customtkinter.CTkImage(light_image=Image.open("../data/result.png"), dark_image=Image.open("../data/result.png"), size=(500, 500))

## Constants
k = 1.00

## Fonts
font_regular = customtkinter.CTkFont(family="Roboto", size=12, weight="normal")
font_bold = customtkinter.CTkFont(family="Roboto", size=14, weight="bold")

## Functions

def open_file_explorer():
    global target_file_entry, target_file, target
    target_file = filedialog.askopenfilename(initialdir="/", title="Select a file", filetypes=(("PNG files", "*.png"), ("JPEG files", "*.jpeg"), ("JPG files", "*.jpg")))
    target_file_entry.insert(tk.END, target_file)

    # show image preview
    print("Showing image preview...")
    image = Image.open(target_file)
    image = image.crop((0, 0, 500, 500))
    target.configure(light_image=image, dark_image=image)

    embed_watermark()


def embed_watermark():
    global target_file, embed_button_state, save_button_state, target, result_image, seed, seed_entry
    if target_file != "":
        save_button_state = False
        save_button.configure(state=tk.NORMAL)
        print("Embedding watermark...")

        seed = seed_entry.get()

        # embed watermark
        try:
            seed = int(seed)
        except:
            for i in range(len(seed)):
                intseed = ord(seed[i]) * (i + 1)
            seed = intseed
        result_image = encode_image(target_file, k, seed)

        # show original image grayscale preview
        original_image = cv2.imread(target_file, cv2.IMREAD_GRAYSCALE)
        original = Image.fromarray(original_image)
        original = original.crop((0, 0, 500, 500))
        target.configure(light_image=original, dark_image=original)

        # show watermarked image preview
        image = Image.fromarray(result_image)
        image = image.crop((0, 0, 500, 500))
        result.configure(light_image=image, dark_image=image)

def save_watermarked_image():
    global target_file, embed_button_state, save_button_state, result_image
    if target_file != "":
        print("Saving watermarked image...")
        target_file_name = target_file.split("/")[-1].split(".")[0]
        
        # opening file explorer to choose save directory
        target_save_dir = filedialog.askdirectory(initialdir="/", title="Select a directory")
        
        # save watermarked image
        cv2.imwrite(f"{target_save_dir}/{target_file_name}_watermarked.png", result_image)
        

def sliding(value):
    global k_slider_label, k, target_file
    k = value
    # Updating label with 2 decimal precision
    k_slider_label.configure(text=f"K Constant: {(round(k, 2)):.2f}")

    if target_file != "":
        embed_watermark()
    


## Main window

frame = customtkinter.CTkFrame(app)
frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

# Target file
target_file_frame = customtkinter.CTkFrame(frame)
target_file_frame.pack(fill=tk.BOTH)

target_file_entry = customtkinter.CTkEntry(target_file_frame, placeholder_text="Open target file", font=font_regular)
target_file_entry.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

file_explorer_button = customtkinter.CTkButton(target_file_frame, text="Browse", font=font_regular, command=open_file_explorer)
file_explorer_button.pack(side=tk.LEFT, padx=10, pady=10)

# Embed and save button and slider

button_frame = customtkinter.CTkFrame(frame)
button_frame.pack(fill=tk.BOTH)

# K Constant slider
k_slider_frame = customtkinter.CTkFrame(button_frame)
k_slider_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

seed_entry = customtkinter.CTkEntry(button_frame, placeholder_text="Seed", font=font_regular)
seed_entry.insert(tk.END, seed)
seed_entry.pack(side=tk.LEFT, padx=10, pady=10)

k_slider_label = customtkinter.CTkLabel(k_slider_frame, text=f"K Constant: {k}", font=font_regular)
k_slider_label.pack(side=tk.LEFT, padx=10, pady=10)

k_slider = customtkinter.CTkSlider(k_slider_frame, from_=0, to=255, command=sliding, width=500)
k_slider.pack(side=tk.RIGHT, padx=10, pady=10)

save_button = customtkinter.CTkButton(button_frame, text="Save", font=font_regular, command=save_watermarked_image, state=tk.DISABLED)
save_button.pack(side=tk.RIGHT, padx=10, pady=10)

# Image preview frame
img_section_frame = customtkinter.CTkFrame(frame)
img_section_frame.pack(fill=tk.BOTH, expand=True)

# Image preview
image_preview_frame = customtkinter.CTkFrame(img_section_frame)
image_preview_frame.pack(side=tk.LEFT, expand=True)

image_preview_label = customtkinter.CTkLabel(image_preview_frame, text="", image=target, font=font_regular)
image_preview_label.pack(padx=10, pady=10, expand=True)


# Watermarked image preview
watermarked_image_preview_frame = customtkinter.CTkFrame(img_section_frame)
watermarked_image_preview_frame.pack(side=tk.RIGHT, expand=True)

watermarked_image_preview_label = customtkinter.CTkLabel(watermarked_image_preview_frame, text="", image=result, font=font_regular)
watermarked_image_preview_label.pack(padx=10, pady=10, expand=True)


app.mainloop()
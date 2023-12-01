import tkinter as tk
from tkinter import filedialog
import customtkinter
import cv2
import os
from PIL import Image

from encoder import encode_image, generate_watermark
from decoder import detect_watermark

## Tkinter setup

app = customtkinter.CTk()
app.geometry("1100x800")
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
t = 0.9

## Fonts
font_regular = customtkinter.CTkFont(family="Roboto", size=12, weight="normal")
font_bold = customtkinter.CTkFont(family="Roboto", size=14, weight="bold")

## Functions

def open_file_explorer():
    global target_file_entry, target_file, target, analyze_button, result_frame
    target_file = filedialog.askopenfilename(initialdir="/", title="Select a file", filetypes=(("PNG files", "*.png"), ("JPEG files", "*.jpeg"), ("JPG files", "*.jpg")))
    target_file_entry.insert(tk.END, target_file)

    # show image preview
    print("Showing image preview...")
    image = Image.open(target_file)
    image = image.crop((0, 0, 500, 500))
    target.configure(light_image=image, dark_image=image)

    embed_watermark()

    analyze_button.configure(state=tk.NORMAL)
    result_frame.configure(fg_color="gray16")


def embed_watermark():
    global target_file, embed_button_state, save_button_state, target, result_image, seed, seed_entry, result_frame, result_label
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

    result_frame.configure(fg_color="gray16")
    result_label.configure(text="Analyze to see if the watermark can be readed")

def save_watermarked_image():
    global target_file, embed_button_state, save_button_state, result_image
    if target_file != "":
        print("Saving watermarked image...")
        target_file_name = target_file.split("/")[-1].split(".")[0]
        
        # opening file explorer to choose save directory
        target_save_dir = filedialog.askdirectory(initialdir="/", title="Select a directory")
        
        # save watermarked image
        cv2.imwrite(f"{target_save_dir}/{target_file_name}_watermarked.png", result_image)
        
def analyze_watermark():
    global target_file, result_image, t, result_label, result_frame, k, seed
    if target_file != "":
        print("Analyzing watermarked image...")
        result_frame.configure(fg_color="#3a7ebf")
        result_label.configure(text="Analyzing watermarked image...")

        width, height = result_image.shape[:2]

        # generate watermark
        watermark = generate_watermark(width, height, k, seed)

        print(result_image.shape[:2])
        print(watermark.shape[:2])

        # detect watermark
        result = detect_watermark(result_image, watermark, t)
        if result:
            result_frame.configure(fg_color="#3abf3a")
            result_label.configure(text="Gambar mengandung watermark.")
        else:
            result_frame.configure(fg_color="#bf3a3a")
            result_label.configure(text="Gambar tidak mengandung watermark.")

def k_sliding(value):
    global k_slider_label, k, target_file
    k = value
    # Updating label with 2 decimal precision
    k_slider_label.configure(text=f"K Constant: {(round(k, 2)):.2f}")

    if target_file != "":
        embed_watermark()

def t_sliding(value):
    global treshold_slider_label, t, target_file
    t = value
    # Updating label with 2 decimal precision
    treshold_slider_label.configure(text=f"Treshold: {(round(t, 2)):.2f}")
    


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

k_slider = customtkinter.CTkSlider(k_slider_frame, from_=0, to=255, number_of_steps=255, command=k_sliding, width=500)
k_slider.set(k)
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

# Treshold slider and analyze button
analyze_frame = customtkinter.CTkFrame(frame)
analyze_frame.pack(fill=tk.BOTH)

treshold_slider_frame = customtkinter.CTkFrame(analyze_frame)
treshold_slider_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

treshold_slider_label = customtkinter.CTkLabel(treshold_slider_frame, text=f"Treshold: {t}", font=font_regular)
treshold_slider_label.pack(side=tk.LEFT, padx=10, pady=10)

treshold_slider = customtkinter.CTkSlider(treshold_slider_frame, from_=0, to=1, command=t_sliding, width=500)
treshold_slider.set(t)
treshold_slider.pack(side=tk.RIGHT, padx=10, pady=10)

analyze_button = customtkinter.CTkButton(analyze_frame, text="Analyze", font=font_regular, command=analyze_watermark, state=tk.DISABLED, width=300)
analyze_button.pack(side=tk.RIGHT, padx=10, pady=10)

# Result label
result_frame = customtkinter.CTkFrame(frame)
result_frame.pack(fill=tk.BOTH, expand=True)

result_label = customtkinter.CTkLabel(result_frame, text="Analyze to see if the watermark can be readed", font=font_regular)
result_label.pack(fill=tk.BOTH, expand=True)

app.mainloop()
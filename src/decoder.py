import cv2
import numpy as np

def normalize_image(img):
    # Normalisasi citra menjadi zero mean
    normalized_img = img - np.mean(img)
    return normalized_img

def edge_enhance_filter(img):
    # Define an edge-enhance filter kernel
    kernel = np.array([[-1, -1, -1],
                       [-1,  8, -1],
                       [-1, -1, -1]])

    # Apply the filter
    filtered_img = cv2.filter2D(img, -1, kernel)
    return filtered_img

def detect_watermark(watermarked_img, watermark, threshold):
    # Matching image format
    watermark = watermark.astype(np.float32)
    watermarked_img = watermarked_img.astype(np.float32)

    # Apply edge-enhance filter to the watermarked image
    watermarked_img_enhanced = edge_enhance_filter(watermarked_img)

    # Normalization
    watermark_normalized = normalize_image(watermark)

    # Correlation
    correlation = cv2.matchTemplate(watermarked_img_enhanced, watermark_normalized, cv2.TM_CCOEFF_NORMED)
    loc = np.where(correlation >= threshold)

    if len(loc[0]) > 0:
        print("Gambar mengandung watermark.")
        return True
    else:
        print("Gambar tidak mengandung watermark.")
        return False
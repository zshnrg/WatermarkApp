import cv2
import numpy as np

def encode_image(img_path, k, seed):
    # file name
    file_name = img_path.split("/")[-1]

    # watermarking citra grayscale berbasis pseudorandom generator
    # extract grayscale image and size
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    img = np.array(img, dtype=np.int16)
    img_width, img_height = img.shape[:2]

    # generate watermark
    watermark = generate_watermark(img_width, img_height, k, seed)

    # add watermark to image
    print("Adding watermark...")
    watermarked_img = cv2.add(img, watermark)

    # save watermarked image
    return watermarked_img

def generate_watermark(img_width, img_height, k, seed):
    # random seed initialization for reproducibility
    np.random.seed(seed)

    # The pseudorandom noise pattern is a binary pattern consisting of {0,1} and is generated based on a key using, for instance, a seed.
    # generate watermark
    print("Generating watermark...")
    watermark = np.random.randint(2, size=(img_width, img_height))
    watermark = watermark.astype(np.int16)

    # Mapping the watermark signal to the {-1, 1} range
    watermark[watermark == 0] = -1

    # The watermark signal is then multiplied by a constant k to produce the final watermark signal W(x,y)
    watermark = watermark * k

    # converting into cv2 image
    watermark = np.array(watermark, dtype=np.int16)
    return watermark

hasil = encode_image("a.jpg", 5, 18221121)
cv2.imwrite("hasil.png", hasil)
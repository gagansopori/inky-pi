import os
import numpy as np
import cv2
from PIL import Image, ImageFont, ImageDraw
import tflite_runtime.interpreter as tflite

# --- CONFIG ---
MODEL_PATH = "ghibli_model.tflite"
INPUT_PATH = "input.jpg"  # Your source image
OUTPUT_PATH = "ghibli_out.png"  # Transformed image
ASSETS_DIR = "./assets"  # Where you keep your fonts
EPAPER_SIZE = (800, 480)  # Adjust to your specific display


def process_ghibli():
    # 1. Load Model
    interpreter = tflite.Interpreter(model_path=MODEL_PATH)
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # 2. Prepare Image
    img = cv2.imread(INPUT_PATH)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Model expects 512x512
    img_resized = cv2.resize(img, (512, 512))
    img_input = np.expand_dims(img_resized.astype(np.float32) / 127.5 - 1, axis=0)

    # 3. Inference
    interpreter.set_tensor(input_details[0]['index'], img_input)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])

    # 4. Post-Process
    output_data = (np.squeeze(output_data) + 1.0) * 127.5
    output_data = np.clip(output_data, 0, 255).astype(np.uint8)
    ghibli_pil = Image.fromarray(output_data)

    # 5. Add Text with Assets Fonts
    draw = ImageDraw.Draw(ghibli_pil)
    # Automatically finds the first .ttf font in your assets folder
    font_files = [f for f in os.listdir(ASSETS_DIR) if f.endswith('.ttf')]

    if font_files:
        font_path = os.path.join(ASSETS_DIR, font_files[0])
        font = ImageFont.truetype(font_path, 30)
        draw.text((10, 10), "Ghibli-Pi Render", font=font, fill=(255, 255, 255))
        print(f"✅ Applied font: {font_files[0]}")

    # 6. Resize and Dither for ePaper (Critical step)
    # Converting to 'L' (Grayscale) then '1' (1-bit) uses Floyd-Steinberg dithering
    final_epaper = ghibli_pil.resize(EPAPER_SIZE, Image.LANCZOS).convert("L").convert("1")
    final_epaper.save(OUTPUT_PATH)
    print(f"✨ Transformation complete: {OUTPUT_PATH}")


if __name__ == "__main__":
    if os.path.exists(MODEL_PATH):
        process_ghibli()
    else:
        print("❌ Model file not found! Run the wget command first.")
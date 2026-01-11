import os
import re
import math
from PIL import Image

def clean_filename(path):
    """
    Cleans filename to be Android-safe:
    - Lowercase
    - Replace non-alphanumeric with _
    - Trim _
    - Prepend img_ if starts with digit
    """
    original_name = os.path.splitext(os.path.basename(path))[0]
    clean_name = original_name.lower()
    clean_name = re.sub(r'[^a-z0-9_]', '_', clean_name)
    clean_name = re.sub(r'_+', '_', clean_name)
    clean_name = clean_name.strip('_')

    if not clean_name:
        clean_name = "image"

    if re.match(r'^[0-9]', clean_name):
        clean_name = f"img_{clean_name}"

    return clean_name

def detect_base_density(width):
    """
    Detects the base density of the image based on width, 
    assuming a target baseline of roughly 48dp for icons/assets.
    """
    densities = {
        "mdpi": 1.0,
        "hdpi": 1.5,
        "xhdpi": 2.0,
        "xxhdpi": 3.0,
        "xxxhdpi": 4.0
    }
    
    # Heuristic: find density that makes the base width closest to 48
    # Using the logic from the PowerShell script: abs(width / density - 48)
    
    best_density_name = "mdpi"
    min_diff = float('inf')
    
    for name, value in densities.items():
        diff = abs((width / value) - 48)
        if diff < min_diff:
            min_diff = diff
            best_density_name = name
            
    return best_density_name, densities[best_density_name]

def generate_assets_for_file(file_path, base_output_dir, log_callback=print):
    """
    Generates assets for a single file.
    """
    if not os.path.exists(file_path):
        log_callback(f"❌ File not found: {file_path}")
        return

    try:
        with Image.open(file_path) as img:
            width, height = img.size
            log_callback(f"Processing: {os.path.basename(file_path)}")
            log_callback(f"📐 Original Size: {width} x {height}")

            clean_name = clean_filename(file_path)
            extension = os.path.splitext(file_path)[1].lower()
            # If the extension is not .png, .jpg, or .jpeg, we might want to default to .png for assets 
            # or keep original. Let's keep original unless logical to convert.
            # Android assets usually PNG/JPG.
            if extension not in ['.png', '.jpg', '.jpeg', '.webp']:
                 # Fallback to png if weird format, but let's respect original if possible or default to png
                 extension = ".png"

            final_filename = f"{clean_name}{extension}"
            log_callback(f"📝 Asset Name: {final_filename}")

            base_density_name, base_density_value = detect_base_density(width)
            log_callback(f"🎯 Base Density: {base_density_name} ({base_density_value}x)")

            mdpi_width = width / base_density_value
            mdpi_height = height / base_density_value
            
            densities = {
                "mdpi": 1.0,
                "hdpi": 1.5,
                "xhdpi": 2.0,
                "xxhdpi": 3.0,
                "xxxhdpi": 4.0
            }

            if not os.path.exists(base_output_dir):
                os.makedirs(base_output_dir)

            for dpi_name, dpi_scale in densities.items():
                target_width = int(round(mdpi_width * dpi_scale))
                target_height = int(round(mdpi_height * dpi_scale))
                
                # Avoid resizing to 0
                target_width = max(1, target_width)
                target_height = max(1, target_height)

                target_dir = os.path.join(base_output_dir, f"drawable-{dpi_name}")
                if not os.path.exists(target_dir):
                    os.makedirs(target_dir)

                target_path = os.path.join(target_dir, final_filename)
                
                # Resize
                resized_img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
                resized_img.save(target_path)
                
                log_callback(f"✔ drawable-{dpi_name}: {target_width}x{target_height}")
            
            log_callback("--------------------------------------------------")

    except Exception as e:
        log_callback(f"❌ Error processing {os.path.basename(file_path)}: {e}")

def process_input(input_path, output_dir, log_callback=print):
    """
    Main entry point for processing file or directory.
    """
    if not input_path:
        log_callback("❌ No input selected.")
        return

    if not output_dir:
        output_dir = os.path.join(os.path.dirname(input_path), "android")
    
    log_callback(f"🚀 Starting output to: {output_dir}")

    if os.path.isfile(input_path):
        generate_assets_for_file(input_path, output_dir, log_callback)
    elif os.path.isdir(input_path):
        supported_exts = ('.png', '.jpg', '.jpeg', '.webp')
        files = [f for f in os.listdir(input_path) if f.lower().endswith(supported_exts)]
        
        if not files:
            log_callback("❌ No compatible images found in directory.")
            return

        log_callback(f"📂 Found {len(files)} images in directory.")
        for f in files:
            full_path = os.path.join(input_path, f)
            generate_assets_for_file(full_path, output_dir, log_callback)
    else:
        log_callback("❌ Invalid input path.")
    
    log_callback("🎉 Done!")

import os
import json
from PIL import Image, PngImagePlugin
from mutagen.oggvorbis import OggVorbis

# Define the metadata
metadata_text = """Apache-2.0 License
Copyright (c) 2025 Mazey-Jessica Emily Twilight
Copyright (c) 2025 UnifiedGaming Systems Ltd (Company Number: 16108983)"""

metadata_dict = {
    "license": "Apache-2.0",
    "copyright": [
        "Copyright (c) 2025 Mazey-Jessica Emily Twilight",
        "Copyright (c) 2025 UnifiedGaming Systems Ltd (Company Number: 16108983)"
    ]
}

# Function to clean and update JSON, JEM, and MCMETA files
def clean_and_update_json(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith((".json", ".jem", ".mcmeta")):
                file_path = os.path.join(root, file)
                
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        data = json.load(f)

                    # Remove any keys that start with "_"
                    data = {k: v for k, v in data.items() if not k.startswith("_")}

                    # Add metadata if missing
                    data.setdefault("license", metadata_dict["license"])
                    data.setdefault("copyright", metadata_dict["copyright"])

                    with open(file_path, "w", encoding="utf-8") as f:
                        json.dump(data, f, indent=4)

                    print(f"Updated JSON/JEM/MCMETA: {file_path}")

                except (json.JSONDecodeError, ValueError):
                    print(f"Skipped (invalid JSON): {file_path}")

# Function to add metadata to PNG files
def add_metadata_to_png(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".png"):
                file_path = os.path.join(root, file)
                try:
                    img = Image.open(file_path)
                    meta = PngImagePlugin.PngInfo()
                    meta.add_text("License", metadata_dict["license"])
                    meta.add_text("Copyright", "\n".join(metadata_dict["copyright"]))
                    img.save(file_path, "PNG", pnginfo=meta)
                    print(f"Updated PNG Metadata: {file_path}")
                except Exception as e:
                    print(f"Failed to update {file_path}: {e}")

# Function to add metadata to .properties files
def add_metadata_to_properties(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".properties"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        lines = f.readlines()
                    if any("license=" in line or "copyright=" in line for line in lines):
                        continue  # Skip if metadata exists
                    new_lines = [f"license={metadata_dict['license']}\n",
                                 f"copyright={'; '.join(metadata_dict['copyright'])}\n"] + lines
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.writelines(new_lines)
                    print(f"Updated .properties: {file_path}")
                except Exception as e:
                    print(f"Failed to update {file_path}: {e}")

# Function to add metadata to .ogg files
def add_metadata_to_ogg(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".ogg"):
                file_path = os.path.join(root, file)
                try:
                    audio = OggVorbis(file_path)
                    audio["LICENSE"] = metadata_dict["license"]
                    audio["COPYRIGHT"] = "\n".join(metadata_dict["copyright"])
                    audio.save()
                    print(f"Updated OGG Metadata: {file_path}")
                except Exception as e:
                    print(f"Failed to update {file_path}: {e}")

# Function to add metadata to XML, Java, and YML files
def add_metadata_to_text_files(directory, extensions, comment_style):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(extensions):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.readlines()
                    
                    # Check if metadata already exists
                    if any("Apache-2.0 License" in line for line in content):
                        continue  # Skip if already present

                    # Add metadata at the top of the file
                    metadata_comment = "\n".join([f"{comment_style} {line}" for line in metadata_text.split("\n")])
                    new_content = [metadata_comment + "\n\n"] + content

                    with open(file_path, "w", encoding="utf-8") as f:
                        f.writelines(new_content)

                    print(f"Updated {file_path}")

                except Exception as e:
                    print(f"Failed to update {file_path}: {e}")

# Run the script in the current directory
clean_and_update_json(".")
add_metadata_to_png(".")
add_metadata_to_properties(".")
add_metadata_to_ogg(".")
add_metadata_to_text_files(".", (".xml",), "<!--")  # XML Comments
add_metadata_to_text_files(".", (".java",), "//")  # Java Comments
add_metadata_to_text_files(".", (".yml", ".yaml"), "#")  # YAML Comments

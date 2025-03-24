import os

root_folder = 'C:\\D\\DSU\\Gunda_Gunde\\Asir Matira'

def append_folder_name_to_images(root_folder):
    """
    Append the immediate folder name followed by @@!!!!!!@@ to each image file name
    in the given root folder and its subdirectories.
    """
    # Supported image file extensions
    image_extensions = {'.png', '.jpg', '.jpeg', '.tif', '.tiff', '.gif'}

    # Walk through all directories and files in the root folder
    for dirpath, _, filenames in os.walk(root_folder):
        # Extract the immediate folder name
        folder_name = os.path.basename(dirpath)

        for filename in filenames:
            # Check if the file has a valid image extension
            ext = os.path.splitext(filename)[1].lower()
            if ext in image_extensions and '@@!!!!!!@@' not in filename:
                old_path = os.path.join(dirpath, filename)
                # Create the new filename
                name_without_ext = os.path.splitext(filename)[0]
                new_name = f"{folder_name}@@!!!!!!@@{name_without_ext}{ext}"
                new_path = os.path.join(dirpath, new_name)

                # Rename the file
                try:
                    os.rename(old_path, new_path)
                    print(f"Renamed: {old_path} -> {new_path}")
                except Exception as e:
                    print(f"Error renaming {old_path}: {e}")

# Example usage
if __name__ == "__main__":
    if os.path.isdir(root_folder):
        append_folder_name_to_images(root_folder)
        print("Renaming completed.")
    else:
        print("Invalid folder path!")

import os
import shutil

# Paths to the two folders
src_folder = 'C:\\D\\DSU\\Dragomans\\CNN-labelled-Dragomans - Copy\\CNN-labelled-Dragomans\\upright - Copy'  # The folder containing 10000 files without structure
tgt_folder = 'E:\\Special_media_images\\Dragomans\\Finished'  # The folder with the desired folder structure

def replicate_structure(src_folder, tgt_folder):
    missing_list = []
    # Walk through all files and directories in the target_folder
    for root, _, files in os.walk(tgt_folder):
        for file in files:
            print(file)
            # Get the relative path of the file from the target folder root
            relative_path = os.path.relpath(os.path.join(root, file), tgt_folder)
            
            # Create the corresponding directory structure in the source folder
            target_dir = os.path.join(src_folder, os.path.dirname(relative_path))
            os.makedirs(target_dir, exist_ok=True)
            
            def clean_name(name):
                """some filenames in the target_folder have unwanted substrings 
                including left and right"""
                if 'left' in name:
                    return name.rsplit('left', 1)[0] + name.rsplit('left', 1)[1]
                elif 'right' in name:
                    return name.rsplit('right', 1)[0] + name.rsplit('right', 1)[1]
                else:
                    return name

            nm, ext = os.path.splitext(file)
            nm = clean_name(nm)
            # Source file path (without structure) and new target file path (with structure)
            src_file_path = r"\\?\\" + os.path.join(src_folder, nm+ext)
            src_file_path_right = r"\\?\\" + os.path.join(src_folder, nm + '_r' + ext)
            new_file_path = r"\\?\\" + os.path.join(target_dir, nm+ext)
            new_file_path_right = r"\\?\\" + os.path.join(target_dir, nm + '_r' + ext)
            
            # Move the file from src_folder to the new location
            found = False
            if os.path.exists(src_file_path):
                shutil.move(src_file_path, new_file_path)
                found = True
            if os.path.exists(src_file_path_right):
                shutil.move(src_file_path_right, new_file_path_right)
                found = True
            if not found:
                missing_list.append(src_file_path)

    # Get the current directory of the .py file
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Define the filename and full path for the new text file
    txt_name = "missing_list_.txt"
    txt_path = os.path.join(current_dir, txt_name)

    # Write the list to the text file
    with open(txt_path, 'w') as file:
        for item in missing_list:
            file.write(f"{item}\n")

# Call the function with the paths to your folders
replicate_structure(src_folder, tgt_folder)
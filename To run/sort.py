import os
import glob
from packaging import version

def sort_files_by_columns(input_folder, output_folder):
    # Create a new folder called 'sorted' if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # List all text files in the given folder
    files = glob.glob(os.path.join(input_folder, '*.txt'))

    for file_path in files:
        with open(file_path, 'r') as file:
            # Read lines from the file
            lines = file.readlines()

            # Sort lines based on eslint-plugin-import, version, and date
            sorted_lines = sorted(lines, key=lambda x: (
                x.split(',')[2], version.parse(x.split(',')[4]), x.split(',')[5]
            ))

        # Extract the filename from the path
        _, filename = os.path.split(file_path)

        # Create the output file path in the specified output folder
        output_file_path = os.path.join(output_folder, filename)

        # Write sorted lines to the new file in the specified output folder
        with open(output_file_path, 'w') as file:
            file.writelines(sorted_lines)

if __name__ == "__main__":
    input_folder = './clean_all_dependency_versions'
    output_folder = 'sorted_ver_dep'

    # List all text files in the given folder
    files = glob.glob(os.path.join(input_folder, '*.txt'))

    # Check if there are any text files in the input folder
    if not files:
        print("No text files found in the input folder.")
    else:
        sort_files_by_columns(input_folder, output_folder)
        print("Text files sorted successfully! Sorted files are saved in the 'sorted' folder.")

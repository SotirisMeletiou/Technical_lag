import os
from packaging import version as packaging_version

def process_file(file_path):
    max_version = packaging_version.parse("0.0.0")
    max_dependency = None

    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            if len(parts) == 3:
                version = packaging_version.parse(parts[2])
                if version > max_version:
                    max_version = version
                    max_dependency = parts[0]

    return max_dependency, str(max_version)

def main():
    folder_path = 'technical_lag'
    output_file_path = 'max_lag.txt'

    results = []

    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            max_dependency, max_version = process_file(file_path)
            # Remove ".txt" from the version in the output file
            version_without_extension = os.path.splitext(filename)[0]
            result_line = f"{version_without_extension},{max_dependency},{max_version}\n"
            results.append(result_line)

    # Sort the results by the first column (version)
    results.sort(key=lambda x: packaging_version.parse(x.split(',')[0]))

    with open(output_file_path, 'w') as output_file:
        for result in results:
            output_file.write(result)

    print(f"Output written to {output_file_path}")

if __name__ == "__main__":
    main()

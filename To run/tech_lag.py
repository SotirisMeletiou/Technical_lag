import os
import pandas as pd
from packaging import version as packaging_version

def read_dates_file(file_path):
    data = []

    if not os.path.exists(file_path):
        print(f"'{file_path}' not found.")
        return None

    with open(file_path, 'r') as file:
        for line in file:
            columns = line.split()
            if len(columns) >= 5:
                new_row = [columns[2], columns[3] + ' ' + columns[4]]
                data.append(new_row)

    df = pd.DataFrame(data, columns=['Version', 'Published Date'])
    return df

def read_clean_versions(file_path):
    with open(file_path, 'r') as version_file:
        version_data = version_file.read()

    lines = version_data.split('\n')
    new_data = []
    for line in lines:
        columns = line.split()
        if len(columns) >= 11:
            new_row = [columns[6], columns[10]]
            new_data.append(new_row)

    return pd.DataFrame(new_data, columns=['Dependency Name', 'Dependency Version'])

def read_dependency_days(file_path):
    with open(file_path, 'r') as version_file:
        version_data = version_file.read()

    lines = version_data.split('\n')
    new_data = []
    for line in lines:
        columns = line.split(',')
        if len(columns) >= 6:
            new_row = [columns[2], columns[4], columns[5]]
            new_data.append(new_row)

    return pd.DataFrame(new_data, columns=['Dependency Name', 'Dependency Version', 'Published Date'])

def calculate_days_difference(current_date, dep_day_date):
    if not pd.isnull(dep_day_date) and not pd.isnull(current_date):
        return (current_date - dep_day_date).days
    return None

def compare_versions(dep_version, day_dep_version):
    if dep_version.startswith('^'):
        # For versions that start with '^', extract the major number
        major_version_dep = int(dep_version.split('.')[0].lstrip('^'))
        major_version_day_dep = int(day_dep_version.split('.')[0].lstrip('^'))
        #print(f"{major_version_dep} , {major_version_day_dep}")
        if major_version_day_dep > major_version_dep:
            return True
        else:
            return False  # Major version of day_dep_version is not greater
    else:
        return packaging_version.parse(day_dep_version) > packaging_version.parse(dep_version)

if __name__ == '__main__':
    file_path = 'dates.txt'
    dates_df = read_dates_file(file_path)

    if dates_df is not None:
        total_versions = len(dates_df)
        for i, row in dates_df.iterrows():
            version_str = row['Version']
            version_dependency = read_clean_versions(os.path.join('clean_versions_of_depend', f'{version_str}.txt'))
            dependency_day = read_dependency_days(os.path.join('sorted_ver_dep', f'{version_str}.vd.txt'))
            
            current_date = pd.to_datetime(row['Published Date'], format='%Y-%m-%d %H:%M:%S')
           # print("\n")
            results = []
            for dep_index, dep_row in version_dependency.iterrows():
                dep_name = dep_row['Dependency Name']
                dep_version = dep_row['Dependency Version']
                dep_day_date = None
                if dep_version.startswith('^'):
                    # For versions that start with '^', extract the major number
                    major_version = dep_version.split('.')[0].lstrip('^')
                    dep_version_temp = dep_version.lstrip('^')
                    found_same_name = False
                    for day_index, day_row in dependency_day.iterrows():
                        day_dep_name = day_row['Dependency Name']
                        day_dep_version = day_row['Dependency Version'].lstrip('^')

                        if dep_name == day_dep_name and dep_version_temp==day_dep_version:
                            found_same_name=True

                        if found_same_name==True and dep_name == day_dep_name and compare_versions(dep_version, day_dep_version):
                            dep_day_date = pd.to_datetime(day_row['Published Date'], format='%Y-%m-%d %H:%M:%S')
                            break
                else:
                    # For versions that do not start with '^', find the first line with a different version
                    found_same_name = False
                    for day_index, day_row in dependency_day.iterrows():
                        day_dep_name = day_row['Dependency Name']
                        day_dep_version = day_row['Dependency Version'].lstrip('^')

                        if dep_name == day_dep_name and dep_version==day_dep_version:
                            found_same_name=True

                        if found_same_name==True and dep_name == day_dep_name and compare_versions(dep_version, day_dep_version):
                            dep_day_date = pd.to_datetime(day_row['Published Date'], format='%Y-%m-%d %H:%M:%S')
                            break

                if dep_day_date is None:
                 # No match found, use the latest version
                    dep_day_date = current_date
                    
                diff_days = calculate_days_difference(current_date, dep_day_date)
                if diff_days is not None:
                    #print(f"{current_date},{dep_day_date} , {dep_version} , {dep_name} , {day_dep_version}")
                    result_str = f"{dep_name},{dep_version},{diff_days}"
                    results.append(result_str)

            # Save results to a text file in the "technical_lag" folder
            output_folder = "technical_lag"
            os.makedirs(output_folder, exist_ok=True)

            with open(os.path.join(output_folder, f"{version_str}.txt"), "w") as output_file:
                output_file.write("\n".join(results))

            print(f"Processing for version {version_str} finished. {i+1}/{total_versions}")

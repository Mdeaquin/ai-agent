import os

def get_files_info(working_directory, directory="."):
    abs_working_dir = os.path.normpath(os.path.abspath(working_directory))
    path_to_check = os.path.normpath(os.path.abspath(os.path.join(working_directory, directory)))
    if path_to_check.startswith(abs_working_dir) is False:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(path_to_check):
        return f'Error: "{directory}" is not a directory'
    else:
        file_list = os.listdir(path_to_check)
        for file in file_list:
            file_name = file
            path_to_file = os.path.join(directory, file)
            file_size = os.path.getsize(path_to_file)
            if os.path.isfile(path_to_file) is True:
                is_dir = False
            else: 
                is_dir = True

            print(f"- {file_name}: file_size={file_size} bytes, is_dir={is_dir}")

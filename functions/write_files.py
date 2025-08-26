import os

def write_file(working_directory, file_path, content):
    abs_working_dir = os.path.normpath(os.path.abspath(working_directory))
    path_to_check = os.path.normpath(os.path.abspath(os.path.join(working_directory, file_path)))
    try:
        common = os.path.commonpath([abs_working_dir, path_to_check])
    except ValueError:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if common != abs_working_dir:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    try:
        parent_dir = os.path.dirname(path_to_check)
        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir,exist_ok=True)
        with open(path_to_check, "w", encoding="utf-8") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"

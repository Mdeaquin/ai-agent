import os
from google.genai import types
import config

def get_files_info(working_directory, directory="."):
    abs_working_dir = os.path.normpath(os.path.abspath(working_directory))
    path_to_check = os.path.normpath(os.path.abspath(os.path.join(working_directory, directory)))
    if path_to_check.startswith(abs_working_dir) is False:
        return f'    Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(path_to_check):
        return f'    Error: "{directory}" is not a directory'
    else:
        file_lines = []
        file_list = sorted(os.listdir(path_to_check), key=lambda filename: (os.path.isdir(os.path.join(path_to_check, filename)), filename))
        try:
            for file in file_list:
                file_name = file
                path_to_file = os.path.join(path_to_check, file)
                if os.path.isdir(path_to_file) is True:
                    is_dir = True
                    file_size = 0
                else:
                    is_dir = False
                    file_size = os.path.getsize(path_to_file)
                if not file_name.startswith("__"):
                    file_lines.append(f" - {file_name}: file_size={file_size} bytes, is_dir={is_dir}")

            return "\n".join(file_lines)
        except Exception as e:
            return f"    Error: An unexpected error occurred: {e}"

def get_file_content(working_directory, file_path):
    abs_working_dir = os.path.normpath(os.path.abspath(working_directory))
    path_to_check = os.path.normpath(os.path.abspath(os.path.join(working_directory, file_path)))
    if path_to_check.startswith(abs_working_dir) is False:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(path_to_check):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(path_to_check, "r", encoding="utf-8") as f:
            file_content_string = f.read(config.MAX_CHARS)
            return file_content_string
    except Exception as e:
        return f'    Error: unexpected error: "{e}"'

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the file and at a specified file path and returns the contents of the file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to read the file contents provided it exists and is a regular file"
            ),
        },
    ),
)

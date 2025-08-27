import os
import subprocess
import sys
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    abs_working_dir = os.path.normpath(os.path.abspath(working_directory))
    path_to_check = os.path.normpath(os.path.abspath(os.path.join(working_directory, file_path)))
    cmd = [sys.executable, path_to_check, *map(str, args)]
    try:
        common = os.path.commonpath([abs_working_dir, path_to_check])
    except ValueError:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if common != abs_working_dir:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(path_to_check):
        return(f'Error: File "{file_path}" not found.')
    if not path_to_check.endswith(".py"):
        return(f'Error: "{file_path}" is not a Python file.')
    try:
        result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=30,
        cwd=working_directory
        )
        stdout = result.stdout.rstrip("\n")
        stderr = result.stderr.rstrip("\n")
        if not stdout and not stderr:
            return "No output produced."

        out = f"STDOUT: {stdout}\nSTDERR: {stderr}"
        if result.returncode != 0:
            out += f"\nProcess exited with code {result.returncode}"
        return out
    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python program",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of the python program to run, as long as it exists within the working directory, and is a python file"
            ),
            "args": types.Schema(
                type=types.Type.STRING ,
                description="Arguements to be specified when running the python program"
            ),
        },
    ),
)
"""
Main module for antools. This script serves as the entry point for the antools package.
It contains the main execution logic or imports for running the package.
"""

import importlib.util
import os
import shutil
import subprocess
import sys


def init():
    """Copies all files and subdirectories from a automation_template folder inside antools to the current working directory."""

    spec = importlib.util.find_spec("antools")
    if not spec or not spec.origin:
        print("Antools library was not found!")
        return

    package_path = os.path.dirname(spec.origin)
    source_path = os.path.join(package_path, "core", "new_project_template")

    if not os.path.exists(source_path):
        print(f"Error: Could not find the folder '{source_path}' inside antools.")
        return

    dest_path = os.getcwd()  # Copy contents to the current working directory

    print(f"Copying contents from {source_path} to {dest_path}...")

    for item in os.listdir(source_path):
        src_item = os.path.join(source_path, item)
        dest_item = os.path.join(dest_path, item)

        if os.path.isdir(src_item):
            shutil.copytree(src_item, dest_item, dirs_exist_ok=True)
        else:
            shutil.copy2(src_item, dest_item)

    batch_file_path = os.path.join(os.path.dirname(__file__), "initialize.bat")
    # Run the batch file
    try:
        # subprocess.run() to execute the batch file
        result = subprocess.run(
            [batch_file_path], shell=True, text=True, capture_output=True, check=True
        )

        # Print the output (standard output and error)
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)

        # Check for success or failure
        if result.returncode == 0:
            print("Batch file executed successfully.")
        else:
            print("Error running the batch file.")

    except Exception as e:
        print(f"An error occurred: {e}")

    print("Initialization complete!")


def main():
    """Enable to run python -m antools commands"""
    if len(sys.argv) > 1 and sys.argv[1] == "init":
        init()
    else:
        print("Usages: python -m antools init (To start new project)")


if __name__ == "__main__":
    main()

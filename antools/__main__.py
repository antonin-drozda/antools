import sys
import os
import shutil
import importlib.util

def get_package_subfolder(subfolder_name):
    """Finds the path of a specific subfolder inside the antools package."""
    spec = importlib.util.find_spec("antools")
    if not spec or not spec.origin:
        return None

    package_path = os.path.dirname(spec.origin)
    subfolder_path = os.path.join(package_path, subfolder_name)

    return subfolder_path if os.path.exists(subfolder_path) else None

def init():
    """Copies all files and subdirectories from a automation_template folder inside antools to the current working directory."""
    subfolder_name = "automation_template"  # Change this to the folder inside antools
    source_path = get_package_subfolder(subfolder_name)
    
    if not source_path:
        print(f"Error: Could not find the folder '{subfolder_name}' inside antools.")
        return

    dest_path = os.getcwd()  # Copy contents to the current working directory

    try:
        print(f"Copying contents from {source_path} to {dest_path}...")

        for item in os.listdir(source_path):
            src_item = os.path.join(source_path, item)
            dest_item = os.path.join(dest_path, item)

            if os.path.isdir(src_item):
                shutil.copytree(src_item, dest_item, dirs_exist_ok=True)
            else:
                shutil.copy2(src_item, dest_item)

        print("Initialization complete!")
    except Exception as e:
        print(f"Error during initialization: {e}")

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "init":
        init()
    else:
        print("Usage: python -m antools init")

if __name__ == "__main__":
    main()
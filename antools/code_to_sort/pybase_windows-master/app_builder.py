import app_settings as sett
from distutils.dir_util import copy_tree
import PyInstaller.__main__
import os
import shutil
import re

from tests import * 

if __name__ == "__main__":

    # run unittests
    try:
        unittest.main()
    except:
        user_input = input("\nNot all unittests run successfully! Should I continue? [y/n] ")
        if not user_input.lower() == "y":
            raise SystemExit()

    # run other tests???

    # run pyinstaller
    pyinstaller_commands = list()
    pyinstaller_commands.append("--onefile")
    pyinstaller_commands.append("--windowed") if sett.APP_WITH_GUI else None
    pyinstaller_commands.append(f"--icon={sett.ICON_FILE}") if sett.ICON_FILE else None
    pyinstaller_commands.append(sett.MAIN_FILE)
    PyInstaller.__main__.run(pyinstaller_commands)

    # add files and folders
    sett.FILES_TO_ADD.append(sett.ICON_FILE) if sett.ICON_FILE else None
    for file in sett.FILES_TO_ADD:
        shutil.copyfile(os.path.join(os.getcwd(), file), os.path.join(os.getcwd(), "dist", file)) if file else None
        
    for folder in sett.FOLDERS_TO_ADD:
        copy_tree(os.path.join(os.getcwd(), folder), os.path.join(os.getcwd(), "dist", folder)) if folder else None

    # create version folder if not exists
    os.mkdir(os.path.join(os.getcwd(), sett.VERSION_FOLDER)) if not os.path.exists(os.path.join(os.getcwd(), sett.VERSION_FOLDER)) else None

    # names for build and exe file
    BUILD_FOLDER_NAME = os.path.join(os.getcwd(), sett.VERSION_FOLDER, sett.CLIENT_SCRIPT_NAME + " (" + sett.VERSION + ")")
    BUILD_EXE_NAME = re.sub(".py", "", sett.CLIENT_SCRIPT_NAME) + ".exe"

    # remove previous folder with same version
    if os.path.exists(BUILD_FOLDER_NAME): 
        print("\n")
        user_input = input("This version already exists, do you want to replace it? [Y/N] ")

        if user_input.lower() == "y":
            shutil.rmtree(BUILD_FOLDER_NAME)
        else:
            raise SystemError("Version already exists!")

    # copy distribution
    copy_tree(os.path.join(os.getcwd(), "dist"), os.path.join(BUILD_FOLDER_NAME))

    for folder in ["build", "dist"]:
        try:
            shutil.rmtree(folder)
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))

    os.rename(os.path.join(BUILD_FOLDER_NAME, re.sub(".py", ".exe", sett.MAIN_FILE)), os.path.join(BUILD_FOLDER_NAME, BUILD_EXE_NAME))
    os.remove(re.sub(".py", "", sett.MAIN_FILE) + ".spec")

    # generate zip file
    try:
        os.remove(os.path.join(os.getcwd(), sett.VERSION_FOLDER, BUILD_FOLDER_NAME))
    except:
        pass
    shutil.make_archive(os.path.join(os.getcwd(), sett.VERSION_FOLDER, BUILD_FOLDER_NAME), 
    'zip', os.path.join(os.getcwd(), sett.VERSION_FOLDER, sett.CLIENT_SCRIPT_NAME + " (" + sett.PYINSTALLER_VERSION + ")"))

    # change cwd and try to run
    os.chdir(os.path.join(os.getcwd(), BUILD_FOLDER_NAME))
    os.startfile(BUILD_EXE_NAME)

    try:
        os.remove(os.path.join(os.getcwd(), sett.VERSION_FOLDER, BUILD_FOLDER_NAME))
    except:
        pass

    # remove previous iso and exe installations
    try:
        os.remove(os.path.join(os.getcwd(), sett.VERSION_FOLDER, BUILD_FOLDER_NAME + ".iso"))
    except:
        pass

    try:
        os.remove(os.path.join(os.getcwd(), sett.VERSION_FOLDER, BUILD_FOLDER_NAME + ".exe"))
    except:
        pass

    # make iso file if wanted
    print(".\n.\n.")
    print(" ".center(50, "#"))
    print("TO CREATE WINDOWS INSTALLER .. download NSIS (https://nsis.sourceforge.io/Download)")
    print("TO CREATE ISO FILE .. download ANYTOISO (https://crystalidea.com/anytoiso/download)\n")
    print(" ".center(50, "#"))
    print(".\n.\n.")
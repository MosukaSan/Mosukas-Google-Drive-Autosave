from time import sleep

import google_drive_service
import os
import easygui
import shutil
import json
import keyboard
import platform
import threading

GDS = google_drive_service.GoogleDriveService()
system_os = platform.system()

def terminal_clear():
    if system_os == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def add_folder(save_data):
    print("Creating google drive folder...")
    folder_name = "Mosuka's Autosave"
    save_data["drive_folder"] = GDS.create_folder(folder_name)
    return save_data

def add_location(save_data):
    while True:
        print("[1] - Autosave a folder")
        print("[2] - Autosave a file")
        response = input()

        if response == "1":
            terminal_clear()
            folder_path = easygui.diropenbox(msg="Choose a folder", title="Folder selection")
            save_data["file"] = folder_path
            return save_data
        elif response == "2":
            terminal_clear()
            file_path = easygui.fileopenbox(msg="Choose a file", title="File selection")
            save_data["file"] = file_path
            return save_data
        else:
            print("Choose a valid option\n")
    
def file_upload(save_data):
    if os.path.isdir(save_data["file"]):
        print("Compressing...")
        shutil.make_archive(save_data["file"], "zip", save_data["file"])
        zip_path = save_data["file"] + ".zip"

        if os.path.exists(zip_path):
            name = os.path.basename(zip_path)
            print("Uploading...")
            GDS.upload_file(name, zip_path, save_data["drive_folder"]["id"])
            os.remove(zip_path)
            print("File upload sucessful")
        else:
            terminal_clear()
            print("Choose a valid folder\n")
    else:
        if os.path.exists(save_data["file"]):
            name = os.path.basename(save_data["file"])
            print("Uploading...")
            GDS.upload_file(name, save_data["file"], save_data["drive_folder"]["id"])
            print("File upload sucessful\n")
        else:
            terminal_clear()
            print("Choose a valid file\n")

def main():
    terminal_clear()
    print("Automatically save your files on google drive!")
    sleep(2)

    save_data = {
        "drive_folder": None,
        "file": None
    }

    GDS.authenticate()
    GDS.init_service()

    print("Login Sucessful!\n")
    terminal_clear()

    if os.path.exists("save_data.json") and os.stat("save_data.json").st_size != 0:
        while True:
            with open("save_data.json", "r", encoding="utf-8") as save_data_file:
                save_data = json.load(save_data_file)

            terminal_clear()
            print("[1] - Create google drive folder again")
            print("[2] - Change location to save")
            print("[3] - Delete all data")
            print("[4] - Logout and delete all data")
            print("[5] - Save after a specific time")
            print("[6] - Start listening ctrl+s")
            print("[7] - Exit")
            response = input()

            if response == "1":
                terminal_clear()
                save_data = add_folder(save_data)

                with open("save_data.json", "w", encoding="utf-8") as save_data_file:
                    json.dump(save_data, save_data_file, ensure_ascii=False, indent=4)
            elif response == "2":
                terminal_clear()
                save_data = add_location(save_data)
                file_upload(save_data)

                with open("save_data.json", "w", encoding="utf-8") as save_data_file:
                    json.dump(save_data, save_data_file, ensure_ascii=False, indent=4)
            elif response == "3":
                os.remove("save_data.json")
                terminal_clear()
                main()
            elif response == "4":
                os.remove("token.json")
                os.remove("save_data.json")
                terminal_clear()
                main()
            elif response == "5":
                terminal_clear()
                time_to_save = int(input("Select the time range (in minutes): "))
                stop_loop = False

                def timer_exit():
                    print("Stoping...")
                    nonlocal stop_loop
                    stop_loop = True

                def file_upload_in_other_thread():
                    file_upload(save_data)

                print("Press crtl+alt+q to stop\n")
                thread = threading.Thread(target=file_upload_in_other_thread)
                thread.start()
                keyboard.add_hotkey("ctrl+alt+q", timer_exit)

                while not stop_loop:
                    for x in range(time_to_save*60):
                        if stop_loop:
                            break
                        if x == time_to_save*60-1:
                            file_upload_in_other_thread()
                        sleep(1)

                keyboard.remove_all_hotkeys()
            elif response == "6":
                terminal_clear()
                stop_listening = False

                def activate():
                    file_upload(save_data)

                def listener_exit():
                    print("Stoping...")
                    nonlocal stop_listening 
                    stop_listening = True
                    
                keyboard.add_hotkey("ctrl+s", activate)
                keyboard.add_hotkey("ctrl+alt+q", listener_exit)
                print("Press crtl+alt+q to stop\n")

                while not stop_listening:
                    pass

                keyboard.remove_all_hotkeys()
            elif response == "7":
                exit()
            else:
                print("Choose a valid option")
    else:
        save_data = add_folder(save_data)
        terminal_clear()
        save_data = add_location(save_data)
        terminal_clear()
        file_upload(save_data)
        print("Done!")

        with open("save_data.json", "w", encoding="utf-8") as save_data_file:
            json.dump(save_data, save_data_file, ensure_ascii=False, indent=4)

        main()

if __name__ == "__main__":
    main()
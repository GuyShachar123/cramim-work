import os
import time
import win32file
import win32con
import datetime
import threading
import webbrowser
import urllib.parse

while True:
    folder = input("enter folder: ").strip()
    pic_folder = input("enter pic folder: ").strip()
    if os.path.isdir(folder) and os.path.isdir(pic_folder):
        break
    print("folder not found do again")

script_dir = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.join(script_dir, "file_monitor.log")

FILE_LIST_DIRECTORY = 0x0001
hDir = win32file.CreateFile(
    folder,
    FILE_LIST_DIRECTORY,
    win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
    None,
    win32con.OPEN_EXISTING,
    win32con.FILE_FLAG_BACKUP_SEMANTICS,
    None
)


def monitor(dir_handle, log_file_path, monitored_folder, target_pic_folder):
    pic_list = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.tiff', '.tif']

    try:
        while True:
            results = win32file.ReadDirectoryChangesW(
                dir_handle,
                1024,
                True,
                win32con.FILE_NOTIFY_CHANGE_FILE_NAME | win32con.FILE_NOTIFY_CHANGE_DIR_NAME,
                None,
                None
            )

            for action, file_name in results:
                msg = ""

                if action == 1:
                    msg = f"New file created: {file_name}"

                    ext = os.path.splitext(file_name)[1].lower()
                    if ext in pic_list:
                        src_path = os.path.join(monitored_folder, file_name)
                        dest_path = os.path.join(target_pic_folder, file_name)

                        if not os.path.isfile(dest_path):
                            success = False
                            for i in range(10):
                                try:
                                    if os.path.isfile(src_path):
                                        with open(src_path, "rb") as f:
                                            data = f.read()
                                        with open(dest_path, "wb") as f:
                                            f.write(data)
                                        print(f"-> Copied image to pic folder: {file_name}")
                                        success = True
                                        break
                                # this is the error we were getting 
                                except PermissionError:
                                    time.sleep(0.5)
                                except Exception as e:
                                    print(f"-> Error copying file: {e}")
                                    break

                            if not success:
                                print(f"-> Failed to copy {file_name}: File remained locked.")

                elif action == 2:
                    msg = f"File deleted: {file_name}"
                elif action == 4:
                    msg = f"File renamed from: {file_name}"
                elif action == 5:
                    msg = f"File renamed to: {file_name}"

                if msg:
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    log_line = f"{timestamp} - {msg}\n"
                    print(log_line.strip())
                    with open(log_file_path, "a", encoding="utf-8") as f:
                        f.write(log_line)

    except Exception:
        pass


if __name__ == "__main__":
    t = threading.Thread(target=monitor, args=(hDir, log_path, folder, pic_folder), daemon=True)
    t.start()

    while True:
        msg2 = input("exit to exit enter a pic name to look it up").strip().lower()
        if msg2 == "exit":
            win32file.CloseHandle(hDir)
            os._exit(0)
        else:
            #encoded_query = urllib.parse.quote(msg2)
            url = f"https://www.google.com/search?q={msg2}&tbm=isch"
            webbrowser.open(url)
            print(f"Opened browser search for: {msg2}")
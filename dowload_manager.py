from os import scandir, rename
from os.path import join, exists
from shutil import move
import time

import logging

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


# Source destination:
SOURCE_DIR = "C:\\Users\\lucja\\Downloads"


# Destination folders:
MUSIC_DIR = f"{SOURCE_DIR}\\Music"
VIDEO_DIR = f"{SOURCE_DIR}\\Video"
IMAGES_DIR = f"{SOURCE_DIR}\\Images"
DOCS_DIR = f"{SOURCE_DIR}\\Documents"
EXE_DIR = f"{SOURCE_DIR}\\Programs"


# Most popular extensions:
MUSIC_EXT = ['.mp3', '.acc', '.flac', '.wav', '.m4a', '.wma']
IMAGE_EXT = ['.jpeg', '.jpg', '.png', '.gif', '.tiff', '.psd', '.eps', '.ai', '.indd', '.raw', '.svg']
VIDEO_EXT = ['.mp4', '.mov', '.wmv', '.avi', '.mkv', '.avchd', '.webm']
DOCS_EXT = ['.doc', '.docx', '.odt', '.pdf', '.xls', '.xlsx', '.ppt', '.pptx', '.html', 'csv']
EXE_EXT = ['.exe', '.msi', '.py', '.wsf', '.bat', '.bin', '.com', '.jar', '.apk']


# Moving file
def move_new_file(dest, entry, name):
    if exists(f"{dest}\\{name}"):
        new_name = unique_filename(dest, name)
        old = join(dest, name)
        new = join(dest, new_name)
        rename(old, new)
    move(entry, dest)

# Adding a (number) to already existing file with:
def unique_filename(dest, name):
    dot = name.rfind('.')
    counter = 1
    while exists(f"{dest}\\{name}"):
        name = f"{name[:dot]}({str(counter)}){name[dot:]}"
        counter += 1
    return name



# Watchdog class copied from https://pythonhosted.org/watchdog/api.html#watchdog.events.FileSystemEventHandler
# and adjusted

class MoverHandler(FileSystemEventHandler):
    def on_modified(self, event):
        with scandir(SOURCE_DIR) as entries:
            for entry in entries:
                name = entry.name
                dot = name.rfind('.')

                self.audio(entry, name, dot)
                self.video(entry, name, dot)
                self.images(entry, name, dot)
                self.docs(entry, name, dot)
                self.exe(entry, name, dot)

    # Method for every file type:
    def audio(self, entry, name, dot):
        if name[dot:] in MUSIC_EXT:
            dest = MUSIC_DIR
            move_new_file(dest, entry, name)

    def video(self, entry, name, dot):
        if name[dot:] in (VIDEO_EXT):
            dest = VIDEO_DIR
            move_new_file(dest, entry, name)

    def images(self, entry, name, dot):
        if name[dot:] in (IMAGE_EXT):
            dest = IMAGES_DIR
            move_new_file(dest, entry, name)

    def docs(self, entry, name, dot):
        if name[dot:] in (DOCS_EXT):
            dest = DOCS_DIR
            move_new_file(dest, entry, name)

    def exe(self, entry, name, dot):
        if name[dot:] in (EXE_EXT):
            dest = EXE_DIR                       
            move_new_file(dest, entry, name)
           


# Watchdog sample copied from https://pythonhosted.org/watchdog/quickstart.html
# path and event_handler adjusted

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = SOURCE_DIR
    event_handler = MoverHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
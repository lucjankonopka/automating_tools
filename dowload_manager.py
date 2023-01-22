import os
import shutil
import time
import logging

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


source_dir = 'C:Users/lucja/Downloads'
# Destination folders:
music_dir = 'C:Users/lucja/Downloads/Music'
video_dir = 'C:Users/lucja/Downloads/Video'
images_dir = 'C:Users/lucja/Downloads/Images'
docs_dir = 'C:Users/lucja/Downloads/Documents'
exe_dir = 'C:Users/lucja/Downloads/Programs'
others_dir = 'C:Users/lucja/Downloads/Others'


def move_new_file(dest, entry, name):
    # file_exists = os.path.exists(dest + "/" + name)
    # if file_exists:
    #     unique_name = makeUnique(name)
    #     os.rename(entry, unique_name)
    shutil.move(entry, dest)

class MoveHandler(FileSystemEventHandler):
    def on_modified(self, event):
        with os.scandir(source_dir) as entries:
            for entry in entries:
                name = entry.name
                dest = source_dir
                if name.endswith('.wav') or name.endswith('.mp3'):
                    dest = music_dir
                elif name.endswith('.avi') or name.endswith('.mp4') or name.endswith('.mov'):
                    dest = video_dir
                elif name.endswith('.png') or name.endswith('.jpg') or name.endswith('.jpeg'):
                    dest = images_dir
                elif name.endswith('.pdf') or name.endswith('.doc') or name.endswith('.docx'):
                    dest = docs_dir
                elif name.endswith('.exe'):
                    dest = exe_dir
                else:
                    dest = others_dir
                move_new_file(dest, entry, name)
                





if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = source_dir
    event_handler = MoveHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
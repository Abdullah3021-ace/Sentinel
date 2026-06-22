import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class LogHandler(FileSystemEventHandler):
    def __init__(self, on_new_log):
        self.on_new_log = on_new_log

    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith('.log'):
            print(f'[watcher] new log detected: {event.src_path}')
            self.on_new_log(event.src_path)


def watch(path, on_new_log):
    handler = LogHandler(on_new_log)
    observer = Observer()
    observer.schedule(handler, path, recursive=False)
    observer.start()
    print(f'[watcher] watching {path} ...')
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

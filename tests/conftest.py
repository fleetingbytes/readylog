from pytest import FixtureRequest, fixture
from watchdog.events import FileModifiedEvent, FileSystemEventHandler
from watchdog.observers import Observer


@fixture
def tmp_log_file(tmp_path):
    path = tmp_path / "log" / "debug.log"
    path.parent.mkdir(parents=True, exist_ok=False)
    return path


@fixture
def app_name():
    return "test_app"


@fixture
def log_file_observer(tmp_log_file, request: FixtureRequest) -> Observer:
    expected_number_of_log_lines = request.param

    class LogFileChangeHandler(FileSystemEventHandler):
        @staticmethod
        def on_modified(event: FileModifiedEvent):
            if event.src_path.endswith(tmp_log_file.name):
                pass

    observer = Observer()
    handler = LogFileChangeHandler()
    tmp_log_file.touch()
    observer.schedule(handler, path=tmp_log_file, recursive=False)
    observer.start()
    yield observer

    with open(tmp_log_file, encoding="utf-8") as f:
        lines = f.readlines()
    number_of_log_lines = len(lines)
    assert number_of_log_lines == expected_number_of_log_lines

    observer.stop()
    observer.join()

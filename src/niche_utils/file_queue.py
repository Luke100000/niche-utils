import json
import tempfile

from fasteners import InterProcessLock


class FilesQueue:
    """
    A named, thread-safe list where mp.Queue() would not work.
    """

    def __init__(self, name: str = ".list"):
        self.name = name
        self.data_path = tempfile.gettempdir() + "/" + self.name
        self.lock_path = self.data_path + ".lock"
        self.lock = InterProcessLock(self.lock_path)
        self.set([])

    def set(self, values: list[any]):
        with self.lock:
            with open(self.data_path, "w") as f:
                f.write(json.dumps(values))

    def pop(self) -> any:
        with self.lock:
            with open(self.data_path, "r") as f:
                indices = json.load(f)
            if len(indices) == 0:
                return None
            port = indices.pop()
            with open(self.data_path, "w") as f:
                f.write(json.dumps(indices))
            return port

    def push(self, value: any):
        with self.lock:
            with open(self.data_path, "r") as f:
                indices = json.load(f)
            indices.append(value)
            with open(self.data_path, "w") as f:
                f.write(json.dumps(indices))

import gzip
import json

class Memoize:
    Persistent = 'dump.memo'
    UTF8 = 'utf-8'

    def __init__(self, fn) -> None:
        self.fn = fn
        self.memo = {}
        try:
            with gzip.open(Memoize.Persistent, 'r') as f:
                self.memo = json.loads(f.read().decode(Memoize.UTF8))
        except FileNotFoundError:
            self.memo = {}

    def __call__(self, *args):
        if args not in self.memo:
            self.memo[args] = self.fn(*args)
        return self.memo[args]

    def __del__(self) -> None:
        with gzip.open(Memoize.Persistent, 'w') as f:
            f.write(json.dumps(self.memo).encode(Memoize.UTF8))
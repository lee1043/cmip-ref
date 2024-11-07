from pathlib import Path

class Env:
    def __init__(self, expand_vars: bool) -> None: ...
    def path(self, name: str) -> Path: ...
    def read_env(
        self,
        path: str | None = None,
        recurse: bool = True,
        verbose: bool = False,
        override: bool = False,
    ) -> bool: ...

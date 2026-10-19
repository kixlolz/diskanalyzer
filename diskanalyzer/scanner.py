"""Walk a directory tree and compute sizes. Safe against errors and links."""
import os
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Node:
    path: str
    size: int = 0
    is_dir: bool = False
    children: list["Node"] = field(default_factory=list)
    error: str | None = None

    def sort_recursive(self) -> None:
        self.children.sort(key=lambda c: c.size, reverse=True)
        for c in self.children:
            c.sort_recursive()


def human(n: int) -> str:
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024:
            return f"{n:.1f}{unit}" if unit != "B" else f"{n}{unit}"
        n /= 1024
    return f"{n:.1f}PB"


def scan(root: str, max_depth: int = 32) -> Node:
    """Recursively scan a directory. Skips symlinks; records errors per node."""
    root = os.path.abspath(root)
    return _scan(Path(root), depth=0, max_depth=max_depth)


def _scan(path: Path, depth: int, max_depth: int) -> Node:
    node = Node(path=str(path), is_dir=True)
    try:
        with os.scandir(path) as it:
            for entry in it:
                try:
                    if entry.is_symlink():
                        continue
                    if entry.is_dir(follow_symlinks=False):
                        if depth >= max_depth:
                            continue
                        child = _scan(Path(entry.path), depth + 1, max_depth)
                    else:
                        st = entry.stat(follow_symlinks=False)
                        child = Node(path=entry.path, size=st.st_size, is_dir=False)
                    node.children.append(child)
                    node.size += child.size
                except (PermissionError, OSError) as e:
                    node.children.append(
                        Node(path=entry.path, is_dir=False, error=str(e))
                    )
    except (PermissionError, OSError) as e:
        node.error = str(e)
    return node
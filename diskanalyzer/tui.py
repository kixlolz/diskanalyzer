"""Textual TUI for browsing scan results."""
from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import Header, Footer, Tree, Static, Label
from textual.widgets.tree import TreeNode
from .scanner import Node, human


class DiskApp(App):
    CSS = """
    #summary { padding: 1; background: $panel; }
    #tree { height: 1fr; }
    """

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("r", "refresh", "Refresh"),
    ]

    def __init__(self, root_node: Node, root_path: str):
        super().__init__()
        self.root_node = root_node
        self.root_path = root_path

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical():
            yield Static(self._summary(), id="summary")
            yield Label("Press Enter to expand a folder · q to quit")
            yield Tree(f"{self.root_path}  [{human(self.root_node.size)}]", id="tree")
        yield Footer()

    def _summary(self) -> str:
        n = self.root_node
        errors = sum(1 for _ in self._walk_errors(n))
        return (
            f"Root: {n.path}\n"
            f"Total: {human(n.size)}   "
            f"Children: {len(n.children)}   "
            f"Permission errors: {errors}"
        )

    def _walk_errors(self, node: Node):
        if node.error:
            yield node
        for c in node.children:
            yield from self._walk_errors(c)

    def on_mount(self) -> None:
        tree = self.query_one("#tree", Tree)
        tree.root.expand()
        self._populate(tree.root, self.root_node)

    def _populate(self, tree_node: TreeNode, node: Node, depth: int = 0, limit: int = 200):
        shown = 0
        for child in node.children:
            if shown >= limit:
                tree_node.add_leaf(f"... ({len(node.children) - shown} more)")
                break
            label = (
                f"{human(child.size):>10}  "
                f"{'📁' if child.is_dir else '📄'} "
                f"{child.path.rsplit('/', 1)[-1]}"
                + ("  ⚠" if child.error else "")
            )
            if child.is_dir and child.children:
                branch = tree_node.add(label, expand=(depth == 0 and shown == 0))
                self._populate(branch, child, depth + 1, limit)
            else:
                tree_node.add_leaf(label)
            shown += 1


def run_tui(root: str) -> None:
    node = scan_and_sort(root)
    DiskApp(node, root).run()


def scan_and_sort(root: str) -> Node:
    from .scanner import scan
    node = scan(root)
    node.sort_recursive()
    return node
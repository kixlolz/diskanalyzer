from diskanalyzer.scanner import scan, human


def test_scan_sizes(tmp_path):
    (tmp_path / "a.txt").write_bytes(b"x" * 100)
    sub = tmp_path / "sub"
    sub.mkdir()
    (sub / "b.bin").write_bytes(b"y" * 900)
    node = scan(str(tmp_path))
    assert node.size == 1000
    assert len(node.children) == 2


def test_human():
    assert human(0) == "0B"
    assert human(1024) == "1.0KB"
    assert human(1024 * 1024) == "1.0MB"
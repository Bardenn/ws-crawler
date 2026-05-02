from __future__ import annotations

from pathlib import Path
import subprocess
import sys

from src.indexer import InvertedIndex


def test_non_interactive_find_auto_loads_index_and_prints_results(tmp_path: Path) -> None:
    index_path = tmp_path / "index.json"
    index = InvertedIndex()
    index.add_document("https://example.test/", "Good friends are valuable.", "Example")
    index.save(index_path)

    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "src.main",
            "--index",
            str(index_path),
            "--command",
            'find "good friends"',
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    assert "Loaded index with 1 pages" in completed.stdout
    assert "Found 1 page(s)" in completed.stdout
    assert "https://example.test/" in completed.stdout

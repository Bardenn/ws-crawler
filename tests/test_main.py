from pathlib import Path

import pytest

from src.crawler import CrawledPage, CrawlError
from src.indexer import InvertedIndex
from src.main import SearchShell, main


def test_load_and_find_commands_report_results(tmp_path: Path, capsys) -> None:
    index_path = tmp_path / "index.json"
    index = InvertedIndex()
    index.add_document("https://example.test/", "Good friends are here.", "Example")
    index.save(index_path)

    shell = SearchShell(index_path=index_path)
    shell.onecmd("load")
    shell.onecmd("find good friends")

    output = capsys.readouterr().out
    assert "Loaded index with 1 pages" in output
    assert "Found 1 page(s)" in output
    assert "https://example.test/" in output


def test_print_command_handles_missing_word(tmp_path: Path, capsys) -> None:
    index_path = tmp_path / "index.json"
    index = InvertedIndex()
    index.add_document("https://example.test/", "Existing words.", "Example")
    index.save(index_path)

    shell = SearchShell(index_path=index_path)
    shell.onecmd("load")
    shell.onecmd("print absent")

    output = capsys.readouterr().out
    assert "No index entries found for 'absent'." in output


def test_build_command_crawls_indexes_and_saves(tmp_path: Path, monkeypatch, capsys) -> None:
    index_path = tmp_path / "built.json"

    class FakeCrawler:
        def __init__(self, base_url, politeness_delay, max_pages) -> None:
            self.base_url = base_url
            self.politeness_delay = politeness_delay
            self.max_pages = max_pages

        def crawl(self) -> list[CrawledPage]:
            assert self.politeness_delay == 6.0
            assert self.max_pages == 2
            return [
                CrawledPage(
                    url="https://quotes.toscrape.com/",
                    title="Quotes",
                    text="Good friends and good books.",
                    links=[],
                )
            ]

    monkeypatch.setattr("src.main.QuoteCrawler", FakeCrawler)

    shell = SearchShell(index_path=index_path)
    shell.onecmd(f"build --max-pages 2 --output {index_path}")

    output = capsys.readouterr().out
    loaded = InvertedIndex.load(index_path)
    assert "Built index for 1 pages" in output
    assert loaded.postings_for("good")


def test_build_command_reports_crawl_error(monkeypatch, capsys) -> None:
    class FailingCrawler:
        def __init__(self, base_url, politeness_delay, max_pages) -> None:
            pass

        def crawl(self) -> list[CrawledPage]:
            raise CrawlError("offline")

    monkeypatch.setattr("src.main.QuoteCrawler", FailingCrawler)

    shell = SearchShell()
    shell.onecmd("build")

    assert "Build failed: offline" in capsys.readouterr().out


def test_shell_reports_missing_index_and_invalid_print_queries(capsys) -> None:
    shell = SearchShell()

    shell.onecmd("find good")
    shell.onecmd("print two words")

    output = capsys.readouterr().out
    assert "No index loaded" in output


def test_shell_handles_invalid_build_arguments(capsys) -> None:
    shell = SearchShell()

    shell.onecmd("build --max-pages not-a-number")

    assert "invalid int value" in capsys.readouterr().err


def test_load_command_reports_missing_index(tmp_path: Path, capsys) -> None:
    shell = SearchShell(index_path=tmp_path / "missing.json")

    shell.onecmd("load")

    assert "Run 'build' first" in capsys.readouterr().out


def test_print_command_reports_invalid_query_after_load(tmp_path: Path, capsys) -> None:
    index_path = tmp_path / "index.json"
    index = InvertedIndex()
    index.add_document("https://example.test/", "Good friends.", "Example")
    index.save(index_path)

    shell = SearchShell(index_path=index_path)
    shell.onecmd("load")
    shell.onecmd("print two words")

    assert "Please provide exactly one word" in capsys.readouterr().out


def test_print_command_outputs_existing_postings(tmp_path: Path, capsys) -> None:
    index_path = tmp_path / "index.json"
    index = InvertedIndex()
    index.add_document("https://example.test/", "Good good friends.", "Example")
    index.save(index_path)

    shell = SearchShell(index_path=index_path)
    shell.onecmd("load")
    shell.onecmd("print good")

    output = capsys.readouterr().out
    assert "Inverted index for 'good'" in output
    assert "frequency=2" in output
    assert "positions=[0, 1]" in output


def test_find_command_handles_empty_query_and_suggestions(tmp_path: Path, capsys) -> None:
    index_path = tmp_path / "index.json"
    index = InvertedIndex()
    index.add_document("https://example.test/", "Good friends.", "Example")
    index.save(index_path)

    shell = SearchShell(index_path=index_path)
    shell.onecmd("load")
    shell.onecmd("find")
    shell.onecmd("find frends")

    output = capsys.readouterr().out
    assert "Please provide a non-empty search query" in output
    assert "Suggestions:" in output
    assert "frends: friends" in output


def test_shell_exit_quit_and_emptyline() -> None:
    shell = SearchShell()

    assert shell.onecmd("exit") is True
    assert shell.onecmd("quit") is True
    assert shell.emptyline() is None


def test_main_rejects_fast_delay_for_target_site() -> None:
    with pytest.raises(SystemExit):
        main(["--delay", "0", "--command", "load"])


def test_main_runs_single_command(tmp_path: Path, capsys) -> None:
    index_path = tmp_path / "index.json"
    InvertedIndex().save(index_path)

    assert main(["--index", str(index_path), "--command", "load"]) == 0
    assert "Loaded index with 0 pages" in capsys.readouterr().out


def test_main_auto_loads_for_single_find_command(tmp_path: Path, capsys) -> None:
    index_path = tmp_path / "index.json"
    index = InvertedIndex()
    index.add_document("https://example.test/", "Good friends.", "Example")
    index.save(index_path)

    assert main(["--index", str(index_path), "--command", "find good"]) == 0

    output = capsys.readouterr().out
    assert "Loaded index with 1 pages" in output
    assert "Found 1 page(s)" in output


def test_main_enters_interactive_shell(monkeypatch) -> None:
    called = []

    def fake_cmdloop(self) -> None:
        called.append(self.index_path)

    monkeypatch.setattr(SearchShell, "cmdloop", fake_cmdloop)

    assert main([]) == 0
    assert called == [Path("data/index.json")]

from io import StringIO
from match_diff_lines import match_lines
from match_diff_lines import parse_unified_diff
from textwrap import dedent


def test_flake8_output():
    diff = parse_unified_diff(StringIO(dedent("""\
        diff --git a/match_diff_lines.py b/match_diff_lines.py
        index 72fd615..4bad740 100644
        --- a/match_diff_lines.py
        +++ b/match_diff_lines.py
        @@ -56,6 +56,7 @@ def parse_unified_diff(fd) -> dict[str, set[int]]:
                     (row, number_of_rows) = (
                         1 if not group else int(group) for group in hunk_match.groups()
                     )
        +            assert current_path is not  None
                     parsed_paths[current_path].update(range(row, row + number_of_rows))

             # We have now parsed our diff into a dictionary that looks like:
    """)))
    lines = StringIO(dedent("""\
        match_diff_lines.py:59:39: E271 multiple spaces after keyword
    """))
    errors = list(match_lines(lines, diff))
    assert errors == [
        "match_diff_lines.py:59:39: E271 multiple spaces after keyword\n"]


def test_line_num_only():
    diff = parse_unified_diff(StringIO(dedent("""\
        diff --git a/match_diff_lines.py b/match_diff_lines.py
        index 72fd615..4bad740 100644
        --- a/match_diff_lines.py
        +++ b/match_diff_lines.py
        @@ -56,6 +56,7 @@ def parse_unified_diff(fd) -> dict[str, set[int]]:
                     (row, number_of_rows) = (
                         1 if not group else int(group) for group in hunk_match.groups()
                     )
        +            assert current_path is not None
                     parsed_paths[current_path].update(range(row, row + number_of_rows))

             # We have now parsed our diff into a dictionary that looks like:
    """)))
    lines = StringIO(dedent("""\
        match_diff_lines.py:59 foo bar
    """))
    errors = list(match_lines(lines, diff))
    assert errors == [
        "match_diff_lines.py:59 foo bar\n"]


def test_line_num_only_with_column():
    diff = parse_unified_diff(StringIO(dedent("""\
        diff --git a/match_diff_lines.py b/match_diff_lines.py
        index 72fd615..4bad740 100644
        --- a/match_diff_lines.py
        +++ b/match_diff_lines.py
        @@ -56,6 +56,7 @@ def parse_unified_diff(fd) -> dict[str, set[int]]:
                     (row, number_of_rows) = (
                         1 if not group else int(group) for group in hunk_match.groups()
                     )
        +            assert current_path is not None
                     parsed_paths[current_path].update(range(row, row + number_of_rows))

             # We have now parsed our diff into a dictionary that looks like:
    """)))
    lines = StringIO(dedent("""\
        match_diff_lines.py:59: foo bar
    """))
    errors = list(match_lines(lines, diff))
    assert errors == [
        "match_diff_lines.py:59: foo bar\n"]


def test_ruff_output():
    diff = parse_unified_diff(StringIO(dedent("""\
        diff --git a/match_diff_lines.py b/match_diff_lines.py
        index 72fd615..4bad740 100644
        --- a/match_diff_lines.py
        +++ b/match_diff_lines.py
        @@ -56,6 +56,7 @@ def parse_unified_diff(fd) -> dict[str, set[int]]:
                     (row, number_of_rows) = (
                         1 if not group else int(group) for group in hunk_match.groups()
                     )
        +            assert current_path is not None
                     parsed_paths[current_path].update(range(row, row + number_of_rows))

             # We have now parsed our diff into a dictionary that looks like:
    """)))
    lines = StringIO(dedent("""\
        match_diff_lines.py:59:13: S101 Use of `assert` detected
           |
        57 |                 1 if not group else int(group) for group in hunk_match.groups()
        58 |             )
        59 |             assert current_path is not None
           |             ^^^^^^ S101
        60 |             parsed_paths[current_path].update(range(row, row + number_of_rows))
           |
    """))
    errors = list(match_lines(lines, diff))
    assert errors == [
        "match_diff_lines.py:59:13: S101 Use of `assert` detected\n"]

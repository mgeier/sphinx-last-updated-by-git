import os
from pathlib import Path
import tempfile
import time

import pytest
from sphinx.cmd.build import build_main


# Set timezone to make tests reproducible
os.environ['TZ'] = 'Factory'
try:
    time.tzset()
except AttributeError:
    # time.tzset() is only available on Unix systems
    pass

time1 = '2020-04-22 10:41:20 GMT+00:00'
time2 = '2020-04-23 07:24:08 GMT+00:00'

expected_results = {
    'index': [time1, 'defined'],
    'api': [time2, 'defined'],
    'example_module.example_function': [time2, 'undefined'],
    'search': ['None', 'undefined'],
}

test_dir = Path(__file__).parent


def run_sphinx(srcdir, **kwargs):
    with tempfile.TemporaryDirectory() as outdir:
        args = [str(srcdir), outdir, '-W']
        args.extend('-D{}={}'.format(k, v) for k, v in kwargs.items())
        result = build_main(args)
        assert result == 0
        outdir = Path(outdir)
        data = {}
        for name in expected_results:
            path = outdir / (name + '.html')
            data[name] = path.read_text().splitlines()
    return data


def test_repo_full():
    data = run_sphinx(test_dir / 'repo_full')
    assert data == expected_results


def test_untracked_no_dependencies():
    data = run_sphinx(
        test_dir / 'repo_full',
        git_untracked_check_dependencies=0,
    )
    assert data == {
        **expected_results,
        'example_module.example_function': ['None', 'undefined'],
    }


def test_untracked_show_sourcelink():
    data = run_sphinx(
        test_dir / 'repo_full',
        git_untracked_show_sourcelink=1,
    )
    assert data == {
        **expected_results,
        'example_module.example_function': [time2, 'defined'],
    }


def test_untracked_no_dependencies_and_show_sourcelink():
    data = run_sphinx(
        test_dir / 'repo_full',
        git_untracked_check_dependencies=0,
        git_untracked_show_sourcelink=1,
    )
    assert data == {
        **expected_results,
        'example_module.example_function': ['None', 'defined'],
    }


def test_repo_shallow():
    data = run_sphinx(test_dir / 'repo_shallow')
    assert data == {
        **expected_results,
        'index': ['None', 'defined'],
    }

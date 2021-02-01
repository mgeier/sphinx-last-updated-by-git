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
    import warnings
    warnings.warn('unable to set time zone')

time1 = '2020-04-22 10:41:20'
time2 = '2020-04-23 07:24:08'
time3 = '2021-01-31 20:52:36'

expected_results = {
    'index': [time1, 'defined'],
    'I 🖤 Unicode': [time3, 'defined'],
    'api': [time2, 'defined'],
    'example_module.example_function': [time2, 'undefined'],
    'search': ['None', 'undefined'],
}


def run_sphinx(subdir, **kwargs):
    srcdir = Path(__file__).parent / subdir
    with tempfile.TemporaryDirectory() as outdir:
        args = [str(srcdir), outdir, '-W', '-v']
        args.extend('-D{}={}'.format(k, v) for k, v in kwargs.items())
        result = build_main(args)
        assert result == 0
        data = {}
        for name in expected_results:
            path = Path(outdir) / (name + '.html')
            data[name] = path.read_text().splitlines()
    return data


def test_repo_full():
    data = run_sphinx('repo_full')
    assert data == expected_results


def test_untracked_no_dependencies():
    data = run_sphinx(
        'repo_full',
        git_untracked_check_dependencies=0,
    )
    assert data == {
        **expected_results,
        'example_module.example_function': ['None', 'undefined'],
    }


def test_untracked_show_sourcelink():
    data = run_sphinx(
        'repo_full',
        git_untracked_show_sourcelink=1,
    )
    assert data == {
        **expected_results,
        'example_module.example_function': [time2, 'defined'],
    }


def test_untracked_no_dependencies_and_show_sourcelink():
    data = run_sphinx(
        'repo_full',
        git_untracked_check_dependencies=0,
        git_untracked_show_sourcelink=1,
    )
    assert data == {
        **expected_results,
        'example_module.example_function': ['None', 'defined'],
    }


def test_repo_shallow():
    data = run_sphinx(
        'repo_shallow',
        suppress_warnings='git.too_shallow,',
    )
    assert data == {
        **expected_results,
        'index': ['None', 'defined'],
    }


def test_custom_timezone():
    data = run_sphinx(
        'repo_full',
        git_last_updated_timezone='Africa/Ouagadougou',
    )
    assert data == expected_results


def test_no_git(capsys):
    path_backup = os.environ['PATH']
    os.environ['PATH'] = ''
    try:
        with pytest.raises(AssertionError):
            run_sphinx('repo_full')
        assert '"git" command not found' in capsys.readouterr().err
    finally:
        os.environ['PATH'] = path_backup


def test_no_git_no_warning(capsys):
    path_backup = os.environ['PATH']
    os.environ['PATH'] = ''
    try:
        data = run_sphinx(
            'repo_full',
            suppress_warnings='git.command_not_found')
    finally:
        os.environ['PATH'] = path_backup
    for k, v in data.items():
        assert v == ['None', 'undefined']

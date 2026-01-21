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
time4 = '2026-01-15 21:13:07'  # Unicode
time5 = '2026-01-16 20:14:50'  # API docs
time6 = '2026-01-19 17:24:34'  # merge feature branch

expected_results = {
    'index': [time1, 'defined'],
    'I 🖤 Unicode': [time6, 'defined'],
    'api': [time5, 'defined'],
    'example_module.example_function': [time5, 'undefined'],
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
        'example_module.example_function': [time5, 'defined'],
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


def test_repo_shallow(capsys):
    with pytest.raises(AssertionError):
        run_sphinx('repo_shallow')
    assert 'too shallow' in capsys.readouterr().err


def test_repo_shallow_without_warning():
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


def test_exclude_patterns_srcdir_relative():
    data = run_sphinx(
        'repo_full',
        git_exclude_patterns='I 🖤 Unicode.rst',
    )
    assert data == {
        **expected_results,
        'I 🖤 Unicode': ['None', 'undefined'],
    }


def test_exclude_patterns_glob():
    data = run_sphinx(
        'repo_full',
        git_exclude_patterns='*.rst',
    )
    assert data == {
        **expected_results,
        'index': ['None', 'undefined'],
        'I 🖤 Unicode': ['None', 'undefined'],
        'api': ['None', 'undefined'],
        'example_module.example_function': ['None', 'undefined'],
    }


def test_exclude_patterns_deps_dates():
    data = run_sphinx(
        'repo_full',
        git_exclude_patterns='example_module.py',
    )
    assert data == {
        **expected_results,
        'api': [time1, 'defined'],
        'example_module.example_function': ['None', 'undefined'],
    }


def test_exclude_commits_dates():
    data = run_sphinx(
        'repo_full',
        git_exclude_commits='7f0faf7e62fdc49ef4c65d003002d454f79fa128')
    assert data == {
        **expected_results,
        'api': [time2, 'defined'],
        'example_module.example_function': [time2, 'undefined'],
    }


def test_exclude_commits_warning(capsys):
    with pytest.raises(AssertionError):
        run_sphinx(
            'repo_full',
            # TODO: remove 0a3b, merge commits should not be relevant here
            git_exclude_commits='23d25d0b7ac4604b7a9545420b2f9de84daabe73,5ce13573d9ca44d35c18c5658fbe25e486a80b40,0a3b0953293759543a20fafc3105c35d0c597588')
    assert 'due to excluded commits' in capsys.readouterr().err


def test_exclude_commits_without_warning():
    data = run_sphinx(
        'repo_full',
        suppress_warnings='git.unhandled_files',
        # TODO: remove 0a3b, see above
        git_exclude_commits='23d25d0b7ac4604b7a9545420b2f9de84daabe73,5ce13573d9ca44d35c18c5658fbe25e486a80b40,0a3b0953293759543a20fafc3105c35d0c597588')
    assert data == {
        **expected_results,
        'I 🖤 Unicode': ['None', 'undefined'],
    }

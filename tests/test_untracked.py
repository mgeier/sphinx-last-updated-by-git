from pathlib import Path
import tempfile

from sphinx.cmd.build import build_main


def create_and_run(srcdir, **kwargs):
    srcdir = Path(srcdir)
    srcdir.joinpath('conf.py').write_text("""
extensions = [
    'sphinx_last_updated_by_git',
]
templates_path = ['_templates']
""")
    srcdir.joinpath('index.rst').write_text("""
.. include:: another-file.txt
""")
    srcdir.joinpath('another-file.txt').write_text("""
This will be an untracked dependency.
""")
    srcdir.joinpath('_templates').mkdir()
    srcdir.joinpath('_templates', 'layout.html').write_text("""\
{{ last_updated }}
{% if sourcename is not defined %}un{% endif %}defined
""")
    outdir = srcdir / '_build'
    args = [str(srcdir), str(outdir), '-W', '-v']
    args.extend('-D{}={}'.format(k, v) for k, v in kwargs.items())
    result = build_main(args)
    if result != 0:
        return None
    path = outdir / 'index.html'
    return path.read_text().splitlines()


def test_without_git_repo(capsys):
    with tempfile.TemporaryDirectory() as srcdir:
        assert create_and_run(srcdir) is None
        assert 'Error getting data from Git' in capsys.readouterr().err


def test_without_git_repo_without_warning():
    with tempfile.TemporaryDirectory() as srcdir:
        data = create_and_run(srcdir, suppress_warnings='git.subprocess_error')
    assert data == ['None', 'undefined']


def test_untracked_source_files():
    test_dir = Path(__file__).parent
    with tempfile.TemporaryDirectory(dir=str(test_dir)) as srcdir:
        data = create_and_run(srcdir)
    assert data == ['None', 'undefined']

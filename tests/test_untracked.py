from pathlib import Path
import subprocess
import tempfile

import pytest
from sphinx.cmd.build import build_main


def create_and_run(srcdir, warning_is_error):
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
    args = [str(srcdir), str(outdir)]
    if warning_is_error:
        args.append('-W')
    result = build_main(args)
    assert result == 0
    path = outdir / 'index.html'
    return path.read_text().splitlines()


@pytest.mark.xfail
def test_without_git_repo():
    with tempfile.TemporaryDirectory() as srcdir:
        create_and_run(srcdir, warning_is_error=False)


def test_untracked_source_files():
    test_dir = Path(__file__).parent
    with tempfile.TemporaryDirectory(dir=str(test_dir)) as srcdir:
        data = create_and_run(srcdir, warning_is_error=True)
    assert data == ['None', 'undefined']

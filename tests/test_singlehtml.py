from pathlib import Path
import tempfile

from sphinx.cmd.build import build_main


def test_singlehtml():
    srcdir = Path(__file__).parent / 'repo_full'
    with tempfile.TemporaryDirectory() as outdir:
        args = [str(srcdir), outdir, '-W', '-v', '-b', 'singlehtml']
        result = build_main(args)
        assert result == 0
        path = Path(outdir) / 'index.html'
        data = path.read_text().splitlines()
    # NB: sourcefile is defined but empty in this case
    assert data == ['None', 'defined']

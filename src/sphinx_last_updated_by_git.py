"""Get the "last updated" time for each Sphinx page from Git."""
import datetime
from pathlib import Path
import subprocess

from sphinx.locale import _
from sphinx.util.i18n import format_date
from sphinx.util.logging import getLogger


__version__ = '0.1.0'


logger = getLogger(__name__)


class NotInRepository(Exception):
    """The file is not in a Git repo."""


def get_datetime(path):
    """Obtain the "author time" for *path* from Git."""
    path = Path(path)
    cmd = ['git', 'log', '-n1', '--pretty=format:%at', '--', path.name]
    timestamp = subprocess.check_output(
        cmd,
        cwd=path.parent,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )
    if not timestamp:
        raise NotInRepository(path)
    timestamp = int(timestamp)
    return datetime.datetime.fromtimestamp(timestamp)


def _html_page_context(app, pagename, templatename, context, doctree):
    context['last_updated'] = None
    lufmt = app.config.html_last_updated_fmt
    if lufmt is None or 'sourcename' not in context:
        return
    dates = []
    sourcefile = Path(app.confdir, pagename + context['page_source_suffix'])
    try:
        dates.append(get_datetime(sourcefile))
    except subprocess.CalledProcessError as e:
        logger.warning('Git error:\n%s', e.stderr, location=pagename)
        return
    except FileNotFoundError as e:
        logger.warning('"git" command not found: %s', e, location=pagename)
        return

    # Check dependencies (if they are in a Git repo)
    for dep in app.env.dependencies[pagename]:
        try:
            dates.append(get_datetime(Path(app.confdir, dep)))
        except Exception:
            continue

    context['last_updated'] = format_date(
        lufmt or _('%b %d, %Y'),
        date=max(dates),
        language=app.config.language)


def _config_inited(app, config):
    if config.html_last_updated_fmt is None:
        config.html_last_updated_fmt = ''


def setup(app):
    """Sphinx extension entry point."""
    app.require_sphinx('1.8')  # For "config-inited" event
    app.connect('html-page-context', _html_page_context)
    app.connect('config-inited', _config_inited)
    return {
        'version': __version__,
        'parallel_read_safe': True,
    }

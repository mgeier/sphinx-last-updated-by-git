"""Get the "last updated" time for each Sphinx page from Git."""
from datetime import datetime, timezone
from pathlib import Path
import subprocess

import sphinx.errors
from sphinx.locale import _
from sphinx.util.i18n import format_date
from sphinx.util.logging import getLogger


__version__ = '0.2.4'


logger = getLogger(__name__)


class NotInRepository(Exception):
    """The file is not in a Git repo."""


class TooShallow(Exception):
    """The file was last updated in the initial commit of a shallow clone."""


def get_datetime(path, tz):
    """Obtain the "author time" for *path* from Git."""
    path = Path(path)

    def run_command(cmd):
        return subprocess.check_output(
            cmd,
            cwd=str(path.parent),
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )

    result = run_command(
        ['git', 'log', '-n1', '--pretty=tformat:%at%n%P', '--', path.name])
    if not result:
        raise NotInRepository(path)
    timestamp, parents = result.splitlines()
    if not parents:
        # --is-shallow-repository is available since Git 2.15.
        result = run_command(['git', 'rev-parse', '--is-shallow-repository'])
        if result.rstrip('\n') == 'true':
            raise TooShallow(path)
    utc_time = datetime.fromtimestamp(int(timestamp), timezone.utc)
    return utc_time.astimezone(tz)


def _html_page_context(app, pagename, templatename, context, doctree):
    context['last_updated'] = None
    lufmt = app.config.html_last_updated_fmt
    if lufmt is None or 'sourcename' not in context:
        return
    if 'page_source_suffix' not in context:
        # This happens in 'singlehtml' builders
        assert context['sourcename'] == ''
        return
    sourcefile = Path(app.srcdir, pagename + context['page_source_suffix'])
    dates = []
    try:
        dates.append(get_datetime(
            sourcefile, app.config.git_last_updated_timezone))
    except subprocess.CalledProcessError as e:
        raise sphinx.errors.ExtensionError(e.stderr, e)
    except FileNotFoundError as e:
        raise sphinx.errors.ExtensionError('"git" command not found', e)
    except NotInRepository:
        if not app.config.git_untracked_show_sourcelink:
            del context['sourcename']
        if not app.config.git_untracked_check_dependencies:
            return
        shallow = False
    except TooShallow:
        shallow = True

    # Check dependencies (if they are in a Git repo)
    for dep in app.env.dependencies[pagename]:
        path = Path(app.srcdir, dep)
        try:
            date = get_datetime(path, app.config.git_last_updated_timezone)
        except Exception:
            continue
        else:
            dates.append(date)

    if not dates:
        if shallow:
            logger.warning(
                'Git clone too shallow', location=pagename,
                type='git', subtype='too_shallow')
        return

    date = max(dates)

    context['last_updated'] = format_date(
        lufmt or _('%b %d, %Y'),
        date=date,
        language=app.config.language)

    if app.config.git_last_updated_metatags:
        context['metatags'] += """
    <meta property="article:modified_time" content="{}" />""".format(
            date.isoformat())


def _config_inited(app, config):
    if config.html_last_updated_fmt is None:
        config.html_last_updated_fmt = ''
    if isinstance(config.git_last_updated_timezone, str):
        from babel.dates import get_timezone
        config.git_last_updated_timezone = get_timezone(
            config.git_last_updated_timezone)


def setup(app):
    """Sphinx extension entry point."""
    app.require_sphinx('1.8')  # For "config-inited" event
    app.connect('html-page-context', _html_page_context)
    app.connect('config-inited', _config_inited)
    app.add_config_value(
        'git_untracked_check_dependencies', True, rebuild='html')
    app.add_config_value(
        'git_untracked_show_sourcelink', False, rebuild='html')
    app.add_config_value(
        'git_last_updated_timezone', None, rebuild='html')
    app.add_config_value(
        'git_last_updated_metatags', True, rebuild='html')
    return {
        'version': __version__,
        'parallel_read_safe': True,
    }

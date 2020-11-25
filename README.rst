Get the "last updated" time for each Sphinx page from Git
=========================================================

This is a little Sphinx_ extension that does exactly that.

It also checks for included files and other dependencies.

If a page doesn't have a source file, its last_updated_ time is set to ``None``.

If a source file is not tracked by Git (e.g. because it has been auto-generated
on demand by autosummary_generate_) but its dependencies are, the last_updated_
time is taken from them.  If you don't want this to happen, use
``git_untracked_check_dependencies = False``.

If a source file is not tracked by Git, its HTML page doesn't get a source link.
If you do want those pages to have a sourcelink, set
``git_untracked_show_sourcelink = True``.  Of course, in this case
html_copy_source_ and html_show_sourcelink_ must also be ``True``,
and the theme you are using must support source links in the first place.

The default value for html_last_updated_fmt_ is changed
from ``None`` to the empty string.

By default, timestamps are displayed using the local time zone.
You can specify a datetime.timezone_ object
(or any ``tzinfo`` subclass instance)
with the configuration option ``git_last_updated_timezone``.
You can also use any string recognized by babel_,
e.g. ``git_last_updated_timezone = 'NZ'``.

By default, the "last updated" timestamp is added as an HTML ``<meta>`` tag.
This can be disabled by setting the configuration option
``git_last_updated_metatags`` to ``False``.

Usage
    #. Install the Python package ``sphinx-last-updated-by-git``
    #. Add ``'sphinx_last_updated_by_git'`` to ``extensions`` in your ``conf.py``
    #. Run Sphinx!

Caveats
    * When using a "Git shallow clone" (with the ``--depth`` option),
      the "last updated" commit for a long-unchanged file
      might not have been checked out.
      In this case, the last_updated_ time is set to ``None``
      (and a warning is shown during the build).

      This might happen on https://readthedocs.org/
      because they use shallow clones by default.
      The DONT_SHALLOW_CLONE_ feature should fix this.

      If you want to get rid of the warning, use this in your ``conf.py``::

          suppress_warnings = ['git.too_shallow']

    * The date might not be displayed on https://readthedocs.org/
      when using the ``sphinx_rtd_theme`` (which is their default).
      See `issue #1`_.

License
    BSD-2-Clause (same as Sphinx itself),
    for more information take a look at the ``LICENSE`` file.

Similar stuff
    | https://github.com/jdillard/sphinx-gitstamp
    | https://github.com/OddBloke/sphinx-git
    | https://github.com/MestreLion/git-tools (``git-restore-mtime``)
    | https://github.com/TYPO3-Documentation/sphinxcontrib-gitloginfo

.. _Sphinx: https://www.sphinx-doc.org/
.. _last_updated: https://www.sphinx-doc.org/en/master/
    templating.html#last_updated
.. _autosummary_generate: https://www.sphinx-doc.org/en/master/
    usage/extensions/autosummary.html#confval-autosummary_generate
.. _html_copy_source: https://www.sphinx-doc.org/en/master/
    usage/configuration.html#confval-html_copy_source
.. _html_show_sourcelink: https://www.sphinx-doc.org/en/master/
    usage/configuration.html#confval-html_show_sourcelink
.. _html_last_updated_fmt: https://www.sphinx-doc.org/en/master/
    usage/configuration.html#confval-html_last_updated_fmt
.. _datetime.timezone: https://docs.python.org/3/library/
    datetime.html#timezone-objects
.. _babel: https://babel.pocoo.org/
.. _DONT_SHALLOW_CLONE: https://read-the-docs.readthedocs.io/en/latest/
    guides/feature-flags.html
.. _issue #1: https://github.com/mgeier/sphinx-last-updated-by-git/issues/1

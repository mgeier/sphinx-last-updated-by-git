Get the "last updated" time for each Sphinx page from Git
=========================================================

This is a little Sphinx_ extension that does just that.

It also checks for included files.

If a page doesn't have a source file (or if Git is broken or whatever),
its last_updated_ time is set to ``None``.

The default value for html_last_updated_fmt_ is changed to the empty string.

Usage
    #. Install the Python package ``sphinx-last-updated-by-git``
    #. Add ``'sphinx_last_updated_by_git'`` to ``extensions`` in your ``conf.py``
    #. Run Sphinx!

Caveats
    * When using a "Git shallow clone" (with the ``--depth`` option),
      the "last updated" time for long-unchanged files
      might be more recent than expected,
      because the commit containing their last change hasn't been checked out.

      This might happen on https://readthedocs.org/
      because they use shallow clones by default.
      The DONT_SHALLOW_CLONE_ feature should fix this.

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

.. _Sphinx: https://www.sphinx-doc.org/
.. _last_updated: https://www.sphinx-doc.org/en/master/
    templating.html#last_updated
.. _html_last_updated_fmt: https://www.sphinx-doc.org/en/master/
    usage/configuration.html#confval-html_last_updated_fmt
.. _DONT_SHALLOW_CLONE: https://read-the-docs.readthedocs.io/en/latest/
    guides/feature-flags.html
.. _issue #1: https://github.com/mgeier/sphinx-last-updated-by-git/issues/1

Get the "last updated" time for each Sphinx page from Git
=========================================================

This is a little Sphinx_ extension that does just that.

It also checks for included files.

If a page doesn't have a source file (or if Git is broken or whatever),
its last_updated_ time is set to ``None``.

The default value for html_last_updated_fmt_ is changed to the empty string.

Usage
    #. Install the Python package ``sphinx-last-updated-by-git``
    #. Add ``sphinx_last_updated_by_git`` to ``extensions`` in your ``conf.py``
    #. Run Sphinx!

License
    BSD-2-Clause (same as Sphinx itself),
    for more information take a look at the ``LICENSE`` file.

Similar stuff
    | https://github.com/jdillard/sphinx-gitstamp
    | https://github.com/OddBloke/sphinx-git

.. _Sphinx: https://www.sphinx-doc.org/
.. _last_updated: https://www.sphinx-doc.org/en/master/
    templating.html#last_updated
.. _html_last_updated_fmt: https://www.sphinx-doc.org/en/master/
    usage/configuration.html#confval-html_last_updated_fmt

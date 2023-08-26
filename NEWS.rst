Version 0.3.6 (2023-08-26):
 * Support for changed behavior of ``source-read`` event in Sphinx 7.2

Version 0.3.5 (2023-05-18):
 * A few build system and test updates

Version 0.3.4 (2022-09-02):
 * Add ``git_exclude_patterns`` and ``git_exclude_commits`` features

Version 0.3.3 (2022-08-21):
 * Remove ``page_source_suffix`` from ``context`` if there is no source link

Version 0.3.2 (2022-04-30):
 * Use ``--no-show-signature`` to avoid error when ``log.showSignature`` is on
 * Properly stop ``git log`` subprocess even on error (to avoid warnings)

Version 0.3.1 (2022-03-04):
 * Handle "added" but not yet "committed" files

Version 0.3.0 (2021-02-09):
 * Refactor to make ``git`` calls per directory instead of per file,
   which makes this extension usable on big repositories
 * Raise warnings instead of errors when ``git`` is not available
   and when source files are not in a Git repo
 * Add warning subtypes ``git.command_not_found`` and ``git.subprocess_error``
 * Drop support for Python 3.5

Version 0.2.4 (2021-01-21):
 * ``srcdir`` can now be different from ``confdir``

Version 0.2.3 (2020-12-19):
 * Add timestamp as a ``<meta>`` tag

Version 0.2.2 (2020-07-20):
 * Add option ``git_last_updated_timezone``

Version 0.2.1 (2020-04-21):
 * Set ``last_updated`` to ``None`` when using a ``singlehtml`` builder

Version 0.2.0 (2020-04-25):
 * Change Git errors from warnings to proper errors
 * Change "too shallow" message to proper warning
   (with the ability to suppress with ``git.too_shallow``)
 * Explicitly use the local time zone
 * Support for Python 3.5

Version 0.1.1 (2020-04-20):
 * Don't add times for too shallow Git clones
 * Handle untracked source files, add configuration options
   ``git_untracked_check_dependencies`` and ``git_untracked_show_sourcelink``

Version 0.1.0 (2020-04-08):
   Initial release

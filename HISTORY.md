# Release v4.2 (2015-01-17)

* Fixed a bug where the full path to `/usr/bin/python` was not specified.
* Fixed a settings selection bug.
* Streamlined some verbiage within notifications.

# Release v4.1 (2015-01-14)

* Implemented auto-updating.
* Fixed a few small path bugs.

# Release v4.0 (2015-01-09)

* Added ability to inspect a vault item's fields.
* Added background updating to address slowness.
* Added ability to configure filepath to `lpass`.
* Added ability to toggle uppercase letter use in password generation.
* Added ability to toggle lowercase letter use in password generation.
* Added ability to toggle digit use in password generation.
* Added ability to toggle symbol use in password generation.
* Added ability to toggle ambiguous character avoidance in password generation.
* Modified field retrieval to use official `lpass` flags.

# Release v3.2 (2015-01-04)

* Added support for non-ASCII characters.
* Addresses slow Script Filter results.
* Modified how default configuration settings are stored.
* Modified notifications to be more streamlined.
* Fixed a bug wherein password generation would fail.

# Release v3.1 (2014-12-29)

* Entirely new settings/configuration management via `lpsettings`.
* Added ability to login to LastPass.
* Added ability to logout from LastPass.
* Added new (and slimmer) icons.
* Environment-proofed Python path in all scripts and Script Filters.

# Release v3.0 (2014-12-29)

* Shifted from Ruby to Python.
* Implemented [Alfred-Workflow](https://github.com/deanishe/alfred-workflow) (including fuzzy search, configuration management, and more).
* Added `lpbrowser` command to look up default browser's front-most tab's URL in the vault.
* Configuration management: cache timeout, default browser, number of generated password, and generated password length.
* Check for whether `lpass` is logged in.

# Release v2.0 (2014-12-16)

* Added data caching
* Added command to force data caching
* Added ability to specify path to `lpass` executable
* Added fallback lookup for `lpass` executable
* Changed `lpvs` command to look at vault item name *and* URL
* Major code refactoring

# Release v1.0 (2014-12-16)

* Added ability to search a LastPass vault.
* Added ability to launch URL of LastPass item.
* Added ability to copy username of LastPass item.
* Added ability to copy password of LastPass item.
* Added ability to generate a random password.
* Created documentation.

# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).




## [Unreleased]

### Added
- An `auth_token` parameter for `caosdb.configure_connection(...)`. This parameter accepts a plain text auth token (which can only be issued by the CaosDB Server). Under the hood, auth tokens are stored plain, instead of urlencoded now.
- New type of exception: `ConfigurationException` for misconfigurations.
- Some unit tests, mainly for the `caosdb.connection.authentication` module
* Advanced setup.py for easy versioning and publication as pypi repository.

### Changed
- [pytest](https://docs.pytest.org/en/latest/) is the new preferred unit test frame work.
- If a password is specified in the configuration even though the password_method is not set to `plain`, a warning is logged.
- Under the hood, the password of from a `pass` or `keyring` call is not stored anymore. Instead the password is requested each time a login is necessary.
- Always load system default CA repository into the ssl context


### Deprecated
- Unit test frame work: [Nose](https://nose.readthedocs.io/en/latest/) should not be used anymore. Please use [pytest](https://docs.pytest.org/en/latest/) instead.

### Fixed
- #1 - Problems with pass as a credentials provider
- #3 - Python client does login before the first request to circumvent problems
  with anonymous role.



## [0.1.0] - 2018-10-09
Tag `v0.1` - Commit 6fc0dcaa


### Added
- everything

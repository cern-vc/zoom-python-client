# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.3] - 2026-02-17

### Changed
- Allow calling streaming status with a settings object (support for transcriptions)

## [0.2.2] - 2023-08-30

### Added
- Calendars component for interacting with Zoom calendar resources
- Tests for calendars component
- Example script for interacting with calendars

### Changed
- Updated documentation with new calendar endpoints

## [0.2.1] - 2023-08-29

### Changed
- Upgraded project dependencies
- Updated dev dependencies

### Fixed
- Fixed test returning content on 204 status
- Removed debug logging from production code

## [0.2.0] - 2023-07-12

### Added
- Zoom Rooms component for interacting with Zoom Rooms API
- Example script to interact with Zoom Rooms
- Tests for Rooms component
- Utility function to create dict from TypedDict with NotRequired fields

### Changed
- Improved typed dict parameters to work with `from` and `to` date fields
- Renamed `generate_parameters_dict` function
- Simplified `get_project_dir()` function

### Fixed
- Fixed typo in import inside example in README
- Fixed typo in CONTRIBUTING.md

## [0.1.1] - 2023-06-01

### Added
- Retry mechanism for generating a new token on 401 responses
- Support for loading/saving access token from/to file system
- Poetry for dependency management

### Changed
- Changed LICENSE to MIT
- Set minimum dependencies instead of strict versions
- Lowered minimum required requests version to 2.23.0
- Added Pypi install instructions to README
- Published beta version on PyPI

## [0.1.0] - 2023-05-30

### Changed
- Set minimum dependencies instead of strict versions

## [0.0.6] - 2023-05-30

### Added
- Support for loading and saving access token from/to file

## [0.0.5] - 2023-05-22

### Changed
- Lowered the minimum required requests version to 2.23.0

## [0.0.4] - 2023-05-15

### Added
- Retry mechanism on 401 unauthorized responses

## [0.0.3] - 2023-05-05

### Added
- Resolution parameter support for live streams

## [0.0.2] - 2023-05-05

### Added
- Meeting token endpoint (`get_meeting_token`)
- Updated workflows

## [0.0.1] - 2023-05-05

### Added
- Initial release
- Server-to-Server OAuth token support
- `ZoomApiClient` with `init_from_env` and `init_from_dotenv` methods
- Users component with `get_user` and `get_user_meetings` endpoints
- Meetings component with `get_meeting` endpoint
- Meeting livestreams component
- Webinars component
- Webinar livestreams component
- Logging utilities
- Pre-commit hooks with mypy, isort, flake8, and black
- GitHub Actions for testing, pre-commit, and CodeQL analysis
- Code coverage reporting with codecov

[0.2.3]: https://github.com/cern-vc/zoom-python-client/compare/v0.2.2...v0.2.3
[0.2.2]: https://github.com/cern-vc/zoom-python-client/compare/v0.2.1...v0.2.2
[0.2.1]: https://github.com/cern-vc/zoom-python-client/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/cern-vc/zoom-python-client/compare/v0.1.1...v0.2.0
[0.1.1]: https://github.com/cern-vc/zoom-python-client/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/cern-vc/zoom-python-client/compare/v0.0.6...v0.1.0
[0.0.6]: https://github.com/cern-vc/zoom-python-client/compare/0.0.5...v0.0.6
[0.0.5]: https://github.com/cern-vc/zoom-python-client/compare/0.0.4...0.0.5
[0.0.4]: https://github.com/cern-vc/zoom-python-client/compare/0.0.3...0.0.4
[0.0.3]: https://github.com/cern-vc/zoom-python-client/compare/0.0.2...0.0.3
[0.0.2]: https://github.com/cern-vc/zoom-python-client/compare/0.0.1...0.0.2
[0.0.1]: https://github.com/cern-vc/zoom-python-client/releases/tag/0.0.1

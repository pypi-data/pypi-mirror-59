from typing import Optional

import questionary
from packaging.version import Version

from commitizen import bump, factory, git, out
from commitizen.config import BaseConfig

NO_COMMITS_FOUND = 3
NO_VERSION_SPECIFIED = 4
NO_PATTERN_MAP = 7
COMMIT_FAILED = 8
TAG_FAILED = 9


class Bump:
    """Show prompt for the user to create a guided commit."""

    def __init__(self, config: BaseConfig, arguments: dict):
        self.config: BaseConfig = config
        self.arguments: dict = arguments
        self.parameters: dict = {
            **config.settings,
            **{
                key: arguments[key]
                for key in [
                    "dry_run",
                    "tag_format",
                    "prerelease",
                    "increment",
                    "bump_message",
                ]
                if arguments[key] is not None
            },
        }
        self.cz = factory.commiter_factory(self.config)

    def is_initial_tag(self, current_tag_version: str, is_yes: bool = False) -> bool:
        """Check if reading the whole git tree up to HEAD is needed."""
        is_initial = False
        if not git.tag_exist(current_tag_version):
            if is_yes:
                is_initial = True
            else:
                out.info(f"Tag {current_tag_version} could not be found. ")
                out.info(
                    (
                        "Possible causes:\n"
                        "- version in configuration is not the current version\n"
                        "- tag_format is missing, check them using 'git tag --list'\n"
                    )
                )
                is_initial = questionary.confirm("Is this the first tag created?").ask()
        return is_initial

    def find_increment(self, commits: list) -> Optional[str]:
        bump_pattern = self.cz.bump_pattern
        bump_map = self.cz.bump_map
        if not bump_map or not bump_pattern:
            out.error(f"'{self.config.settings['name']}' rule does not support bump")
            raise SystemExit(NO_PATTERN_MAP)
        increment = bump.find_increment(
            commits, regex=bump_pattern, increments_map=bump_map
        )
        return increment

    def __call__(self):
        """Steps executed to bump."""
        try:
            current_version_instance: Version = Version(self.parameters["version"])
        except TypeError:
            out.error("[NO_VERSION_SPECIFIED]")
            out.error("Check if current version is specified in config file, like:")
            out.error("version = 0.4.3")
            raise SystemExit(NO_VERSION_SPECIFIED)

        # Initialize values from sources (conf)
        current_version: str = self.config.settings["version"]
        tag_format: str = self.parameters["tag_format"]
        bump_commit_message: str = self.parameters["bump_message"]
        current_tag_version: str = bump.create_tag(
            current_version, tag_format=tag_format
        )
        version_files: list = self.parameters["version_files"]
        dry_run: bool = self.parameters["dry_run"]

        is_yes: bool = self.arguments["yes"]
        prerelease: str = self.arguments["prerelease"]
        increment: Optional[str] = self.arguments["increment"]
        is_files_only: Optional[bool] = self.arguments["files_only"]

        is_initial = self.is_initial_tag(current_tag_version, is_yes)
        commits = git.get_commits(current_tag_version, from_beginning=is_initial)

        # No commits, there is no need to create an empty tag.
        # Unless we previously had a prerelease.
        if not commits and not current_version_instance.is_prerelease:
            out.error("[NO_COMMITS_FOUND]")
            out.error("No new commits found.")
            raise SystemExit(NO_COMMITS_FOUND)

        if increment is None:
            increment = self.find_increment(commits)

        # Increment is removed when current and next version
        # are expected to be prereleases.
        if prerelease and current_version_instance.is_prerelease:
            increment = None

        new_version = bump.generate_version(
            current_version, increment, prerelease=prerelease
        )
        new_tag_version = bump.create_tag(new_version, tag_format=tag_format)
        message = bump.create_commit_message(
            current_version, new_version, bump_commit_message
        )

        # Report found information
        out.write(message)
        out.write(f"tag to create: {new_tag_version}")
        out.write(f"increment detected: {increment}")

        # Do not perform operations over files or git.
        if dry_run:
            raise SystemExit()

        bump.update_version_in_files(current_version, new_version.public, version_files)
        if is_files_only:
            raise SystemExit()

        self.config.set_key("version", new_version.public)
        c = git.commit(message, args="-a")
        if c.err:
            out.error('git.commit errror: "{}"'.format(c.err.strip()))
            raise SystemExit(COMMIT_FAILED)
        c = git.tag(new_tag_version)
        if c.err:
            out.error(c.err)
            raise SystemExit(TAG_FAILED)
        out.success("Done!")

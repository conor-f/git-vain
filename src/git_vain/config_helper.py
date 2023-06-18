import os
import logging
import sys
import yaml

# TODO: Set up logging better.
logger = logging.getLogger("git-vain")
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.DEBUG)


class Config():
    def __init__(
        self,
        config_filepath=os.environ.get(
            "GITVAIN_CONFIG_FILEPATH",
            "/gitvain_config.yaml"
        )
    ):
        """
        Wraps the config getting. This has a rough heirarchy of preferring ENV
        vars, then anything from the config filepath, and finally dumb
        defaults.
        """
        self.file_config = self.get_config_from_file(config_filepath)

    @staticmethod
    def get_config_from_file(config_filepath: str) -> dict:
        """
        Given a filepath (that may or may not exit), return a dict of the
        contents of the file. It should be a yaml file (even though I despise
        it as a format). If the file doesn't exist, return an empty dict.

        Am using yaml as the repos are defined as a list and it doesn't feel
        natural to put a list of strings in an env var. This may change later.
        """
        try:
            if os.path.exists(config_filepath):
                with open(config_filepath, "r") as fh:
                    config = yaml.safe_load(fh)
                    return config if config else {}
        except Exception as e:
            logger.warning({
                "message": "Error getting config file",
                "config_filepath": config_filepath,
                "exception": str(e)
            })

            return {}

    def get(self, key, default=None):
        """
        Returns the key from the config. Operates on the heirarchy of ENV var
        -> config file -> default.
        """
        print(key)
        print(self.file_config)
        print(default)

        return os.environ.get(
            key,
            self.file_config.get(
                key,
                default
            )
        )

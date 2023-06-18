import os

from github import Github

from git_vain.config_helper import Config


class GitVainClient():
    """
    Simple wrapper around PyGithub to get an authenticated/unauthenticated
    client and to find any changes in stargazers on repos.
    """
    def __init__(self):
        self.client = self.get_client()

    def get_client(self):
        return Github(Config().get("PYGITHUB_TOKEN", None))

    def get_stargazers(self, repo_name):
        # TODO: Is a paginated list. See if this affects things.
        return list(self.client.get_repo(repo_name).get_stargazers())

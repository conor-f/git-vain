import os

from github import Github

# TODO: Name this more generically
from git_vain.git_vain_stargazer import GitVainStargazer


class GitVainClient():
    """
    Simple wrapper around PyGithub to get an authenticated/unauthenticated
    client and to find any changes in stargazers on repos.
    """
    def __init__(self):
        self.client = self.get_client()

    def get_client(self):
        return Github(os.environ.get("PYGITHUB_TOKEN", None))

    def get_stargazers(self, repo_name):
        # TODO: Is a paginated list. See if this affects things.
        return [
            GitVainStargazer(stargazer)
            for stargazer in self.client.get_repo(repo_name).get_stargazers_with_dates()
        ]

    def get_followers(self, user_name):
        """
        Given a string user name, return a list of all followers in a
        simplified object.
        """
        return [
            GitVainStargazer(user)
            for user in self.client.get_user(user_name).get_followers()
        ]

    def get_current_watchers(self, identifier):
        """
        This distinguishes between a repo, a user, a gist etc and returns back
        the simplified list of users that are currently watching this resource.
        """
        # Assume a repo if scoped with a "/" as users can't have a slash
        # character in their login:
        if "/" in identifier:
            return self.get_stargazers(identifier)
        else:
            return self.get_followers(identifier)

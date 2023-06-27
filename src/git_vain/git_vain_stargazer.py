from github.NamedUser import NamedUser
from github.Stargazer import Stargazer


class GitVainStargazer():
    """
    Simplified version of the PyGithub Stargazer/NamedUser class.
    """
    def __init__(self, stargazer):
        # TODO: Add more details for better notifications
        if isinstance(stargazer, Stargazer):
            stargazer = stargazer.user

        self.login = stargazer.login
        self.name = stargazer.login

    def __eq__(self, other):
        return self.login == other.login

    def __hash__(self):
        return hash(self.login)

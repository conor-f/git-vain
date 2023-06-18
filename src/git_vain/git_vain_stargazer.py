class GitVainStargazer():
    """
    Simplified version of the PyGithub Stargazer/NamedUser class.
    """
    def __init__(self, stargazer):
        # TODO: Add more details for better notifications
        self.login = stargazer.user.login
        self.name = stargazer.user.login

    def __eq__(self, other):
        return self.login == other.login

    def __hash__(self):
        return hash(self.login)

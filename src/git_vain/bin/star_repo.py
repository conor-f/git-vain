import argparse
import yaml

from github import Github


def parse_args():
    """
    Returns args including:
    args.star == [True | False]
    args.unstar == [True | False]
    args.follow_user == [True | False]
    args.unfollow_user == [True | False]

    args.identifier == str

    identifier acts as either a repo name or a user depending on context
    """
    parser = argparse.ArgumentParser()

    star_action_group = parser.add_mutually_exclusive_group(required=False)
    star_action_group.add_argument("--star", action="store_true")
    star_action_group.add_argument("--unstar", action="store_true")

    follow_action_group = parser.add_mutually_exclusive_group(required=False)
    follow_action_group.add_argument("--follow-user", action="store_true")
    follow_action_group.add_argument("--unfollow-user", action="store_true")

    parser.add_argument("identifier")

    return parser.parse_args()

def get_auth_token() -> str:
    """
    Returns the Github auth token stored in the gh CLI config file.
    """
    with open("/home/conor/.config/gh/config.yml", "r") as fh:
        return yaml.safe_load(fh)["hosts"]["github.com"]["oauth_token"]

def main():
    args = parse_args()
    client = Github(get_auth_token())

    if args.star:
        client.get_user().add_to_starred(client.get_repo(args.identifier))
    elif args.unstar:
        client.get_user().remove_from_starred(client.get_repo(args.identifier))
    elif args.follow_user:
        client.get_user().add_to_following(client.get_user(args.identifier))
    elif args.unfollow_user:
        client.get_user().remove_from_following(client.get_user(args.identifier))
    else:
        print("No action taken")


if __name__ == "__main__":
    main()

import argparse
import yaml

from github import Github


def parse_args():
    """
    Returns args including:
    args.star == [True | False]
    args.unstar == [True | False]
    args.repo_name == str
    """
    parser = argparse.ArgumentParser()

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--star", action="store_true")
    group.add_argument("--unstar", action="store_true")

    parser.add_argument("repo_name")

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

    print(args.repo_name)
    if args.star:
        client.get_user().add_to_starred(client.get_repo(args.repo_name))
    elif args.unstar:
        client.get_user().remove_from_starred(client.get_repo(args.repo_name))
    else:
        print("No action taken")


if __name__ == "__main__":
    main()

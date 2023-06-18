import logging
import os
import requests
import sched
import sys
import time

from git_vain.git_vain_client import GitVainClient


# TODO: Set up logging better.
logger = logging.getLogger("git-vain")
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.DEBUG)

def get_repos():
    logger.info("Getting repos...")
    return [
        "conor-f/git-vain"
    ]

def get_change_in_stargazers(repo, stargazers):
    logger.info(f"Calculating change in stargzers for {repo}")
    return stargazers[-1] if stargazers else []

def format_message(details):
    return f"""Git Vain Updates for {details["repo_name"]}: {details["stargazers_diff"]}"""

def send_update(details):
    logger.info("Sending update!")
    requests.post(
        os.environ.get(
            "GITVAIN_NTFY_ENDPOINT",
            "https://ntfy.sh/gitvain"
        ),
        data=format_message(details)
    )

def send_updates(updates_list):
    for update in updates_list:
        send_update(update)

def get_updates(scheduler):
    logger.info("Beginning to get updates...")
    scheduler.enter(
        os.environ.get("GITVAIN_UPDATE_DELAY", 60),
        1,
        get_updates,
        (scheduler,)
    )

    client = GitVainClient()

    updates = []

    for repo_name in get_repos():
        stargazers = client.get_stargazers(repo_name)
        stargazers_diff = get_change_in_stargazers(repo_name, stargazers)

        if stargazers_diff is not None:
            updates.append({
                "repo_name": repo_name,
                "stargazers_diff": stargazers_diff
            })

    # TODO: Check if it's the first run and if so give some sort of
    # notification to show it's working.
    send_updates(updates)

def entrypoint():
    logger.info("git_vain running!")

    scheduler = sched.scheduler(time.time, time.sleep)
    get_updates(scheduler)
    scheduler.run()

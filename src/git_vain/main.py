import logging
import os
import requests
import sched
import shelve
import sys
import time

from apprise import Apprise

from git_vain.git_vain_client import GitVainClient


# TODO: Set up logging better.
logger = logging.getLogger("git-vain")
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.DEBUG)

def expand_wildcard_location(location: str) -> list:
    return GitVainClient().get_repos(location.split("/")[0])

def expand_wildcard_locations(locations: list) -> list:
    """
    Given a list of locations, potentially containing some with wildcards,
    expand all wildcards into just a flat list of repos.

    e.g. The user conor-f has 3 repos A, B and C. If the locations param is
    ["conor-f/*"], the returned list should be ["conor-f/A", "conor-f/B",
    "conor-f/C"]
    """
    expanded_locations = []

    for location in locations:
        if location[-1] == "*":
            expanded_locations.extend(expand_wildcard_location(location))
        else:
            expanded_locations.append(location)

    return expanded_locations

def get_repos():
    """
    Returns a list of locations to watch. This should be named more generically
    than repos as there can also be users passed. Eventually should support
    gists too I guess.
    """
    logger.info("Getting repos...")

    locations = os.environ.get("GITVAIN_WATCHED_LOCATIONS", None)
    locations = locations.split(",") if locations else []

    expanded_locations = expand_wildcard_locations(locations)

    locations = list(set(expanded_locations))
    logger.info(f"Got repos: {locations}")

    return locations

def get_previous_stargazers(repo_name):
    with shelve.open(
        os.environ.get("GITVAIN_SHELF_PATH", "./gitvain_shelf")
    ) as shelf:
        return shelf.get("previous_stargazers", {}).get(repo_name, set())

def get_change_in_stargazers(repo_name, stargazers):
    logger.info(f"Calculating change in stargzers for {repo_name}")

    previous_stargazers = get_previous_stargazers(repo_name)
    stargazers = set(stargazers)
    diff = stargazers.symmetric_difference(previous_stargazers)

    result = []
    for stargazer in diff:
        if stargazer in stargazers:
            change = "starred"
        else:
            change = "unstarred"

        result.append({
            "direction": change,
            "details": stargazer
        })

    return result

def update_stargazers(repo_name, stargazers):
    logger.info(f"Updating stargzers for repo {repo_name}")

    with shelve.open(
        os.environ.get("GITVAIN_SHELF_PATH", "./gitvain_shelf"),
        writeback=True
    ) as shelf:
        if "previous_stargazers" not in shelf:
            shelf["previous_stargazers"] = dict()

        shelf["previous_stargazers"][repo_name] = set(stargazers)

def format_message(details):
    message = ""

    for change in details["stargazers_diff"]:
        message += f"""{change["details"].login} just {change["direction"]} {details["repo_name"]}\n"""

    # TODO: Format this nicer:
    return details["repo_name"], message

def get_notification_client():
    """
    Return a notification client configured with notifiers to send
    notifications with.
    """
    notification_client = Apprise()

    notification_config_file = os.environ.get(
        "GITVAIN_NOTIFICATIONS_FILE",
        None
    )
    notification_config_list = os.environ.get(
        "GITVAIN_NOTIFICATIONS_LIST",
        []
    )

    if notification_config_file:
        print("Adding notification handlers from config file...")
        notification_client.add(
            apprise.AppriseConfig(notification_config_file)
        )

    for notification_config_element in notification_config_list.split(","):
        print("Adding notification handler from notifications list...")
        print(notification_config_element)

        notification_client.add(notification_config_element)

    # Just for testing:
    notification_client.add("dbus://")

    return notification_client

def send_update(details):
    logger.info("Sending update!")
    notification_client = get_notification_client()

    title, message = format_message(details)

    notification_client.notify(
        title=title,
        body=message,
    )

def send_updates(updates_list):
    for update in updates_list:
        send_update(update)

def get_updates(scheduler):
    logger.info("Beginning to get updates...")
    scheduler.enter(
        int(os.environ.get("GITVAIN_UPDATE_DELAY", 60)),
        1,
        get_updates,
        (scheduler,)
    )

    client = GitVainClient()

    updates = []

    for repo_name in get_repos():
        logger.info(f"Getting updates for {repo_name}")
        stargazers = client.get_current_watchers(repo_name)
        stargazers_diff = get_change_in_stargazers(repo_name, stargazers)

        logger.info("Got stargazers and diff succesfully")
        if stargazers_diff:
            update_stargazers(repo_name, stargazers)

            updates.append({
                "repo_name": repo_name,
                "stargazers_diff": stargazers_diff
            })
        else:
            logger.info("No change in stargazers")

    # TODO: Check if it's the first run and if so give some sort of
    # notification to show it's working.
    send_updates(updates)

def entrypoint():
    logger.info("git_vain running!")

    scheduler = sched.scheduler(time.time, time.sleep)
    get_updates(scheduler)
    scheduler.run()

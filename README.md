### _Everyone's a little vain..._

&nbsp;
# Git Vain Overview

git-vain is a simple polling service that will notify you whenever a user or a repo has a change in followers. It does this using [Apprise](https://github.com/caronc/apprise) for many different notification channels and [PyGithub](https://github.com/PyGithub/PyGithub) to interact with Github. Check out a complete buildlog [here](https://blog.randombits.host/git-vain/).

### Usage
To run, you can take the `docker-compose.yaml.prod` file and modify it as needed to fit your `Caddy`, `Traefik`, or similar stack.

Alternatively, for a more quick-and-dirty approach, you can just pull the image from Docker Hub and pass environment variables directly to the container:

```
$ docker run -d \
-e GITVAIN_WATCHED_LOCATIONS=conor-f,conor-f/spotibar \
-e GITVAIN_UPDATE_DELAY=30 \
-e GITVAIN_NOTIFICATIONS_LIST="ntfy://ntfy.sh/gitvain" \
conorjf/git-vain
```

For development and modification purposes, clone the repo, then pass arguments to the `Make` rule like follows:

```
$ GITVAIN_WATCHED_LOCATIONS=conor-f \
GITVAIN_UPDATE_DELAY=30 \
GITVAIN_NOTIFICATIONS_LIST="ntfy://ntfy.sh/gitvain" \
make build run
```

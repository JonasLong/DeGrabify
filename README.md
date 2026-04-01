[![Filter List Update](https://github.com/JonasLong/DeGrabify/actions/workflows/gist-update.yml/badge.svg)](https://github.com/JonasLong/DeGrabify/actions/workflows/gist-update.yml)

# DeGrabify
  Provides an up-to-date list of Grabify domains, for use by adblockers.\
  The goal of this project is to reduce the risk of being doxxed by unknowingly clicking on IP logger links.\
  This project is not associated with Grabify.

  This project is made up of two parts:
  - A client which periodically retrieves a list of domains offered by the IP Logger service Grabify
  - A webserver which provides this list of domains to adblock clients

  Compatible with uBlock Origin / AdBlockPlus (ABP), uBlacklist, and Hosts files\
  Easily self-hosted with Docker or compatible virtualization\
  Uses Flask, Python requests, and TinyDB

# Pre-built filters
  The client/server are run daily by CI, and the updated lists are pushed to [this gist](https://gist.github.com/JonasLong/82e98e4072ba592f130edc53cdaa386d). If you only want the current filter list, without running your own server, use this. Note that the filter lists in this gist will not preserve historical changes over time, only the domains that are currently in-use.

  - [uBlock/ABP filter](https://gist.githubusercontent.com/JonasLong/82e98e4072ba592f130edc53cdaa386d/raw/6f2f8c27a139f9a530c92ab0b883001f956e1760/DeGrabify%2520uBlock%2520Blocklist) or [Subscribe via uBlock/ABP](https://subscribe.adblockplus.org?location=https%3A%2F%2Fgist.githubusercontent.com%2FJonasLong%2F82e98e4072ba592f130edc53cdaa386d%2Fraw%2F6f2f8c27a139f9a530c92ab0b883001f956e1760%2FDeGrabify%252520uBlock%252520Blocklist&amp;title=DeGrabify%20uBlock%20Blocklist)
  - [uBlacklist filter](https://gist.githubusercontent.com/JonasLong/82e98e4072ba592f130edc53cdaa386d/raw/6f2f8c27a139f9a530c92ab0b883001f956e1760/DeGrabify%2520uBlacklist%2520Blocklist) or [Subscribe via uBlacklist](https://ublacklist.github.io/rulesets/subscribe?url=https://gist.githubusercontent.com/JonasLong/82e98e4072ba592f130edc53cdaa386d/raw/6f2f8c27a139f9a530c92ab0b883001f956e1760/DeGrabify%252520uBlacklist%252520Blocklist)
  - [plain URL list](https://gist.githubusercontent.com/JonasLong/82e98e4072ba592f130edc53cdaa386d/raw/6f2f8c27a139f9a530c92ab0b883001f956e1760/DeGrabify%2520Plain%2520Domain%2520Blocklist)

# Setup

  You can run this project in [Docker](#docker) or [locally](#run-locally-no-docker). Docker is recommended.

  TLDR: `git clone`, edit `.docker/single-container-compose.yml`, `./.docker/single-build.sh`. For a reverse proxy, forward the server through nginx/caddy/etc, get the forwarded URL. In the compose file, set the base proxied domain, set the proxy level `-p`, disable the exposed port, and connect the server to your bridge network.

## Docker

 ### Server
  - Clone this repository
    - `git clone https://github.com/JonasLong/DeGrabify`
    - `cd DeGrabify`
  - Consider using a reverse proxy as described [below](#run-behind-a-reverse-proxy)
  - Configure the container in `.docker/single-container-compose.yml` (or `.docker/dual-container-compose.yml`)
  - `./.docker/single-build.sh` (or `./.docker/dual-build.sh`)
  - Continue to the [Client section](#client)

  ### Updating
  - `git fetch`
  - `git pull`
    - You may need to `git stash` if you've made changes to the config, then merge your stashed changes into main
  - `./.docker/single-build.sh` (or `./.docker/single-build.sh`)

  ### Run behind a reverse proxy
  - Change the `-p` value in the `commands` section of the server config from `0` to `1`
  - Uncomment both `networks:` sections in the compose file. Change the `name: default` value to the name of your bridge network
    - This will ensure that the server is connected to the same [external bridge network](https://docs.docker.com/compose/how-tos/networking/) that your reverse proxy is running on.
  - Comment out the `ports:` section
  - Change the `-s` option in server/server.py from `http://127.0.0.1:5000` to the base domain your server will be hosted on (e.g. `https://degrab.example.com`). If this is set incorrectly, the "Subscribe" buttons won't work but nothing else will be affected.
  - Configure your reverse proxy
    - scheme: `http`
    - domain: `degrabify-aio-1` (or `degrabify-server-1`)
    - port: `5000`

  ### Development
  - Clone this repository
    - `git clone https://github.com/JonasLong/DeGrabify`
    - `cd DeGrabify`
  - Rebuild the container with `./.docker/single-build.sh` (or `./.docker/single-build.sh`)
  - It may be helpful to convert the `db` volume to a bind mount if you need visibility into the sites.json
  - To make changes with docker compose, reference the current compose file. E.g.: `docker compose -f .docker/dual-container-compose.yml --project-directory . logs --follow` to view compose logs when running the dual-compose container. If using single-compose it may be easier to reference the container by name instead of using docker compose 

  ### Client
  To install with your adblock or Hosts file:
  - Navigate to the webserver address in a browser
  - Click the relevant subscribe link, or follow the instructions in [uBlockOrigin-HUGE-AI-Blocklist](https://github.com/laylavish/uBlockOrigin-HUGE-AI-Blocklist) for the provided URLs.
  - Most likely you'll go to uBlock or uBlacklist and import a filter, passing it the URL
  - Don't copy-paste the list of domains into your filter list- it won't auto-update as the grabify domains change 
 
## Run locally (no Docker)
  - Install python and the pip packages `flask` and `tinydb`
  - Clone this repository
    - `git clone https://github.com/JonasLong/DeGrabify`
    - `cd DeGrabify`
  - In the console, run
    - `python crawler/crawler.py -d database/sites.json`
    - `python server/server.py -d database/sites.json`
  - If you'd like crawler.py to run on a schedule, install `cron` and run
    - `chmod 700 crawler/cron-install.sh`
    - `./crawler/cron-install.sh $(pwd)/crawler.py '0 12 * * *' $(pwd)/database/sites.json`
      - The cronjob will be written to `/etc/cron.d/crawl-cron`. Logs will be saved in `/var/log/crawl.log`.
    - `cron`
  - Open `http://127.0.0.1:5000` in a browser


# Roadmap
- Abstract list formatting into the config/.env
- Make a ghcr build
- Double check header specs for ublock and ublacklist
  - any missing fields?
  - figure out if "access time" field ruins caching
- Use Flask in production
- Pretty up the homepage
- Better disguise crawler
- See if the "r" param in the URL changes over time as a revision #
- Better naming for the containers(?)


# Acknowledgements
 Inspired by the following projects, check them out as well:
 - https://github.com/TMAFE/anti-grabify
 - https://github.com/0n1cOn3/The-AntiIPGrabber-Blocklist
 - https://github.com/laylavish/uBlockOrigin-HUGE-AI-Blocklist
 - https://github.com/NotaInutilis/Super-SEO-Spam-Suppressor

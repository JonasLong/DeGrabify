# DeGrabify
  Provides an up-to-date list of Grabify domains, for use by adblockers.\
  The goal of this project is to reduce the risk of being doxxed by unknowingly clicking on IP logger links.\
  This project is not associated with Grabify.

  This project is made up of two parts:
  - A client which periodically retrieves a list of domains offered by the IP Logger service Grabify
  - A webserver which provides this list of domains to adblock clients

  Compatible with uBlock Origin, uBlacklist, and Hosts files\
  Easily self-hosted with Docker or compatible virtualization\
  Uses Flask, Python requests, and TinyDB

# Setup

  You can run this project in [Docker](#docker) or [locally](#run-locally-no-docker). Docker is recommended.

  TLDR: `docker pull`, `docker compose up`. For a reverse proxy, forward the server through nginx/caddy/etc, get the forwarded URL. In the docker-compose.yml, set the base proxied domain, set the proxy level `-p`, disable the exposed port, and connect the server to your bridge network.

## Docker

 ### Server
  - Clone this repository
    - `git clone https://github.com/JonasLong/DeGrabify`
    - `cd DeGrabify`
  - Consider using a reverse proxy as described [below](#run-behind-a-reverse-proxy)
  - Configure the container in `docker-compose.yml`
  - `docker compose up`
  - Continue to the [Client section](#client)

  ### Updating
  - `git fetch`
  - `git pull`
    - You may need to `git stash` if you've made changes to the config, then merge your stashed changes into main
  - `docker compose up --build`

  ### Run behind a reverse proxy
  - Change the `-p` value in the `commands` section of the server config from `0` to `1`
  - Uncomment both `networks:` sections in the compose file. Change the `name: default` value to the name of your bridge network
    - This will ensure that the server is connected to the same [external bridge network](https://docs.docker.com/compose/how-tos/networking/) that your reverse proxy is running on.
  - Comment out the `ports:` section
  - Change the `-s` option in server/server.py from `http://127.0.0.1:5000` to the base domain your server will be hosted on (e.g. `https://degrab.example.com`). If this is set incorrectly, the "Subscribe" buttons won't work but nothing else will be affected.
  - Configure your reverse proxy
    - scheme: `http`
    - domain: `degrabify-server-1`
    - port: `5000`

  ### Development
  - Clone this repository
    - `git clone https://github.com/JonasLong/DeGrabify`
    - `cd DeGrabify`
  - Run like a normal docker container, but use `docker compose up --build` to rebuild any file changes

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
    - `./crawler/cron-install.sh $(pwd)/crawler.py '0 12 * * *' -d $(pwd)/database/sites.json`
      - The cronjob will be written to `/etc/cron.d/crawl-cron`. Logs will be saved in `/var/log/crawl.log`.
    - `cron`
  - Open `http://127.0.0.1:5000` in a browser


# Roadmap
- Abstract list formatting into the config/.env
- Make a python requirements file
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

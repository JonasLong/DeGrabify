# DeGrabify
 This project is made up of two parts:
 - A client which periodically retrieves a list of domains offered by the IP Logger service Grabify
 - A webserver which provides this list of domains to adblock clients

 The goal of this project is to reduce the risk of being doxxed by unknowingly clicking on IP logger links.

 Compatible with uBlock Origin, uBlacklist, and Hosts files

 Uses Flask, Python requests, and TinyDB

# Setup
 ## Server
  TODO
  TLDR: docker pull, docker compose up, forward server through nginx, get the forwarded URL, store it as the base domain in the config, set the proxy level (also in config)
 ## Client
  To install with your adblock or Hosts file
  - Navigate to the web address of the server
  - Click the relevant subscribe link, or follow the instructions in [uBlockOrigin-HUGE-AI-Blocklist](https://github.com/laylavish/uBlockOrigin-HUGE-AI-Blocklist) for the provided URLs.
  - Most likely you'll go to uBlock or uBlacklist and import a filter, passing it the URL
  - Don't copy-paste the list of domains into your filter list- it won't auto-update as the grabify domains change 
 

# Roadmap
 - Properly handle list formatting for the different services
 - Double check header specs for ublock and ublacklist
  - any missing fields?
  - figure out if "access time" field ruins caching
 - Use environment variables for base domain and proxy level
 - Implement cron scheduling
 - Wrap for Docker
 - Integrate with nginx proxy mgr
 - Write onboarding instructions
 - Use Flask in production
 - Pretty up the homepage
 - Better disguise crawler
 - See if the "r" param in the URL changes over time as a revision #


# Acknowledgements
 Inspired by the following projects, check them out as well:
 - https://github.com/0n1cOn3/The-AntiIPGrabber-Blocklist
 - https://github.com/laylavish/uBlockOrigin-HUGE-AI-Blocklist
 - https://github.com/NotaInutilis/Super-SEO-Spam-Suppressor

#! /bin/bash

# Builds a cron file for a python program with the given name and interval.
#
# USAGE:
# cron-install.sh [filename] [interval] <args>
#
# [filename]: the name of the python file to run
# [interval]: a quoted cron statement e.g. "0 12 * * *"
# Later arguments are passed to the python file

echo Setting up cronjob
echo args: "$@"

pyfile="$1"
cron="$2"
shift 2
args="$@"

command="$cron bash -l -c \"python $pyfile $args >> /var/log/crawl.log 2>&1\""

echo command: "$command"
# Create cronfile
echo "$command" > /etc/cron.d/crawl-cron
 
# Give execution rights on the cron job
chmod 0644 /etc/cron.d/crawl-cron

# Apply cron job
crontab /etc/cron.d/crawl-cron
 
# Create the log file to be able to run tail
touch /var/log/crawl.log

echo Done cron install

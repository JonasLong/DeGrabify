#! /bin/bash

# Runs the crawler, and optionally schedules it as a cron job
#
# USAGE:
# run.sh [interval] <args>
#
# [interval] is either "once" or a quoted cron statement e.g. "0 12 * * *"
# Later arguments are passed to the python file

pyfile="crawler.py"

if [ "$1" != "once" ];
then

    # install the cronjob with the provided args
    ./cron-install.sh "$(pwd)/$pyfile" "$@"
    echo

    # run once
    echo "Initial run:"
    shift 1
    args="$@"
    python "$pyfile" "$args"

    # run the cronjob and tail the logfile
    echo "Starting cronjob, waiting for next run"
    cron
    tail -f /var/log/crawl.log

else
    
    # run once
    echo "Running once:"
    shift 1
    args="$@"
    python "$pyfile" "$args"

fi
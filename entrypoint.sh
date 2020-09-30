#!/bin/bash

# Start the run once job.
echo "Docker container has been started"

# Using System/User specific environment variables in cron
# declare -p | grep -Ev 'BASHOPTS|BASH_VERSINFO|EUID|PPID|SHELLOPTS|UID' > /container.env
# echo "SHELL=/bin/bash"
# BASH_ENV=/container.env

# start cron
/usr/sbin/crond -f -l 8 -L /app/logs/cron.log
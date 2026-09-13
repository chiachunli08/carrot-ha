#!/usr/bin/env bash
cd /data/id4-collector || exit 1
exec 9>supervisor.lock
flock -n 9 || exit 0
export PYTHONPATH="/data/openpilot/pydeps:/data/openpilot${PYTHONPATH:+:$PYTHONPATH}"
while [ -f /data/id4-collector/enabled ]; do
  if [ -f collector.log ] && [ "$(stat -c %s collector.log)" -gt 2097152 ]; then mv collector.log collector.previous.log; fi
  nice -n 15 /usr/local/venv/bin/python3 -u collector.py >> collector.log 2>&1
  sleep 30
done

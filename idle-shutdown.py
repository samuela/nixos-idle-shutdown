import re
import subprocess
import time
from datetime import datetime, timezone

MIN_UPTIME_MINUTES = 60
IDLE_TIMEOUT_MINUTES = 30

# See https://stackoverflow.com/questions/42471475/fastest-way-to-get-system-uptime-in-python-in-linux
def uptime_seconds():
  with open('/proc/uptime', 'r') as f:
    return float(f.readline().split()[0])

def latest_activity():
  # Check if there are any open tmux sessions. See https://github.com/NixOS/nixpkgs/issues/155446
  # TODO: this is broken since this script gets run as root, and tmux sessions
  # are started by normal users. Need to fix somehow, but I can't find a
  # convenient command to check for running tmux servers for _any_ user.
  # if subprocess.run(["tmux", "has-session"]).returncode == 0:
  #   return datetime.now(timezone.utc)

  # An example line of the output from `last`:
  #   skainswo pts/1        2021-04-05T06:18:27+00:00 - 2021-04-05T09:39:48+00:00  (03:21)
  # We want to get the final timestamp, but note that sometimes we get a line
  # like
  #   skainswo pts/1        2021-04-05T06:03:13+00:00 - crash                      (00:13)
  # See https://unix.stackexchange.com/a/21661/358522. We use \d\d\d\d to avoid
  # matching against "crash" lines.
  last = subprocess.check_output(["last", "--time-format", "iso", "--nohostname"]).decode("utf-8")
  if "still logged in" in last:
    return datetime.now(timezone.utc)
  else:
    return max(
        datetime.fromisoformat(x)
        for x in re.findall(r"^[^\s]+ [^\s]+\s+[^\s]+ - (\d\d\d\d-[^\s]+)", last, re.MULTILINE))

while True:
  # If the last active user session ended at least IDLE_TIMEOUT_MINUTES ago and
  # the system has been up for more than an hour, then shut down.
  if (datetime.now(timezone.utc) - latest_activity()).total_seconds(
  ) >= IDLE_TIMEOUT_MINUTES * 60 and uptime_seconds() >= MIN_UPTIME_MINUTES * 60:
    print(f"No user sessions for the last {IDLE_TIMEOUT_MINUTES} minutes, shutting down")
    subprocess.call(["shutdown", "now"])

  time.sleep(IDLE_TIMEOUT_MINUTES * 60)

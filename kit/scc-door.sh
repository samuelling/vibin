#!/bin/bash
# The door to the SCC. You open it; Claude walks through it.
#
#   bash scc-door.sh open     log in once (your password, then Duo), leave it open
#   bash scc-door.sh check    is it open?
#   bash scc-door.sh close    shut it
#
# Needs the "Host scc" block from ssh_config_scc in your ~/.ssh/config.

case "$1" in
  open)
    if ssh -O check scc 2>/dev/null; then
      echo "Already open."
    else
      echo "Logging in to the SCC. Type your BU password, then approve Duo."
      ssh -fN scc && ssh -O check scc && echo "Open. Claude can use it now."
    fi ;;
  check)
    if ssh -O check scc 2>/dev/null; then echo "Open."; else echo "Closed. Run: bash scc-door.sh open"; exit 1; fi ;;
  close)
    ssh -O exit scc 2>/dev/null; echo "Closed." ;;
  *)
    echo "usage: bash scc-door.sh open | check | close"; exit 2 ;;
esac

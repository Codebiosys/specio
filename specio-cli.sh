#! /usr/bin/env bash
#
#
#
#

USAGE="\
Welcome to the Specio-CLI: An easy CLI into the running specio cluster.

Examples
--------
To run the forrest pipeline inside of the current cluster, use the following
command. Note that all paths are the paths *inside* the container.

  ./specio-cli forrest -i /path/to/features
"

logit() {
    echo "[$(date)] $1";
}

## Begin Main ##

ID=$(docker ps | grep "_specio" | cut -f 1 -d ' ');
CMD=$@

logit "Running $CMD in $1 container with ID: $ID";
echo "-------------------------------------------------------------------------"

if [ -z "$ID" ]; then
    logit "ERROR: The specio container isn't running."
    exit -1
fi

if [ -z "$CMD" ]; then
  echo "$USAGE"
  logit "You must supply a command to run."
  exit -1
fi

docker exec -i $ID $CMD

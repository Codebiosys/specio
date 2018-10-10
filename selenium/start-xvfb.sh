#!/usr/bin/env bash
# This is a slightly modified version of the start-xvfb script in the docker
# selenium repo, the only difference is with the options presented to Xvfb on
# startup.

if [ "${START_XVFB}" = true ] ; then
  export GEOMETRY="${SCREEN_WIDTH}""x""${SCREEN_HEIGHT}""x""${SCREEN_DEPTH}"

  rm -f /tmp/.X*lock

  # Added 2018-10-8 (Brian): -listen tcp option to allow for screen grabbing from FFmpeg.
  /usr/bin/Xvfb ${DISPLAY} -screen 0 ${GEOMETRY} -ac +extension RANDR -listen tcp
else
  echo "Xvfb won't start. Chrome/Firefox can only run in headless mode. Remember to set the 'headless' flag in your test."
fi

import time
import logging

import requests

from ..celery import app


logger = logging.getLogger(__name__)


# Endpoints


RECORDING_SERVICE = 'http://selenium_hub:8000'
START_ENDPOINT = f'{RECORDING_SERVICE}/start'
STOP_ENDPOINT = f'{RECORDING_SERVICE}/stop'


# Tasks


@app.task
def start_recording(kwargs):
    if kwargs['specio_config']['no_video']:
        # Don't create a video.
        return kwargs

    response = requests.post(START_ENDPOINT)
    response.raise_for_status()

    result = response.json()

    error = result.get('error')
    if error:
        # TODO raise good exception
        raise Exception()

    return {
        **kwargs,
        'session_id': result['session_id'],
        'video_location': result['output'],
        'video_starttime': time.time(),
    }


@app.task
def stop_recording(kwargs):
    if kwargs['specio_config']['no_video']:
        # Don't create a video.
        return kwargs

    response = requests.post(STOP_ENDPOINT, dict(
        session_id=kwargs['session_id'],
    ))

    result = response.json()

    error = result.get('error')
    if error:
        # TODO raise good exception
        raise Exception(error)

    return kwargs

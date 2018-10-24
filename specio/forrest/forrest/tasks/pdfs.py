from base64 import b64encode
import logging
import os
import os.path
import shutil
from tempfile import mkdtemp
import zipfile

from pydf import template_to_pdf, unzip, find_index

from ..celery import app


logger = logging.getLogger(__name__)


@app.task
def get_report(kwargs):
    """ Given a run config and specio formatted results, attempt to generate the
    PDF report for the results.
    """
    logger.info('Attempting to generate report from test results.')
    # Unpack results
    run_config, specio_results = kwargs['run_config'], kwargs['specio_results']

    params = {
        **run_config.get('report_params', {}),
        **specio_results,
    }

    with open(run_config['template'], 'rb') as source_fp:
        tmp_dir = None          # temporary directory to extract files into
        index_fp = source_fp    # Index template file

        if zipfile.is_zipfile(source_fp):
            logger.debug('Input template is a zip archive.')
            tmp_dir = mkdtemp()
            files = list(unzip(source_fp, tmp_dir))
            index_path = find_index(files)

            if not index_path:
                raise Exception('Could not find index file for source.')

            index_fp = open(index_path)
        else:
            logger.debug('Input template is a file.')

        # HAXX: For now, we have to cd into the directory where the template is
        # to pull in the assets.
        os.chdir(os.path.dirname(index_fp.name))

        try:
            report_blob = template_to_pdf(index_fp, params=params)
        finally:
            # Ensure we cleanup after ourselves if there was a failure
            if tmp_dir:
                # Close index file we created
                index_fp.close()
                shutil.rmtree(tmp_dir)

        logger.debug('Report successfully generated.')

        return {
            **kwargs,
            'report_blob': b64encode(report_blob).decode('ascii'),
        }

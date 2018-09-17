from base64 import b64encode
import os, os.path
import shutil
from tempfile import mkdtemp, SpooledTemporaryFile
import zipfile

from pydf import template_to_pdf, unzip, find_index

from run.forrest.celery import app


@app.task
def get_report(previous_results, specio_config):
    """ Given a run config and specio formatted results, attempt to generate the
    PDF report for the results.
    """
    # Unpack results
    run_config, specio_results = previous_results

    with open(run_config['template'], 'rb') as source_fp:
        tmp_dir = None          # temporary directory to extract files into
        index_fp = source_fp    # Index template file

        if zipfile.is_zipfile(source_fp):
            tmp_dir = mkdtemp()
            files = list(unzip(source_fp, tmp_dir))
            index_path = find_index(files)

            if not index_path:
                raise ValidationError('Could not find index file for source.')

            index_fp = open(index_path)


        # HAXX: For now, we have to cd into the directory where the template is
        # to pull in the assets.
        os.chdir(os.path.dirname(index_fp.name))

        try:
            report_blob = template_to_pdf(index_fp, params=specio_results)
        finally:
            # Ensure we cleanup after ourselves if there was a failure
            if tmp_dir:
                # Close index file we created
                index_fp.close()
                shutil.rmtree(tmp_dir)

        return run_config, b64encode(report_blob).decode('ascii')

import hug

from ziphyr import Ziphyr
from ziphyr.utils import file_iterable


@hug.format.content_type('application/zip')
def output_zip_from_file(filepath, request=None, response=None):
    z = Ziphyr(b'password')
    z.from_filepath(filepath)

    source = file_iterable(filepath)

    response.downloadable_as = 'sample.zip'
    response.stream = z.generator(source)


@hug.get('/download',
         output=hug.output_format.on_content_type(
             {'application/zip': output_zip_from_file}
         ))
def download_from_file(response):
    filepath = 'sample.exe'
    return filepath

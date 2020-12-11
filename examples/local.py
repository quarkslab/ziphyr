from ziphyr import Ziphyr
from ziphyr.utils import file_iterable

filepath = '/tmp/sample.exe'
source = file_iterable(filepath)

z = Ziphyr(b'infected')
z.from_filepath(filepath)

with open('/tmp/sample.zip', 'ab') as f:
    for k in z.generator(source):
        f.write(k)

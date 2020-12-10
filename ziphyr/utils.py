"""Module for comfort utilities. Non-essential to Ziphyr."""


def file_iterable(filepath, chunksize=1024):
    """
    Turn a file on a filepath into a generator.
    """
    with open(filepath, 'rb') as fileobj:
        while True:
            chunk = fileobj.read(chunksize)
            if chunk:
                yield chunk
            else:
                return

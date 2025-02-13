import os


def upload_to(instance, prefix, filename):
    path = os.path.join(prefix, filename)
    return path


import hashlib
import os


# todo : move in utils.py
def upload_to(instance, filename):
    instance.file.open()

    if not instance.hash:
        instance_hash = hashlib.sha512(instance.file.read())
        instance.hash = instance_hash.hexdigest()
        instance.file.seek(0)
    filename_base, filename_ext = os.path.splitext(filename)

    return "{0}{1}".format(instance.hash, filename_ext)
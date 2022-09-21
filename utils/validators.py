from django.core.exceptions import ValidationError
from filesManager.models import FileSetup

def file_size(value):
    try:
        setupFiles = FileSetup.objects.get(pk=1)
        filesize=value.size
        max_file_size = setupFiles.max_file_size * (1024**2)
        if filesize>(max_file_size):
            raise ValidationError("maximum size is {} MBs".format(max_file_size))
    except(FileSetup.DoesNotExist):
        pass
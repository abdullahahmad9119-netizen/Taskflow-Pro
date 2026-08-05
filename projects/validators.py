from django.core.validators import ValidationError

def validate_file_size(file):

    max_file_size_mb = 5
    if file.size > max_file_size_mb:
        raise ValidationError(f" file size is greater than {max_file_size_mb}")
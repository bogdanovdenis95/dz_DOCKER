import re
from django.core.exceptions import ValidationError

def validate_youtube_url(value):
    youtube_regex = re.compile(
        r'^(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/.+$'
    )
    if not youtube_regex.match(value):
        raise ValidationError("Invalid URL. Only YouTube URLs are allowed.")

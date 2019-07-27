STATIC_ROOT = '/opt/rssgenerator-static'

# Use only TemporaryFileUploadHandler for uploaded files
FILE_UPLOAD_HANDLERS = (
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
)

RSSGENERATOR_LOCAL_DATA = '/opt/rssgenerator-data/localData'
ADMINS = (
    ('Anthony Prades', 'toony.github@chezouam.net'),
)

MANAGERS = ADMINS

from storages.backends.gcloud import GoogleCloudStorage


class StaticStorage(GoogleCloudStorage):
    location = 'static'
    default_acl = 'public-read'


class PublicMediaStorage(GoogleCloudStorage):
    location = 'media'
    default_acl = 'public-read'
    file_overwrite = False
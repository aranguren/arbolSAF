from django.contrib.staticfiles.storage import ManifestStaticFilesStorage


class CompressedManifestStorage(ManifestStaticFilesStorage):
    """
    Django's ManifestStaticFilesStorage with manifest_strict=False so that
    CSS url() references to missing vendor assets are silently skipped
    instead of raising an error. WhiteNoise middleware handles serving and
    compression independently.
    """
    manifest_strict = False

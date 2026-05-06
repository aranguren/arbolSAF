from django.contrib.staticfiles.storage import ManifestStaticFilesStorage


class CompressedManifestStorage(ManifestStaticFilesStorage):
    """
    ManifestStaticFilesStorage that silently ignores CSS url() references
    to missing files (e.g. vendor assets). When a referenced file can't be
    found, the original path is kept unchanged instead of raising ValueError.
    WhiteNoise middleware handles serving and compression independently.
    """

    def hashed_name(self, name, content=None, filename=None):
        try:
            return super().hashed_name(name, content=content, filename=filename)
        except ValueError:
            # File not found — return original path unchanged
            return name

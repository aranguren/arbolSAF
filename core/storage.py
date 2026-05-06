from whitenoise.storage import CompressedManifestStaticFilesStorage


class CompressedManifestStorage(CompressedManifestStaticFilesStorage):
    """
    Same as CompressedManifestStaticFilesStorage but skips CSS url()
    references that point to missing files (vendor CSS with optional assets)
    instead of raising MissingFileError.
    """
    manifest_strict = False

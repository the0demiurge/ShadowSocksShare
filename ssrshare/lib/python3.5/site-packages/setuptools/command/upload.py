from distutils.command import upload as orig


class upload(orig.upload):
    """
    Override default upload behavior to look up password
    in the keyring if available.
    """

    def finalize_options(self):
        orig.upload.finalize_options(self)
        self.password or self._load_password_from_keyring()

    def _load_password_from_keyring(self):
        """
        Attempt to load password from keyring. Suppress Exceptions.
        """
        try:
            keyring = __import__('keyring')
            self.password = keyring.get_password(self.repository,
                self.username)
        except Exception:
            pass

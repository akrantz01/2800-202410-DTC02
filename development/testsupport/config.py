from veritasai.config import env


class ConfigPatch:
    """
    A utility for temporarily overriding environment variables.
    """

    def __init__(self, source: dict[str, str] | None = None):
        self._env = source or env
        self._original = {}

    def set(self, key: str, value: str | None):
        """
        Override an environment variable.
        """
        self._original[key] = env.get(key)
        env[key] = value

    def remove(self, key: str):
        """
        Remove an environment variable.
        """
        self._original[key] = env.pop(key, None)

    @property
    def values(self) -> dict[str, str]:
        """
        Retrieve the current environment variables.
        """
        return self._env

    def undo(self):
        """
        Undo all changes.
        """
        for key, value in self._original.items():
            if value is None:
                env.pop(key, None)
            else:
                env[key] = value

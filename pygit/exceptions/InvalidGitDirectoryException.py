
class InvalidGitDirectoryException(Exception):
    """Exception raised when the directory is not a git directory."""

    def __init__(self):
        """Initialize the exception with the given message."""
        super().__init__("Current directory is not a git directory. Check your gitdir parameter or install git fitst.")
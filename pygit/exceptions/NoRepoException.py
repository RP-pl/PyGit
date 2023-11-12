
class NoRepoException(Exception):
    def __init__(self):
        super().__init__("No repository found. Please run \"git init\" first.")
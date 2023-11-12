
class MergeConflictException(Exception):

    def __init__(self):
        super().__init__("Merge conflict occurred. Please resolve the conflict and commit the changes.")
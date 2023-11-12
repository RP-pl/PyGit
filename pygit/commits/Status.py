
class Status:
    WORKING_TREE_CLEAN = 0
    WORKING_TREE_MODIFIED = 1

    def __init__(self,branch, status, versioned_files):
        self.branch = branch
        self.status = status
        self.vesioned_files = versioned_files

    def __str__(self):
        return f"{{branch:{self.branch},status:{self.status},versioned_files:{self.vesioned_files}}}"

    def __repr__(self):
        return f"Status(Branch={self.branch},Status={self.status},VersionedFiles={self.vesioned_files})"


class VersionedFile:

    def __init__(self, name, change_type):
        self.name = name
        self.change_type = change_type

    def __str__(self):
        return f"{{change_type :{self.change_type},name:{self.name}}}"
    def __repr__(self):
        reverse_dict = {v: k for k, v in ChangeType.__dict__.items()}
        return f"VersionedFile(Name={self.name},ChangeType:{reverse_dict[self.change_type]})"

class ChangeType:
    ADDED = 0
    DELETED = 1
    RENAMED = 2
    COPIED = 3
    UPDATED = 4
    MODIFIED = 5
    BOTH_DELETED = 6
    ADDED_BY_US = 7
    DELETED_BY_THEM = 8
    ADDED_BY_THEM = 9
    DELETED_BY_US = 10
    BOTH_ADDED = 11
    BOTH_MODIFIED = 12

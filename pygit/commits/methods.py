from pygit.commits.Commit import Commit
from pygit.commits.Status import Status, VersionedFile, ChangeType


def parse_log(output):
    commits = []
    for line in output.split("\n"):
        commit = line.split("|")
        commits.append(Commit(commit[0],commit[1],commit[2],commit[3],commit[4]))
    return commits

def parse_status(output):
    if "No commits yet on" in output:
        branch = output.split(" ")[4]
        return Status(branch,Status.WORKING_TREE_CLEAN,[])
    else:
        branch = output.split("\n")[0].split(" ")[1]
        status = Status.WORKING_TREE_MODIFIED
        files = []
        for line in output.split("\n")[1:]:
            print(line)
            unmerged = False if line[0] == " " or line[1] == " " else True
            if not unmerged:
                change_type = line[0] if line[0] != " " else line[1]
                if change_type == "A":
                    files.append(VersionedFile(line[3:],ChangeType.ADDED))
                elif change_type == "D":
                    files.append(VersionedFile(line[3:],ChangeType.DELETED))
                elif change_type == "R":
                    files.append(VersionedFile(line[3:],ChangeType.RENAMED))
                elif change_type == "C":
                    files.append(VersionedFile(line[3:],ChangeType.COPIED))
                elif change_type == "U":
                    files.append(VersionedFile(line[3:],ChangeType.UPDATED))
                elif change_type == "M":
                    files.append(VersionedFile(line[3:],ChangeType.MODIFIED))
            if unmerged:
                change_type = line[:2]
                if change_type == "DD":
                    files.append(VersionedFile(line[3:],ChangeType.BOTH_DELETED))
                elif change_type == "AU":
                    files.append(VersionedFile(line[3:],ChangeType.ADDED_BY_US))
                elif change_type == "UD":
                    files.append(VersionedFile(line[3:],ChangeType.DELETED_BY_THEM))
                elif change_type == "UA":
                    files.append(VersionedFile(line[3:],ChangeType.ADDED_BY_THEM))
                elif change_type == "DU":
                    files.append(VersionedFile(line[3:],ChangeType.DELETED_BY_US))
                elif change_type == "AA":
                    files.append(VersionedFile(line[3:],ChangeType.BOTH_ADDED))
                elif change_type == "UU":
                    files.append(VersionedFile(line[3:],ChangeType.BOTH_MODIFIED))

            return Status(branch,status,files)
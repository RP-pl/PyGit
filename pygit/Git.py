import os
import subprocess
from exceptions import NoRepoException, InvalidGitDirectoryException
from pygit.commits import parse_log, RestoreMode
from pygit.commits.methods import parse_status
from pygit.exceptions import SSHKeyException, MergeConflictException


class Git:
    def __init__(self, gitpath="git", workdir="./", return_output=False):
        self.__gitpath = gitpath
        self.__workdir = workdir
        self.__shell = "cmd" if os.name == "nt" else "bash"
        self.return_output = return_output

    def commit(self, message, *filenames: str):
        if not filenames:
            process = self.__run_command_in_workdir(f"{self.__gitpath} commit -a -m \"{message}\"")
        else:
            files = " ".join(filenames)
            print(files)
            process = self.__run_command_in_workdir(f"{self.__gitpath} commit {files} -m \"{message}\"")
        self.__handle_basic_exceptions(process)
        if self.return_output:
            return process.stdout

    def add(self, *filenames):
        process = self.__run_command_in_workdir(f"{self.__gitpath} add {' '.join(filenames)}")
        self.__handle_basic_exceptions(process)
        if "did not match any files" in process.stderr:
            raise FileNotFoundError("Git could not find the file you specified.")
        if self.return_output:
            return process.stdout

    def init(self):
        process = self.__run_command_in_workdir(f"{self.__gitpath} init")
        self.__handle_basic_exceptions(process)
        if self.return_output:
            return process.stdout

    def rm(self, *filenames):
        process = self.__run_command_in_workdir(f"{self.__gitpath} rm {' '.join(filenames)}")
        self.__handle_basic_exceptions(process)
        if self.return_output:
            return process.stdout

    def log(self):
        process = self.__run_command_in_workdir(f'{self.__gitpath} log --pretty=format:"%H|%an|%ae|%ad|%s"')
        commits = parse_log(process.stdout)
        self.__handle_basic_exceptions(process)
        if self.return_output:
            return commits, process.stdout
        return commits

    def status(self):
        process = self.__run_command_in_workdir(f"{self.__gitpath} status -sb")
        status = parse_status(process.stdout)
        self.__handle_basic_exceptions(process)

        if self.return_output:
            return status, process.stdout
        return status

    def checkout(self, branch):
        process = self.__run_command_in_workdir(f"{self.__gitpath} checkout {branch}")
        self.__handle_basic_exceptions(process)
        if self.return_output:
            return process.stdout

    def branch(self, branch):
        process = self.__run_command_in_workdir(f"{self.__gitpath} branch {branch}")
        self.__handle_basic_exceptions(process)
        if self.return_output:
            return process.stdout

    def fetch(self, remote, branch="",force=False,all=False):
        process = self.__run_command_in_workdir(f"{self.__gitpath} fetch {remote} {branch} {'-f' if force else ''}, {'--all' if all else ''}")
        self.__handle_basic_exceptions(process)
        if self.return_output:
            return process.stdout

    def clone(self, remote, directory,branch="",no_checkout=False,local=False,shared=False):
        process = self.__run_command_in_workdir(f"{self.__gitpath} clone {remote} {branch} {directory}, {'--no-checkout' if no_checkout else ''}, {'--local' if local else ''}, {'--shared' if shared else ''}")
        self.__handle_basic_exceptions(process)
        if self.return_output:
            return process.stdout

    def reset(self, commit, *filenames,mode: str = "soft"):
        process = self.__run_command_in_workdir(f"{self.__gitpath} reset {mode} {commit} {' '.join(filenames)}")
        self.__handle_basic_exceptions(process)
        if self.return_output:
            return process.stdout

    def restore(self, commit, *filenames,worktree=False,mode:RestoreMode = RestoreMode.DEFAULT):
        mode_map = {RestoreMode.DEFAULT: "", RestoreMode.OURS: "--ours", RestoreMode.THEIRS: "--theirs", RestoreMode.MERGED: "--staged", RestoreMode.IGNORE_UNMERGED: "--ignore-unmerged"}
        process = self.__run_command_in_workdir(f"{self.__gitpath} restore {commit} {' '.join(filenames)} {'-W' if worktree else ''} {mode_map[mode]}")
        self.__handle_basic_exceptions(process)
        if self.return_output:
            return process.stdout

    def pull(self, remote, branch="",force=False,rebase=False,allow_unrelated=False):
        process = self.__run_command_in_workdir(f"{self.__gitpath} pull {remote} {branch} {'-f' if force else ''}, {'-r' if rebase else ''}, {'--allow-unrelated-histories' if allow_unrelated else ''}")
        self.__handle_basic_exceptions(process)
        if self.return_output:
            return process.stdout

    def push(self, remote, branch="",delete=False,all=False):
        process = self.__run_command_in_workdir(f"{self.__gitpath} push {remote} {branch} {'-d' if delete else ''}, {'--all' if all else ''}")
        self.__handle_basic_exceptions(process)
        if self.return_output:
            return process.stdout


    def rebase(self, branch, force=False):
        process = self.__run_command_in_workdir(f"{self.__gitpath} rebase {branch} {'-f' if force else ''}")
        self.__handle_basic_exceptions(process)
        self.__handle_merge_conflict(process)
        if self.return_output:
            return process.stdout

    def merge(self, branch, no_ff=False):
        process = self.__run_command_in_workdir(f"{self.__gitpath} merge {branch} {'--no-ff' if no_ff else ''}")
        self.__handle_basic_exceptions(process)
        self.__handle_merge_conflict(process)
        if self.return_output:
            return process.stdout

    def revert(self, commit):
        process = self.__run_command_in_workdir(f"{self.__gitpath} revert {commit}")
        self.__handle_basic_exceptions(process)
        self.__handle_merge_conflict(process)
        if self.return_output:
            return process.stdout

    def __run_command_in_workdir(self, command: str) -> subprocess.CompletedProcess:
        process = subprocess.run(command, encoding="utf-8", shell=self.__shell, cwd=self.__workdir,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return process
    @staticmethod
    def __handle_basic_exceptions(process: subprocess.CompletedProcess):
        if process.returncode == 128 and "fatal: not a git repository" in process.stderr:
            raise NoRepoException()
        if process.returncode == 1:
            raise InvalidGitDirectoryException()
        if "Enter passphrase for key" in process.stdout:
            raise SSHKeyException()
    @staticmethod
    def __handle_merge_conflict(process: subprocess.CompletedProcess):
        if process.returncode == 1 and ("CONFLICT (content): Merge conflict in" in process.stderr or "not possible because you have unmerged files" in process.stderr):
            raise MergeConflictException()

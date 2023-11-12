import datetime


class Commit:
    def __init__(self, commit_hash,author_name,author_email,author_date,commit_message):
        self.commit_hash = commit_hash
        self.author_name = author_name
        self.author_email = author_email
        self.author_date = self.__parse_date(author_date)
        self.commit_msg = commit_message

    def __str__(self):
        return f"{{commit_hash: {self.commit_hash}, author_name: {self.author_name}, author_email: {self.author_email}, author_date: {self.author_date}, commit_msg: {self.commit_msg}}}"
    def __repr__(self):
        return f"Commit(Hash={self.commit_hash},Author={self.author_name},Email={self.author_email},Date={self.author_date},Message={self.commit_msg})"



    def __parse_date(self, author_date):
        return datetime.datetime.strptime(author_date, "%a %b %d %H:%M:%S %Y %z")

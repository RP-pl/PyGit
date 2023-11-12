
class SSHKeyException(Exception):

    def __init__(self):
        super().__init__("SSH Key required for this operation")
from .Util import error
class RuntimeError(Exception):
    def __init__(self, token, message, stage):
        self.token = token
        self.message = message
        error(token, f'<{stage}> {message}')
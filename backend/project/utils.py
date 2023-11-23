class CustomException(Exception):
    def __init__(self, error):
        self.error = error

    def to_dict(self):
        return {self.error}
class ReturnEx(Exception):
    def __init__(self, value) -> None:
        self.value = value 

class NotCompleteOUTCAR(Exception):
    def __init__(self, file) -> None:
        super().__init__(f'{file} is not complete')

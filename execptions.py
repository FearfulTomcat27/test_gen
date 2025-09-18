class NoneTestCasesException(Exception):
    def __init__(self, message="No test cases found"):
        self.message = message
        super().__init__(self.message)

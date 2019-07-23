class TestRun:
    def __init__(self, file_path=None):
        self.file_path = file_path

    def return_classification(self, input_name):
        d = {input_name: "high", "filePath": self.file_path}
        return d
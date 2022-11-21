class ModelUninitializedException(Exception):
    def __init__(self):
        super().__init__("Model uninitialized!")

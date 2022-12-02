from fastapi import HTTPException, status


class ModelNotLoadedException(HTTPException):
    def __init__(self):
        super().__init__(status.HTTP_503_SERVICE_UNAVAILABLE, "Model not loaded to the memory!")


class ModelFilesNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(status.HTTP_503_SERVICE_UNAVAILABLE, "Model files not found!")

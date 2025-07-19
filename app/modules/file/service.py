
class FileService:
    def __init__(self, file_validator):
        self.file_validator = file_validator        

    def validate_file(self, file):
        print("Inside file upload service ===>")
        return self.file_validator.validate_file(file)
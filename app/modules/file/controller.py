from flask import render_template, jsonify

class FileController:
    def __init__(self, file_service):
        self.file_service = file_service

    def index(self):
        files = self.file_service.get_all_files()
        print("Files ===>", files)
        return render_template('index.html', files=files)
    
    def upload(self, file):
        print("Inside file upload controller ===>")
        isValid = self.file_service.upload_file(file)
        print("isValid ===>", isValid)
        if isValid['valid']:
            return jsonify({'message': 'File uploaded successfully'}), 200
        else:
            return jsonify({'message': 'File upload failed'}), 400
        
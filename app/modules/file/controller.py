from flask import render_template, jsonify

class FileController:
    def __init__(self, file_service):
        self.file_service = file_service

    def index(self):
        return render_template('index.html')
    
    def list_files(self):
        return render_template('list_files.html',files=[{'name': 'file1.xlsx'}, {'name': 'file2.xlsx'}])
    
    def upload(self, file):
        print("Inside file upload controller ===>")
        isValid = self.file_service.validate_file(file)
        print("isValid ===>", isValid)
        if isValid['valid']:
            return jsonify({'message': 'File uploaded successfully'}), 200
        else:
            return jsonify({'message': 'File upload failed'}), 400
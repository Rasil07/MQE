from flask import render_template, jsonify, send_file
from io import BytesIO
from app.protocols import FileControllerProtocol,FileServiceProtocol
class FileController(FileControllerProtocol):
    def __init__(self, file_service:FileServiceProtocol):
        self.file_service = file_service

    def index(self):
        files = self.file_service.get_all_files()
        return render_template('index.html', files=files)
    
    def upload(self, file):
        isValid = self.file_service.upload_file(file)        
        if isValid['valid']:
            return jsonify({'message': 'File uploaded successfully', 'identifier': isValid.get('identifier')}), 200
        else:
            return jsonify({'message': isValid['error']}), 400
    
    def generate_report(self, file):
        isValid = self.file_service.generate_report(file)
        if isValid['valid']:
            return jsonify({'message': 'Report generated successfully'}), 200
        else:
            return jsonify({'message': isValid['error']}), 400
    
    def download_report(self):
        file_data = self.file_service.download_report()
        self.file_service.delete_file()
        return send_file(
            BytesIO(file_data), 
            as_attachment=True, 
            download_name='Report.xlsx',
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
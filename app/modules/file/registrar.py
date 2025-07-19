from flask import request, jsonify
import os
from werkzeug.utils import secure_filename
from app.modules.file.service import FileService
from app.modules.file.controller import FileController
from app.helpers.file_helpers import FileHelper
from app.modules.file.model import FileModel
class FileRegister:
    """
    File routes registration class following SOLID principles
    """
    
    def __init__(self, app,db):
        """
        Initialize with Flask app injection (Dependency Injection)
        """
        self.app = app
        self.model = FileModel(db)
        self.file_service = FileService(FileHelper(),self.model)
        self.file_controller = FileController(self.file_service)
        self._register_routes()
    
    def _register_routes(self):
        """
        Register all file-related routes using add_url_rule
        """
           # Upload file route
        self.app.add_url_rule(
            '/',
            'index',
            self.rootFile,
            methods=['GET']
        )
        # Upload file route
        self.app.add_url_rule(
            '/file/upload',
            'upload_file',
            self.upload_file,
            methods=['POST']
        )
        
    def rootFile(self):
        return self.file_controller.index()
    
    def upload_file(self):
        """
        Handle file upload endpoint
        """
        return self.file_controller.upload(request.files['file'])
            
      

 
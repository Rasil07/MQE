import os
from datetime import datetime
from werkzeug.utils import secure_filename
import pandas as pd
from app.config import Config
from app.protocols import FileHelperProtocol
class FileHelper(FileHelperProtocol):
    def __init__(self):
        # Allowed file extensions
        self.allowed_extensions = {'xlsx', 'xls'}
        # Maximum file size (10MB)
        self.max_file_size = 10 * 1024 * 1024

    def pre_upload_check(self, file):
        """
        Validate uploaded file
        """
        try:
            # Check if file is provided
            if not file or file.filename == '':
                return {'valid': False, 'error': 'No file provided'}
            
            # Check file extension
            if not self._allowed_file(file.filename):
                return {'valid': False, 'error': f'File type not allowed. Allowed types: {", ".join(self.allowed_extensions)}'}
            
            # Check file size
            file.seek(0, os.SEEK_END)
            file_size = file.tell()
            file.seek(0)  # Reset file pointer
            
            if file_size > self.max_file_size:
                return {'valid': False, 'error': f'File too large. Maximum size: {self.max_file_size // (1024*1024)}MB'}
            
            excelFile = pd.ExcelFile(file)

            expectedSheets = ['Transactions', 'Customers', 'Products']

            if not all(sheet in excelFile.sheet_names for sheet in expectedSheets):
                return {'valid': False, 'error': f'File must contain the following sheets: {", ".join(expectedSheets)}'}

            return {'valid': True}
            
        except Exception as e:
            return {'valid': False, 'error': f'Validation error: {str(e)}'}
        
    def post_upload_check(self, file_name):
        """
        Check if each sheets in the file is valid after upload
        """
        try:
            uploads_dir = Config.UPLOAD_FOLDER
            # Check if file exists
            if not os.path.exists(os.path.join(uploads_dir,file_name)):
                return {'valid': False, 'error': 'File does not exist'}
            
            excelFile = pd.ExcelFile(os.path.join(uploads_dir,file_name))
            # Did Not Include Customers Sheet as it only contains one column with strings.

            expectedColumns = {
                'Transactions': ['transaction_id', 'customer_id','transaction_date', 'product_code', 'amount', 'payment_type'],
                'Products': ['product_code', 'product_name', 'category', 'unit_price']
            }

            for sheet, columns in expectedColumns.items():
                sheetData = excelFile.parse(sheet)
                if not all(col in sheetData.columns for col in columns):
                    return {'valid': False, 'error': f'Sheet {sheet} must contain the following columns: {", ".join(columns)}'}    
            return {'valid': True, 'transaction_row_count': len(excelFile.parse('Transactions')), 'customer_row_count': len(excelFile.parse("Customers")), 'product_row_count': len(excelFile.parse('Products'))}
        except Exception as e:
            return {'valid': False, 'error': f'Validation error: {str(e)}'}
    
    def save_file(self, file):
        """
        Save file to database
        """
        # Generate a unique filename using the original filename and a timestamp
        original_filename = file.filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename, extension = os.path.splitext(original_filename)
        unique_filename = f"{filename}_{timestamp}{extension}"
        
        # Ensure uploads directory exists
        uploads_dir = Config.UPLOAD_FOLDER
        if not os.path.exists(uploads_dir):
            os.makedirs(uploads_dir)
            
        # Save the file to uploads folder
        file_path = os.path.join(uploads_dir, unique_filename)
        file.seek(0)  # Reset file pointer to beginning
        with open(file_path, 'wb') as f:
            f.write(file.read())
            
        return filename, unique_filename
        

    def _allowed_file(self, filename):
        """
        Check if file extension is allowed
        """
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in self.allowed_extensions
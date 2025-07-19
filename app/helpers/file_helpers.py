import os
from werkzeug.utils import secure_filename
import pandas as pd

class FileValidator:
    def __init__(self):
        # Allowed file extensions
        self.allowed_extensions = {'xlsx', 'xls'}
        # Maximum file size (10MB)
        self.max_file_size = 10 * 1024 * 1024

    def validate_file(self, file):
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

            transactionSheet = excelFile.parse('Transactions')
            customersSheet = excelFile.parse('Customers')
            productsSheet = excelFile.parse('Products')

            # Did Not Include Customers Sheet as it only contains one column with strings.
            
            expectedColumns = {
                'Transactions': ['transaction_id', 'customer_id','transaction_date', 'product_code', 'amount', 'payment_type'],
                'Products': ['product_code', 'product_name', 'category', 'unit_price']
            }

            for sheet, columns in expectedColumns.items():
                sheetData = excelFile.parse(sheet)
                if not all(col in sheetData.columns for col in columns):
                    return {'valid': False, 'error': f'Sheet {sheet} must contain the following columns: {", ".join(columns)}'}
                
            

            
            return {'valid': True}
            
        except Exception as e:
            return {'valid': False, 'error': f'Validation error: {str(e)}'}

    def _allowed_file(self, filename):
        """
        Check if file extension is allowed
        """
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in self.allowed_extensions
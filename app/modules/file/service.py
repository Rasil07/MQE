import os


from app.protocols import FileServiceProtocol,FileHelperProtocol,FileModelProtocol
class FileService(FileServiceProtocol):
    def __init__(self, file_helper:FileHelperProtocol,model:FileModelProtocol):
        self.file_helper = file_helper
        self.model = model          

    def upload_file(self, file):
        """
        Handle file upload - validation and saving upload log only
        """
        isVlaid= self.file_helper.validate_file(file)        
        if not isVlaid['valid']:
            return isVlaid
        
        # Generate a unique filename using the original filename and a timestamp
        original_filename,unique_filename = self.file_helper.generate_unique_filename(file)
        # Save file to database
        payload = {
            'name': original_filename,
            'identifier': unique_filename,
            'transaction_row_count': isVlaid['transaction_row_count'],
            'customer_row_count': isVlaid['customer_row_count'],
            'product_row_count': isVlaid['product_row_count']
        }
        # Saved upload log to database
        self.model.create(payload)        
        
        return {'valid': True, 'identifier': unique_filename}
    
    def generate_report(self, file):
        """
        Handle report generation for uploaded file
        """
        isVlaid = self.file_helper.validate_file(file) #validation here as well, it is redundant but just to be safe
        if not isVlaid['valid']:
            return isVlaid
        
        # Process the file and generate report
        self.file_helper.process_file(file)
        
        return {'valid': True}
    
    def get_all_files(self):
        return self.model.getAll()

    def get_file_by_id(self,file_id):
        return self.model.getById(file_id)

    def download_report(self):
        file_path = os.path.join('uploads', 'Report.xlsx')
        if not os.path.exists(file_path):
            return None
        with open(file_path, 'rb') as f:
            file_data = f.read()
        return file_data
    
    def delete_file(self):
        file_path = os.path.join('uploads', 'Report.xlsx')
        if os.path.exists(file_path):
            return os.remove(file_path)
        return None
       
from app.protocols import FileServiceProtocol,FileHelperProtocol,FileModelProtocol
class FileService(FileServiceProtocol):
    def __init__(self, file_helper:FileHelperProtocol,model:FileModelProtocol):
        self.file_helper = file_helper
        self.model = model          

    def upload_file(self, file):
        print("Inside file upload service ===>")
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
        file_id = self.model.create(payload)
        print("File id ===>", file_id)
        data = self.model.getById(file_id)
        print("Data ===>", data)
        # Process the file
        self.file_helper.process_file(file)
        
        return {'valid': True}
    
    def get_all_files(self):
        return self.model.getAll()

    def get_file_by_id(self,file_id):
        return self.model.getById(file_id)

        
       
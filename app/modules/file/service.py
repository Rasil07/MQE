from app.protocols import FileServiceProtocol,FileHelperProtocol,FileModelProtocol
class FileService(FileServiceProtocol):
    def __init__(self, file_helper:FileHelperProtocol,model:FileModelProtocol):
        self.file_helper = file_helper
        self.model = model          

    def upload_file(self, file):
        print("Inside file upload service ===>")
        isVlaid= self.file_helper.pre_upload_check(file)
        if not isVlaid['valid']:
            return isVlaid
        # Save file to folder
        name,identifier = self.file_helper.save_file(file)
        print("File saved filename ===>", name,identifier)
        isVlaid= self.file_helper.post_upload_check(identifier)
        if not isVlaid['valid']:
            return isVlaid
        # Save file to database
        payload = {
            'name': name,
            'identifier': identifier,
            'transaction_row_count': isVlaid['transaction_row_count'],
            'customer_row_count': isVlaid['customer_row_count'],
            'product_row_count': isVlaid['product_row_count']
        }
        file_id = self.model.create(payload)
        print("File id ===>", file_id)
        data = self.model.getById(file_id)
        print("Data ===>", data)
        
        return {'valid': True}
    
    def get_all_files(self):
        return self.model.getAll()
        
       
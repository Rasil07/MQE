
class FileService:
    def __init__(self, file_helper,model):
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
            'transaction_row_count': 0,
            'customer_row_count': 0,
            'product_row_count': 0
        }
        
        return {'valid': True}
        
       
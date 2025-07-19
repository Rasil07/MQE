
from app.protocols import FileModelProtocol,DatabaseProtocol
class FileModel(FileModelProtocol):
    def __init__(self, db_connection:DatabaseProtocol):
        self.db_connection = db_connection

    def create(self,payload):        
       return self.db_connection.run('INSERT INTO uploads (name, identifier, transaction_row_count, customer_row_count, product_row_count) VALUES (?, ?, ?, ?, ?)', (payload['name'], payload['identifier'], payload['transaction_row_count'], payload['customer_row_count'], payload['product_row_count']),commit=True,lastrowid=True)        

    def getById(self,upload_id):
        return self.db_connection.run('SELECT * FROM uploads WHERE id = ?', (upload_id,),fetch_one=True)

    def getAll(self):
        return self.db_connection.run('SELECT * FROM uploads ORDER BY id DESC', (), fetch_all=True)


    
    
    
class FileModel:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def create(self,payload):
        self.db_connection.execute('INSERT INTO uploads (name, identifier, transaction_row_count, customer_row_count, product_row_count) VALUES (?, ?, ?, ?, ?)', (payload['name'], payload['identifier'], payload['transaction_row_count'], payload['customer_row_count'], payload['product_row_count']))
        self.db_connection.commit()

    def read(self,identifier):
        self.db_connection.execute('SELECT * FROM uploads WHERE identifier = ?', (identifier,))
        return self.db_connection.fetchall()
    
    
    
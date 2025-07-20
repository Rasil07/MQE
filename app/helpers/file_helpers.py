import os
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
import pandas as pd
from app.config import Config
from app.protocols import FileHelperProtocol
from app.utils.geoLocation import MapBox

class FileHelper(FileHelperProtocol):
    def __init__(self):
        # Allowed file extensions
        self.allowed_extensions = {'xlsx', 'xls'}
        self.mapbox = MapBox()

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

            excelFile = pd.ExcelFile(file)
            expectedSheets = ['Transactions', 'Customers', 'Products']

            # Check if file contains all expected sheets
            missing_sheets = [sheet for sheet in expectedSheets if sheet not in excelFile.sheet_names]
            if missing_sheets:
                return {'valid': False, 'error': f'File must contain the following sheets: {", ".join(expectedSheets)}. Missing: {", ".join(missing_sheets)}'}

            expectedColumns = {
                'Transactions': ['transaction_id', 'customer_id', 'transaction_date', 'product_code', 'amount', 'payment_type'],
                'Products': ['product_code', 'product_name', 'category', 'unit_price']
            }
            for sheet, columns in expectedColumns.items():
                sheetData = excelFile.parse(sheet)
                if not all(col in sheetData.columns for col in columns):
                    return {'valid': False, 'error': f'Sheet {sheet} must contain the following columns: {", ".join(columns)}'}

            return {
                'valid': True,
                'transaction_row_count': len(excelFile.parse('Transactions')),
                'customer_row_count': len(excelFile.parse("Customers")),
                'product_row_count': len(excelFile.parse('Products'))
            }

        except Exception as e:
            return {'valid': False, 'error': f'Validation error: {str(e)}'}

    def generate_unique_filename(self, file):
        """
        Generate a unique filename using the original filename and a timestamp
        """
        original_filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename, extension = os.path.splitext(original_filename)
        unique_filename = f"{filename}_{timestamp}{extension}"
        return original_filename, unique_filename

    def enrich_address(self, address):
        """
        Enrich the address
        """
        location_data = self.mapbox.get_coordinates(address)
        
        # If there's an error, return a default structure
        if 'error' in location_data:
            return {'latitude': None,'longitude': None}
        
        return {'latitude': location_data[0], 'longitude': location_data[1] }


    def build_address_history(self, raw_customer_data):
        """
        Build the customer data
        """
        cleaned_rows = []
        excel_base_date = datetime(1899, 12, 30)

        for row in raw_customer_data[0]:
            # Remove curly braces if present
            row = row.strip('{}')
            # Split by underscore
            parts = row.split('_')
            if len(parts) == 6:
                customer_id, name, email, dob, address, created_at = parts
                address_first_seen = None
                # Parse address_seen_date from Excel timestamp
                try:
                    created_at_float = float(created_at)
                    address_first_seen = excel_base_date + timedelta(days=created_at_float)
                except ValueError:
                    address_first_seen = None
                # This will be an external API call to enrich the address
                enriched_address = self.enrich_address(address)

                cleaned_rows.append({
                    'customer_id': customer_id,
                    'name': name,
                    'email': email,
                    'dob': dob,
                    'address': address,
                    'timestamp': address_first_seen,
                    'geolocation': enriched_address
                })
            else:
                # If the row is malformed, skip or handle as needed
                continue
        df = pd.DataFrame(cleaned_rows)
        # Sort and track address changes per customer
        df = df.sort_values(by=['customer_id', 'timestamp'])
        df = df.drop_duplicates(subset=['customer_id', 'address'])
        df['change_order'] = df.groupby('customer_id').cumcount() + 1

        return df


    def build_customer_trxn_prod_data(self, trxn_prod_data):
        """
        Build the transaction data
        """
        return trxn_prod_data.groupby(['customer_id', 'category'])['amount'].sum().reset_index().rename(columns={'amount': 'total_spent'}).sort_values(['customer_id', 'total_spent'], ascending=[True, False])

    def build_top_spender_per_category(self, customer_trxn_prod_data: pd.DataFrame):
        """
        Build the top spender per category
        """
        return customer_trxn_prod_data.sort_values(['category', 'total_spent'],ascending=[True, False]).groupby('category', as_index=False).first()[['category', 'customer_id', 'total_spent']] # last() because we want the top spender per category
        

    def build_customer_spent_rank(self, trxn_prod_data: pd.DataFrame):
        """
        Build the customer spent rank
        """
        total_spent_data = trxn_prod_data.groupby('customer_id')['amount'].sum().reset_index().rename(columns={'amount': 'total_spent'})
        total_spent_data['rank'] = total_spent_data['total_spent'].rank(method='first', ascending=False).astype(int)
        return total_spent_data.sort_values('rank', ascending=True)

    def process_file(self, file):
        excelFile = pd.ExcelFile(file)
        product_data = excelFile.parse('Products')
        transaction_data = excelFile.parse('Transactions')
        raw_customer_data = excelFile.parse('Customers', header=None)

        customer_address_history_data = self.build_address_history(raw_customer_data)
        trxn_prod_data = pd.merge(transaction_data, product_data, on='product_code', how='left')
        customer_trxn_prod_data = self.build_customer_trxn_prod_data(trxn_prod_data)
        top_spender_per_category = self.build_top_spender_per_category(customer_trxn_prod_data)
        customer_spent_rank = self.build_customer_spent_rank(trxn_prod_data)

        """
        a. Detect changes in customer addresses over time and keep a history of those changes.
        b. Calculate total transaction amount of each customer for each product category.
        c. Identify the top spender in each category.
        d. Rank all customers based on their total purchase value across all products.
        """

        # Ensure the uploads directory exists
        output_dir = "uploads"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        output_file = "Report.xlsx"
        report_path = os.path.join(output_dir, output_file)
        if os.path.exists(report_path):
            os.remove(report_path)

        with pd.ExcelWriter(report_path, engine='openpyxl', mode='w') as writer:
            customer_address_history_data.to_excel(writer, sheet_name='Customer Address History', index=False)
            customer_trxn_prod_data.to_excel(writer, sheet_name='Trxn Per Customer Per Category', index=False)
            top_spender_per_category.to_excel(writer, sheet_name='Top Spender Per Category', index=False)
            customer_spent_rank.to_excel(writer, sheet_name='Customer Spent Rank', index=False)            
            writer.book.save(report_path)

    def _allowed_file(self, filename):
        """
        Check if file extension is allowed
        """
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in self.allowed_extensions
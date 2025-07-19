CREATE TABLE IF NOT EXISTS uploads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    identifier TEXT UNIQUE,
    transaction_row_count INTEGER,
    customer_row_count INTEGER,
    product_row_count INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);


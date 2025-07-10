CREATE TABLE IF NOT EXISTS serviceprice (
    id INT AUTO_INCREMENT PRIMARY KEY,
    careid VARCHAR(255) NOT NULL,
    servicetype VARCHAR(255) NOT NULL,
    servicedescription TEXT,
    serviceprice DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (careid) REFERENCES careresource_info(centreid)
); 
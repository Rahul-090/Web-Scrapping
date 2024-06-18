# Data Extractor for Websites

This project uses a list of websites to extract different types of information, which is then stored in a MySQL database. Social media connections, tech stack, payment gateways, meta titles, meta descriptions, website language, and website category are all included in the data.


## Requirements

Make sure you have fulfilled the following prerequisites before starting:

- MySQL is installed
- Python is installed
- The necessary Python packages are installed on your system:
  - requests
  - beautifulsoup
  - tqdm
  - python mysql-connector

- Pip can be used to install the necessary Python packages:

      pip install requests mysql-connector-python beautifulsoup4 tqdm

## 1. Setting Up the MySQL Database
1. Start your MySQL server.

2. Create a new database and a table to store the extracted website data.

## SQL code
    CREATE DATABASE website_data;
    USE website_data;
    
    CREATE TABLE websites (
        id INT AUTO_INCREMENT PRIMARY KEY,
        url VARCHAR(255),
        social_media_links TEXT,
        tech_stack TEXT,
        meta_title VARCHAR(255),
        meta_description TEXT,
        payment_gateways TEXT,
        website_language VARCHAR(10),
        website_category VARCHAR(50)
    );

## 2. Running the Script
1. Clone this repository or download the main.py script.
   
2. Open the script and modify the database connection details in the insert_website_data function:
   
        def insert_website_data(url, social_media_links, tech_stack, meta_title, meta_description, payment_gateways, website_language, website_category):
            try:
                connection = mysql.connector.connect(
                    host="localhost",
                    user="your_username",
                    password="your_password",
                    database="website_data"
                )
                # The rest of the function

Replace your_username and your_password with your MySQL credentials.

3.Run the script:
          
      python main.py



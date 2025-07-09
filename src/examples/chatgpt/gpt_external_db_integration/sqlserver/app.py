"""
Connects the SQL Server database using pyodbc
Pre-requisites:
1. Install pyodbc: pip3 install pyodbc
2. Install ODBC Driver for SQL Server: https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver17
Step 1: Install unixODBC
    sudo apt install unixodbc
Setp 2: Install ODBC Driver for SQL Server
    # Follow Microsoft's instructions to add the repository and install the driver
    # Example for Ubuntu:
    # run the bash script to install ODBC Driver for SQL Server on Ubuntu

    # bash script start
    if ! [[ "20.04 22.04 24.04 24.10" == *"$(grep VERSION_ID /etc/os-release | cut -d '"' -f 2)"* ]];
    then
        echo "Ubuntu $(grep VERSION_ID /etc/os-release | cut -d '"' -f 2) is not currently supported.";
        exit;
    fi

    # Download the package to configure the Microsoft repo
    curl -sSL -O https://packages.microsoft.com/config/ubuntu/$(grep VERSION_ID /etc/os-release | cut -d '"' -f 2)/packages-microsoft-prod.deb
    # Install the package
    sudo dpkg -i packages-microsoft-prod.deb
    # Delete the file
    rm packages-microsoft-prod.deb

    # Install the driver
    sudo apt-get update
    sudo ACCEPT_EULA=Y apt-get install -y msodbcsql18
    # optional: for bcp and sqlcmd
    sudo ACCEPT_EULA=Y apt-get install -y mssql-tools18
    echo 'export PATH="$PATH:/opt/mssql-tools18/bin"' >> ~/.bashrc
    source ~/.bashrc
    # optional: for unixODBC development headers
    sudo apt-get install -y unixodbc-dev
    # bash script end
    
3. Set up environment variables
"""

# import packages
import os
import pyodbc
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI
from typing import List, Dict, Any

# Load environment variables from .env file
load_dotenv(find_dotenv(), override=True)

# define openai constant
GPT_MODEL: str = "gpt-4o-mini"
TEMPERATURE: float = 0.0

# These environment variables should be set in your .env file or system environment
# define SQL Server connection parameters constants
MSSQL_OLEDB_PROVIDER: str = os.environ.get("MSSQL_OLEDB_PROVIDER", "SQLOLEDB.1")
MSSQL_SERVER_HOST: str = os.environ.get("MSSQL_DATA_SOURCE")
MSSQL_DATABASE: str = os.environ.get("MSSQL_INITIAL_CATALOG")
MSSQL_UID: str = os.environ.get("MSSQL_USER_ID")
MSSQL_PWD: str = os.environ.get("MSSQL_USER_PWD")
MSSQL_ODBC_CXN_STR: str = os.environ.get("MSSQL_ODBC_CXN_STR", "")
MSSQL_OLEDB_CXN_STR: str = os.environ.get("MSSQL_OLEDB_CXN_STR", "")

print(MSSQL_ODBC_CXN_STR)

# Initialize the SQL Server client
sql_server_odbc_conn = pyodbc.connect(
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER={MSSQL_SERVER_HOST};"
    f"DATABASE={MSSQL_DATABASE};"
    f"UID={MSSQL_UID};"
    f"PWD={MSSQL_PWD}"
)

sql_server_oledb_conn = pyodbc.connect(
    f"Provider={MSSQL_OLEDB_PROVIDER};"
    f"Data Source={MSSQL_SERVER_HOST};"
    f"Initial Catalog={MSSQL_DATABASE};"
    f"User ID={MSSQL_UID};"
    f"Password={MSSQL_PWD};"
    f"TrustServerCertificate=True;"
)

#print(sql_server_odbc_conn.state)
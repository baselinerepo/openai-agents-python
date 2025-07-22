#--------------------------------------------------------------------
# Usage: Azure Function App for SQL Connector Middleware
# Description: This Azure Function App provides middleware for executing SQL queries,
# retrieving database schema, and executing procedures.
#
# Step 1: Set up the Azure Function App with the necessary environment variables:
#
# Step 2: Local testing can be done using the Azure Functions Core Tools.
# - sudo apt-get install azure-functions-core-tools-4
# - or use pip install azure-functions-core-tools
#
# Step 3: Run the function app locally:
# - func start
# - Worker process started and initialized on port localhost:7071
# - http://localhost:7071/api/sqlconnector/query/query
#
# Step 4: Test the endpoints using tools like Postman or curl.
#
# - Three Main Endpoints:
#
# POST: /api/sqlconnector/query/query - Execute SELECT queries
# GET:  /api/sqlconnector/schema/schema - Get database schema information
# POST: /api/sqlconnector/procedure/procedure - Execute stored procedures
#
# - POST /api/sqlconnector/query with JSON body containing "query" and optional "parameters"
#
# Example Usage from GPT:
# json// Query data
# POST /api/sqlconnector/query/query
# {
#   "query": "SELECT TOP 10 * FROM SalesLT.Customer WHERE Title=@title ORDER BY CustomerID",
#   "parameters": {
#     "title": "Mr."
#   }
# }
#
#
#- GET /api/sqlconnector/schema/schema with optional "table" query parameter
#
# // Get schema
#GET /api/sqlconnector/schema?table=Users
#
#
# - POST /api/sqlconnector/procedure with JSON body containing "procedureName" and optional "parameters"
#
# POST /api/sqlconnector/procedure/procedure
#{
#  "procedureName": "[dbo].[AP_S_Customer_details]",
#  "parameters": {
#    "title": "Mr."
#  }
#}
#
#--------------------------------------------------------------------
import azure.functions as func
import time
import os
import json
import logging
from dotenv import load_dotenv, find_dotenv
from typing import Any, List, Dict, Optional, Any

# load environment variables from .env file
load_dotenv(find_dotenv(), override=True)

# Configuration
MSSQL_OLEDB_PROVIDER = os.getenv("MSSQL_OLEDB_PROVIDER", "")
MSSQL_DATA_SOURCE = os.getenv("MSSQL_DATA_SOURCE", "")
MSSQL_INITIAL_CATALOG = os.getenv("MSSQL_INITIAL_CATALOG", "")
MSSQL_USER_ID = os.getenv("MSSQL_USER_ID", "")
MSSQL_USER_PWD = os.getenv("MSSQL_USER_PWD", "")
MSSQL_PORT = os.getenv("MSSQL_PORT", "")
ODBC_DRIVER = os.getenv("ODBC_DRIVER", "")

AZURE_SQL_CNXN_STRING = f"Driver={ODBC_DRIVER};Server={MSSQL_DATA_SOURCE},{MSSQL_PORT};Database={MSSQL_INITIAL_CATALOG};UID={MSSQL_USER_ID};PWD={MSSQL_USER_PWD};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=20;"
#AZURE_SQL_CNXN_STRING = os.getenv("AZURE_SQL_CNXN_STRING", "")
AZURE_API_KEY = os.getenv("AZURE_API_KEY", "")

# dengarous SQL keywords to prevent SQL injection
DANGEROUS_SQL_KEYWORDS = ['CREATE','DROP','DELETE','ALTER','INSERT','UPDATE','TRUNCATE','EXECUTE','EXEC','BULK','MERGE','XP_','SP_']

# function app configuration
app = func.FunctionApp()

# POST /api/sqlconnector/query
@app.route(route="sqlconnector/query/{route}", auth_level=func.AuthLevel.FUNCTION, methods=["POST"])
def sqlconnector_query(req: func.HttpRequest) -> func.HttpResponse:
    try:
        logging.info('Python HTTP trigger function processed sql query request.')
        #req.route_params['route'] = 'query'
        return main(req)
    except Exception as e:
        logging.info(f"Error processing sql query request: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )


# POST: http://localhost:7071/api/sqlconnector/procedure
@app.route(route="sqlconnector/procedure/{route}", auth_level=func.AuthLevel.ANONYMOUS, methods=["POST"])
def sqlconnector_procedure(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed sql stored procedure request.')
    #req.route_params['route'] = 'procedure'
    return main(req)


# GET /api/sqlconnector/schema?table=Users
@app.route(route="sqlconnector/schema/{route}", auth_level=func.AuthLevel.FUNCTION, methods=["GET"])
def sqlconnector_schema(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed sql schema request.')
    #req.route_params['route'] = 'schema'
    return main(req)



def main(req: func.HttpRequest) -> func.HttpResponse:
    """Main entry point for the Azure Function App."""

    # route the request to the appropriate function
    route = req.route_params.get('route')

    try:
        if route == 'query':
            return query_handler(req)
        elif route == 'schema':
            return schema_handler(req)
        elif route == 'procedure':
            return stored_procedure_handler(req)
        else:
            return func.HttpResponse(
                json.dumps({ "error": "Invalid route"}),
                status_code=404,
                mimetype="application/json"
            )
    except Exception as e:
        logging.error(f"Unhandled error: {str(e)}")
        return func.HttpResponse(
            json.dumps({ "error": str(e) }),
            status_code=500,
            mimetype="application/json"
        )


def validate_api_key(req: func.HttpRequest) -> bool:
    """Validate the API key from the request headers or query parameter"""
    if not AZURE_API_KEY:
        logging.warning("API key environment variable is not set")
        return False

    # check if the API key is in the request headers
    api_key = req.headers.get('x-api-key', '')

    # fall back to query parameter if not in headers
    if not api_key:
        api_key = req.params.get('api_key', '')

    return api_key == AZURE_API_KEY


def contains_dangerous_sql_keywords(query: str) -> bool:
    """Check if the SQL query contains dangerous keywords."""
    query_upper = query.upper()
    return any(keyword in query_upper for keyword in DANGEROUS_SQL_KEYWORDS)


def get_dbConnection():
    """Get a database connection using the configured connection string."""
    import pyodbc
    try:
        if not AZURE_SQL_CNXN_STRING:
            raise ValueError("AZURE_SQL_CNXN_STRING environment variables not set.")

        cnxn = pyodbc.connect(AZURE_SQL_CNXN_STRING)
        return cnxn
    except Exception as e:
        logging.error(f"Database connection error: {str(e)}")
        raise e
    

def query_handler(req: func.HttpRequest) -> func.HttpResponse:
    """Execute a SELECT query"""
    try:
        # Validate API key
        #if not validate_api_key(req):
        #    return func.HttpResponse(
        #        json.dumps({"error": "Invalid API key"}),
        #        status_code=401,
        #        mimetype="application/json"
        #    )
        
        # Parse request body
        try:
            req_body = req.get_json()
        except ValueError:
            return func.HttpResponse(
                json.dumps({"error": "Invalid JSON in request body"}),
                status_code=400,
                mimetype="application/json"
            )
        
        if not req_body or not req_body.get('query'):
            return func.HttpResponse(
                json.dumps({"error": "Invalid query request"}),
                status_code=400,
                mimetype="application/json"
            )
        
        query = req_body['query']
        parameters = req_body.get('parameters', {})
        
        # Security check
        if contains_dangerous_sql_keywords(query):
            return func.HttpResponse(
                json.dumps({"error": "Query contains potentially dangerous operations"}),
                status_code=400,
                mimetype="application/json"
            )
        
        logging.info(f"Executing query: {query} with parameters: {parameters}")

        # Execute query
        result = execute_sql_query(query, parameters)

        return func.HttpResponse(
            json.dumps({
                "success": True,
                "data": result["data"],
                "rowCount": result["row_count"],
                "executionTime": result["execution_time"]
            }, default=str),
            status_code=200,
            mimetype="application/json"
        )
        
    except Exception as e:
        logging.error(f"Error executing query: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )


def execute_sql_query(query: str, parameters: Dict[str, Any] = None) -> Dict[str, Any]:
    """Execute a SQL query and return the results."""
    start_time = time.time()
    results = []

    with get_dbConnection() as cnxn:
        cur = cnxn.cursor()

        # prepare parameterized query
        if parameters:
            # Use parameterized query to prevent SQL injection
            # convert parameters to a pyodbc compatible format
            param_values = []
            modified_query = query

            for key, value in parameters.items():
                # replace the parameter placeholder with a question mark ? for pyodbc sql
                modified_query = modified_query.replace(f'@{key}', '?')
                #modified_query = modified_query.replace(f'@{key}', f"'{value}'")
                param_values.append(value)

            cur.execute(modified_query, param_values or {})
            #cur.execute(modified_query) # => execute a single parameterized sqlserver query
        else:
            cur.execute(query)

        # fetch results
        columns = [column[0] for column in cur.description] if cur.description else []
        results = [dict(zip(columns, row)) for row in cur.fetchall()]

        cur.close()

        #for row in cur.fetchall():
        #    row_dict = {}
        #    for i, value in enumerate(row):
        #        row_dict[columns[i]] = value
        #    results.append(row_dict)

    execution_time = (time.time() - start_time) * 1000  # convert to milliseconds

    return {
        "data": results,
        "row_count": len(results),
        "execution_time": round(execution_time, 2),
    }


def stored_procedure_handler(req: func.HttpRequest) -> func.HttpResponse:
    """Execute a stored procedure handler"""
    try:
        #if not validate_api_key(req):
        #    return func.HttpResponse(
        #        json.dumps({"error": "Invalid API key"}),
        #        status_code=401,
        #        mimetype="application/json"
        #    )
        
        try:
            req_body = req.get_json()
        except ValueError:
            return func.HttpResponse(
                json.dumps({"error": "Invalid JSON in request body"}),
                status_code=400,
                mimetype="application/json"
            )
        
        if not req_body or not req_body.get('procedureName'):
            return func.HttpResponse(
                json.dumps({"error": "Invalid procedure request"}),
                status_code=400,
                mimetype="application/json"
            )
        
        procedure_name = req_body['procedureName']
        parameters = req_body.get('parameters', {})
        
        logging.info(f"Executing stored procedure: {procedure_name} with parameters: {parameters}")
        
        result = execute_stored_proc(procedure_name, parameters)
        
        return func.HttpResponse(
            json.dumps({
                "success": True,
                "data": result["data"],
                "rowCount": result["row_count"],
                "executionTime": result["execution_time"]
            }, default=str),
            status_code=200,
            mimetype="application/json"
        )
        
    except Exception as e:
        logging.error(f"Error executing stored procedure: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )


def execute_stored_proc(procedure_name: str, parameters: Dict[str, Any] = None) -> Dict[str, Any]:
    """Execute a stored procedure and return the results."""
    start_time = time.time()
    results = []

    try:
        with get_dbConnection() as cnxn:
            cur = cnxn.cursor()

            # prepare parameterized query
            param_values = []
            parameterized_procedure = f"EXEC {procedure_name}"

            print(procedure_name, parameters)

            # build procedure call with parameters
            if parameters:
                for key, value in parameters.items():
                    parameterized_procedure += f" @{key}=?"
                    param_values.append(value)

            print(parameterized_procedure)
            cur.execute(parameterized_procedure, param_values)
            columns = [column[0] for column in cur.description]
            results = [dict(zip(columns, row)) for row in cur.fetchall()]

            cnxn.commit()
            cur.close()

            execution_time = (time.time() - start_time) * 1000  # convert to milliseconds

            return {
                "data": results,
                "row_count": len(results),
                "execution_time": round(execution_time, 2)
            }

    except Exception as e:
        logging.error(f"Stored procedure execution error: {str(e)}")
        return {
            json.dumps({"error": str(e)}),
        }

def schema_handler(req: func.HttpRequest) -> func.HttpResponse:
    """Get database schema information"""
    try:
        #if not validate_api_key(req):
        #    return func.HttpResponse(
        #        json.dumps({"error": "Invalid API key"}),
        #        status_code=401,
        #        mimetype="application/json"
        #    )
        
        table_name = req.params.get('table')
        
        schema = get_table_schema(table_name)
        
        return func.HttpResponse(
            json.dumps({
                "success": True,
                "schema": schema
            }, default=str),
            status_code=200,
            mimetype="application/json"
        )
        
    except Exception as e:
        logging.error(f"Error getting schema: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )


def get_table_schema(table_name: Optional[str] = None) -> List[Dict[str, Any]]:
    """Get database schema information"""
    base_query = """
        SELECT 
            t.TABLE_NAME,
            c.COLUMN_NAME,
            c.DATA_TYPE,
            c.IS_NULLABLE,
            c.COLUMN_DEFAULT,
            c.CHARACTER_MAXIMUM_LENGTH,
            c.NUMERIC_PRECISION,
            c.NUMERIC_SCALE
        FROM INFORMATION_SCHEMA.TABLES t
        INNER JOIN INFORMATION_SCHEMA.COLUMNS c ON t.TABLE_NAME = c.TABLE_NAME
        WHERE t.TABLE_TYPE = 'BASE TABLE'
    """
    
    if table_name:
        query = base_query + " AND t.TABLE_NAME = ?"
        params = [table_name]
    else:
        query = base_query
        params = []
    
    query += " ORDER BY t.TABLE_NAME, c.ORDINAL_POSITION"
    
    schemas = []
    
    with get_dbConnection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        
        columns = [column[0] for column in cursor.description]
        
        for row in cursor.fetchall():
            schema_dict = {}
            for i, value in enumerate(row):
                schema_dict[columns[i]] = value
            schemas.append(schema_dict)

        cursor.close()
    
    return schemas

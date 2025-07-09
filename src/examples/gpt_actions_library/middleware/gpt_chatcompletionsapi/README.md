## GPT Actions library - SQL Database

**the workflow** required to connect ChatGPT to a SQL Database via a middleware application. We’ll use a PostgreSQL database for this example, but the process should be similar for all SQL databases (MySQL, MS SQL Server, Amazon Aurora, SQL Server on Google Cloud, etc.). This documentation outlines the steps required to create GPT Action which can:

- Execute read queries against a SQL Database
- Return records via a text response
- Return records via a CSV file

### Value + Example Business Use Cases

**Value**: Users can now leverage ChatGPT's natural language capability to answer questions about data in a SQL database:

- Business users can access information contained in a SQL database without writing SQL or submitting a request to an analyst
- Data analysts can perform complex analysis beyond what is possible with a SQL query by extracting data and analyzing it with ChatGPT

### Application Design Considerations

Given that most managed SQL databases do not provide REST APIs for submitting queries, you will need a middleware application to perform the following functions:

1. Accept database queries via REST API requests
2. Forward queries to the integrated SQL database
3. Convert database responses in to CSV files
4. Return CSV files to the requestor

![Application Design Considerations](https://cookbook.openai.com/images/gptactions_sql_database_middleware.png)


### Middleware Considerations

Developers can either build custom middleware (commonly deployed as serverless functions with CSPs like AWS, GCP, or MS Azure) or use third-party solutions (like Mulesoft Anypoint or Retool Workflows).

Building your own middleware gives you more control over the application’s behavior. For an example of custom middleware, see our [Azure Functions cookbook](https://cookbook.openai.com/examples/chatgpt/gpt_actions_library/gpt_middleware_azure_function).


### Workflow Steps

1. GPT generates a SQL query based on prompt

GPTs are very good at writing SQL queries based on a user’s natural language prompt. You can improve the GPT’s query generation capabilities by giving it access to the database schema

```bash
# Context
You are a data analyst. Your job is to assist users with their business questions by analyzing the data contained in a PostgreSQL database.

## Database Schema

### Accounts Table
**Description:** Stores information about business accounts.

| Column Name  | Data Type      | Constraints                        | Description                             |
|--------------|----------------|------------------------------------|-----------------------------------------|
| account_id   | INT            | PRIMARY KEY, AUTO_INCREMENT, NOT NULL | Unique identifier for each account      |
| account_name | VARCHAR(255)   | NOT NULL                           | Name of the business account            |
| industry     | VARCHAR(255)   |                                    | Industry to which the business belongs  |
| created_at   | TIMESTAMP      | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Timestamp when the account was created  |

### Users Table
**Description:** Stores information about users associated with the accounts.

| Column Name  | Data Type      | Constraints                        | Description                             |
|--------------|----------------|------------------------------------|-----------------------------------------|
| user_id      | INT            | PRIMARY KEY, AUTO_INCREMENT, NOT NULL | Unique identifier for each user         |
| account_id   | INT            | NOT NULL, FOREIGN KEY (References Accounts(account_id)) | Foreign key referencing Accounts(account_id) |
| username     | VARCHAR(50)    | NOT NULL, UNIQUE                   | Username chosen by the user             |
| email        | VARCHAR(100)   | NOT NULL, UNIQUE                   | User's email address                    |
| role         | VARCHAR(50)    |                                    | Role of the user within the account     |
| created_at   | TIMESTAMP      | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Timestamp when the user was created     |

### Revenue Table
**Description:** Stores revenue data related to the accounts.

| Column Name  | Data Type      | Constraints                        | Description                             |
|--------------|----------------|------------------------------------|-----------------------------------------|
| revenue_id   | INT            | PRIMARY KEY, AUTO_INCREMENT, NOT NULL | Unique identifier for each revenue record |
| account_id   | INT            | NOT NULL, FOREIGN KEY (References Accounts(account_id)) | Foreign key referencing Accounts(account_id) |
| amount       | DECIMAL(10, 2) | NOT NULL                           | Revenue amount                          |
| revenue_date | DATE           | NOT NULL                           | Date when the revenue was recorded      |

# Instructions:
1. When the user asks a question, consider what data you would need to answer the question and confirm that the data should be available by consulting the database schema.
2. Write a PostgreSQL-compatible query and submit it using the `databaseQuery` API method.
3. Use the response data to answer the user's question.
4. If necessary, use code interpreter to perform additional analysis on the data until you are able to answer the user's question.
```
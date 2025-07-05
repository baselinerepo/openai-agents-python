## Connect GPT with external databases

### Critical use cases and tips for a mindful implementation of GPT in SQL Databases

### Use Cases

**Query Suggestions**: Automating SQL query generation.
**Code Review**: Identifying performance and security risks. GPT can review existing SQL queries and suggest optimisations, such as indexing, reducing nested subqueries, or spotting potential SQL injection vulnerabilities, helping you maintain efficient and secure code.
**Data Cleaning**: Formatting and transforming data. GPT can assist in creating SQL scripts to clean up data, such as removing duplicates, formatting dates, or standardising text entries, streamlining the data preparation process for analysis.
**Report Generation**: Writing queries for custom reports. By providing GPT with the table schema and report requirements, you can quickly generate queries to extract the necessary data for dashboards, summaries, or detailed reports.
**Learning and Troubleshooting**: Explaining SQL concepts or debugging errors. GPT can help clarify SQL functions, syntax, and error messages, making it a valuable resource for both beginners learning SQL and experienced users troubleshooting complex issues.

## Best practices

**Verify Output**: Always double-check AI-generated queries before running them. While GPT can be highly accurate, reviewing the queries for correctness is important, especially when dealing with complex logic or large datasets.
**Limit Sensitive Data**: When sharing table schemas or prompts with GPT, be mindful of data privacy. To maintain data security, avoid including sensitive personal data, passwords, or confidential business details.
**Performance Monitoring**: Use ChatGPT for non-critical operations or as a starting point for query generation. After obtaining the query, test its performance on a smaller subset of data before applying it to production environments to ensure it runs efficiently.

## How To Generate SQL Server Queries With GPT

You need ChatGPT to help answer data questions for your SQL Server database. To do this, you must provide ChatGPT with the schema of your table so it understands your data's structure.

Let's break down the process:

1. **Open SQL Server Management Studio (SSMS)**: Launch SSMS and connect to your SQL Server instance. Find the database containing the tables you want GPT to work with. For this example, we’ll use a single table named Employees.

2. **Extract the Table Schema**: In the Object Explorer, right-click the Employees table and select **"Script Table as"** > **"CREATE To"** > **"New Query Editor Window."** Example Data: This will generate the following table's structure:

```sh
CREATE TABLE Employees (
        EmployeeID INT PRIMARY KEY,
        FirstName NVARCHAR(50),
        LastName NVARCHAR(50),
        Department NVARCHAR(100),
        HireDate DATE,
        Salary DECIMAL(18, 2)
```

> [!Note]
> This example schema lists columns and data types, which are crucial for GPT to provide correct query responses.

3. **Copy the Schema**: Highlight the script text you see in the editor and copy it to your clipboard. The **example schema** you've copied contains essential details about how your table is set up.

4. **Prepare Your ChatGPT Prompt**: Open GPT and paste the example schema you copied. Now, add a specific data-related question. For example:

```sh
system prompt:
"""
I am using SQL Server 2019. Here is my table schema:
CREATE TABLE Employees (
        EmployeeID INT PRIMARY KEY,
        FirstName NVARCHAR(50),
        LastName NVARCHAR(50),
        Department NVARCHAR(100),
        HireDate DATE,
        Salary DECIMAL(18, 2)
     );
"""
user prompt: Can you write a SQL query to find all employees in the 'Marketing'
```
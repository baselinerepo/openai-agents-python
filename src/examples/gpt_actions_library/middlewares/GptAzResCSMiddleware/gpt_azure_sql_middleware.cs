using System;
using System.IO;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Azure.WebJobs;
using Microsoft.Azure.WebJobs.Extensions.Http;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json;
using System.Data.SqlClient;
using System.Collections.Generic;
using System.Data;

namespace GPTSQLMiddleware
{
    public static class SQLMiddlewareFunction
    {
        private static readonly string ConnectionString = Environment.GetEnvironmentVariable("SQL_CONNECTION_STRING");
        private static readonly string AllowedApiKey = Environment.GetEnvironmentVariable("API_KEY");

        [FunctionName("ExecuteQuery")]
        public static async Task<IActionResult> ExecuteQuery(
            [HttpTrigger(AuthorizationLevel.Function, "post", Route = "sql/query")] HttpRequest req,
            ILogger log)
        {
            try
            {
                // Validate API key
                if (!ValidateApiKey(req, log))
                {
                    return new UnauthorizedObjectResult(new { error = "Invalid API key" });
                }

                string requestBody = await new StreamReader(req.Body).ReadToEndAsync();
                var queryRequest = JsonConvert.DeserializeObject<QueryRequest>(requestBody);

                if (queryRequest == null || string.IsNullOrEmpty(queryRequest.Query))
                {
                    return new BadRequestObjectResult(new { error = "Invalid query request" });
                }

                // Security: Basic SQL injection prevention
                if (ContainsDangerousKeywords(queryRequest.Query))
                {
                    return new BadRequestObjectResult(new { error = "Query contains potentially dangerous operations" });
                }

                log.LogInformation($"Executing query: {queryRequest.Query}");

                var result = await ExecuteSqlQuery(queryRequest.Query, queryRequest.Parameters);
                
                return new OkObjectResult(new
                {
                    success = true,
                    data = result.Data,
                    rowCount = result.RowCount,
                    executionTime = result.ExecutionTime
                });
            }
            catch (Exception ex)
            {
                log.LogError(ex, "Error executing SQL query");
                return new BadRequestObjectResult(new { error = ex.Message });
            }
        }

        [FunctionName("GetSchema")]
        public static async Task<IActionResult> GetSchema(
            [HttpTrigger(AuthorizationLevel.Function, "get", Route = "sql/schema")] HttpRequest req,
            ILogger log)
        {
            try
            {
                if (!ValidateApiKey(req, log))
                {
                    return new UnauthorizedObjectResult(new { error = "Invalid API key" });
                }

                string tableName = req.Query["table"];
                
                var schema = await GetTableSchema(tableName);
                
                return new OkObjectResult(new
                {
                    success = true,
                    schema = schema
                });
            }
            catch (Exception ex)
            {
                log.LogError(ex, "Error getting schema");
                return new BadRequestObjectResult(new { error = ex.Message });
            }
        }

        [FunctionName("ExecuteStoredProcedure")]
        public static async Task<IActionResult> ExecuteStoredProcedure(
            [HttpTrigger(AuthorizationLevel.Function, "post", Route = "sql/procedure")] HttpRequest req,
            ILogger log)
        {
            try
            {
                if (!ValidateApiKey(req, log))
                {
                    return new UnauthorizedObjectResult(new { error = "Invalid API key" });
                }

                string requestBody = await new StreamReader(req.Body).ReadToEndAsync();
                var procedureRequest = JsonConvert.DeserializeObject<StoredProcedureRequest>(requestBody);

                if (procedureRequest == null || string.IsNullOrEmpty(procedureRequest.ProcedureName))
                {
                    return new BadRequestObjectResult(new { error = "Invalid procedure request" });
                }

                log.LogInformation($"Executing stored procedure: {procedureRequest.ProcedureName}");

                var result = await ExecuteStoredProcedure(procedureRequest.ProcedureName, procedureRequest.Parameters);
                
                return new OkObjectResult(new
                {
                    success = true,
                    data = result.Data,
                    rowCount = result.RowCount,
                    executionTime = result.ExecutionTime
                });
            }
            catch (Exception ex)
            {
                log.LogError(ex, "Error executing stored procedure");
                return new BadRequestObjectResult(new { error = ex.Message });
            }
        }

        private static bool ValidateApiKey(HttpRequest req, ILogger log)
        {
            if (string.IsNullOrEmpty(AllowedApiKey))
            {
                log.LogWarning("API_KEY environment variable not set");
                return false;
            }

            var apiKey = req.Headers["X-API-Key"].ToString();
            if (string.IsNullOrEmpty(apiKey))
            {
                apiKey = req.Query["api_key"];
            }

            return apiKey == AllowedApiKey;
        }

        private static bool ContainsDangerousKeywords(string query)
        {
            var dangerousKeywords = new[] 
            { 
                "DROP", "DELETE", "TRUNCATE", "ALTER", "CREATE", "EXEC", "EXECUTE",
                "INSERT", "UPDATE", "MERGE", "BULK", "xp_", "sp_"
            };

            var upperQuery = query.ToUpper();
            foreach (var keyword in dangerousKeywords)
            {
                if (upperQuery.Contains(keyword))
                {
                    return true;
                }
            }
            return false;
        }

        private static async Task<QueryResult> ExecuteSqlQuery(string query, Dictionary<string, object> parameters = null)
        {
            var stopwatch = System.Diagnostics.Stopwatch.StartNew();
            var results = new List<Dictionary<string, object>>();

            using (var connection = new SqlConnection(ConnectionString))
            {
                await connection.OpenAsync();
                
                using (var command = new SqlCommand(query, connection))
                {
                    // Add parameters if provided
                    if (parameters != null)
                    {
                        foreach (var param in parameters)
                        {
                            command.Parameters.AddWithValue($"@{param.Key}", param.Value ?? DBNull.Value);
                        }
                    }

                    using (var reader = await command.ExecuteReaderAsync())
                    {
                        while (await reader.ReadAsync())
                        {
                            var row = new Dictionary<string, object>();
                            for (int i = 0; i < reader.FieldCount; i++)
                            {
                                row[reader.GetName(i)] = reader.IsDBNull(i) ? null : reader.GetValue(i);
                            }
                            results.Add(row);
                        }
                    }
                }
            }

            stopwatch.Stop();
            
            return new QueryResult
            {
                Data = results,
                RowCount = results.Count,
                ExecutionTime = stopwatch.ElapsedMilliseconds
            };
        }

        private static async Task<QueryResult> ExecuteStoredProcedure(string procedureName, Dictionary<string, object> parameters = null)
        {
            var stopwatch = System.Diagnostics.Stopwatch.StartNew();
            var results = new List<Dictionary<string, object>>();

            using (var connection = new SqlConnection(ConnectionString))
            {
                await connection.OpenAsync();
                
                using (var command = new SqlCommand(procedureName, connection))
                {
                    command.CommandType = CommandType.StoredProcedure;

                    // Add parameters if provided
                    if (parameters != null)
                    {
                        foreach (var param in parameters)
                        {
                            command.Parameters.AddWithValue($"@{param.Key}", param.Value ?? DBNull.Value);
                        }
                    }

                    using (var reader = await command.ExecuteReaderAsync())
                    {
                        while (await reader.ReadAsync())
                        {
                            var row = new Dictionary<string, object>();
                            for (int i = 0; i < reader.FieldCount; i++)
                            {
                                row[reader.GetName(i)] = reader.IsDBNull(i) ? null : reader.GetValue(i);
                            }
                            results.Add(row);
                        }
                    }
                }
            }

            stopwatch.Stop();
            
            return new QueryResult
            {
                Data = results,
                RowCount = results.Count,
                ExecutionTime = stopwatch.ElapsedMilliseconds
            };
        }

        private static async Task<List<TableSchema>> GetTableSchema(string tableName = null)
        {
            var schemas = new List<TableSchema>();
            
            string query = @"
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
                WHERE t.TABLE_TYPE = 'BASE TABLE'";
            
            if (!string.IsNullOrEmpty(tableName))
            {
                query += " AND t.TABLE_NAME = @tableName";
            }
            
            query += " ORDER BY t.TABLE_NAME, c.ORDINAL_POSITION";

            using (var connection = new SqlConnection(ConnectionString))
            {
                await connection.OpenAsync();
                
                using (var command = new SqlCommand(query, connection))
                {
                    if (!string.IsNullOrEmpty(tableName))
                    {
                        command.Parameters.AddWithValue("@tableName", tableName);
                    }

                    using (var reader = await command.ExecuteReaderAsync())
                    {
                        while (await reader.ReadAsync())
                        {
                            schemas.Add(new TableSchema
                            {
                                TableName = reader["TABLE_NAME"].ToString(),
                                ColumnName = reader["COLUMN_NAME"].ToString(),
                                DataType = reader["DATA_TYPE"].ToString(),
                                IsNullable = reader["IS_NULLABLE"].ToString() == "YES",
                                DefaultValue = reader["COLUMN_DEFAULT"]?.ToString(),
                                MaxLength = reader["CHARACTER_MAXIMUM_LENGTH"] as int?,
                                NumericPrecision = reader["NUMERIC_PRECISION"] as byte?,
                                NumericScale = reader["NUMERIC_SCALE"] as int?
                            });
                        }
                    }
                }
            }

            return schemas;
        }
    }

    // Data models
    public class QueryRequest
    {
        public string Query { get; set; }
        public Dictionary<string, object> Parameters { get; set; }
    }

    public class StoredProcedureRequest
    {
        public string ProcedureName { get; set; }
        public Dictionary<string, object> Parameters { get; set; }
    }

    public class QueryResult
    {
        public List<Dictionary<string, object>> Data { get; set; }
        public int RowCount { get; set; }
        public long ExecutionTime { get; set; }
    }

    public class TableSchema
    {
        public string TableName { get; set; }
        public string ColumnName { get; set; }
        public string DataType { get; set; }
        public bool IsNullable { get; set; }
        public string DefaultValue { get; set; }
        public int? MaxLength { get; set; }
        public byte? NumericPrecision { get; set; }
        public int? NumericScale { get; set; }
    }
}
from database import connection
import pandas

c, conn = connection()

query = "SELECT temp_id, temp FROM temps_found ORDER BY time_stamp ASC LIMIT 1000"

results = pandas.read_sql_query(query, conn)
results.to_csv("temp_test.csv", index=False)

conn.close()

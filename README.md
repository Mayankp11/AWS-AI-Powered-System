# AI-Powered AWS Cost Intelligence System

## Overview

- Stored the downloaded AWS-cost csv file in S3 as raw data
- Connected to aws using s3fs 
- loaded the file in notebook from S3 bucket using pandas
- (analytics)**
- Integrated Gemini using Google AI Studio
- Gathered insights and details using Gemini by converting the data to a string and prompt generation.

  ## ** Connecting to AWS RDS DB **

```bash
pip install sqlalchemy psycopg2-binary
```
- SQLAlchemy → lets Python connect to your database.
- psycopg2-binary → PostgreSQL driver (required for PostgreSQL connection).

**
- connect using RDS credentials
- username, password, etc etc
- Push the cleaned file to the db
- perform SQl queries as:
- # Count total rows

from sqlalchemy import text
import pandas as pd

query = text('SELECT COUNT(*) AS total_rows FROM billing_data;')

with engine.connect() as connection:
    result = connection.execute(query)
    for row in result:
        print("Total rows in table:", row[0])
- 
## Difference in analytics while using Pandas and SQL

| Aspect                     | Pandas + CSV             | SQL + RDS                       |
| -------------------------- | ------------------------ | ------------------------------- |
| Dataset size               | Limited by RAM           | Can handle millions of rows     |
| Computation location       | Local (Python)           | Server (DB engine optimized)    |
| Memory usage               | High (entire CSV loaded) | Low (only query result fetched) |
| Performance                | Slower for large files   | Fast even for large datasets    |
| Multi-user support         | None                     | Yes                             |
| Integration with dashboard | Manual fetch             | Direct via SQLAlchemy / API     |

✅ Takeaways
- For testing / small CSV: pandas is fine.
- For dashboard / production: always use SQL queries on RDS, especially for aggregates or large datasets.
- Always limit data returned (LIMIT or aggregation) to avoid freezing notebooks.

# Streamlit

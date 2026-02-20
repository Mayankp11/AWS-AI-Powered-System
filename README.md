# AI-Powered AWS Cost Intelligence System

## Overview

- Stored the downloaded AWS-cost csv file in S3 as raw data
- Connected to aws using s3fs 
- loaded the file in notebook from S3 bucket using pandas
- (analytics)**
- Integrated Gemini using Google AI Studio
- Gathered insights and details using Gemini by converting the data to a string and prompt generation.

  ## ** Connecting to AWS RDS DB **

pip install sqlalchemy psycopg2-binary
- SQLAlchemy → lets Python connect to your database.
- psycopg2-binary → PostgreSQL driver (required for PostgreSQL connection).

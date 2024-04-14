import psycopg2
import json
import os
import sys
from dotenv import load_dotenv

class StoreDB:
    def __init__(self, filepath):
        # Load environment variables from .env file
        load_dotenv()
        # Establish connection to PostgreSQL
        self.conn = psycopg2.connect(
            dbname=os.getenv('POSTGRES_DB', '').strip(),
            user=os.getenv('POSTGRES_USER', ''),
            password=os.getenv('POSTGRES_PASSWORD', ''),
            host=os.getenv('POSTGRES_URL', ''),
            port='5432'
        )

        self.__create_database()

        self.json_file_path = filepath

    def __create_database(self):
        try:
            # Create a cursor object
            with self.conn.cursor() as cur:
                # Check if the database exists
                cur.execute("SELECT 1 FROM pg_database WHERE datname = 'mydatabase'")
                exists = cur.fetchone()

                # If the database does not exist, create it
                if not exists:
                    cur.execute("CREATE DATABASE mydatabase")

        except psycopg2.Error as e:
            print("Error creating database:", e)
            sys.exit(1)

    def drop_database(self):
        try:
            # Create a cursor object
            with self.conn.cursor() as cur:
                # Check if the database exists
                cur.execute("SELECT 1 FROM pg_database WHERE datname = 'mydatabase'")
                exists = cur.fetchone()

                # If the database exists, drop it
                if exists:
                    cur.execute("DROP DATABASE mydatabase")

        except psycopg2.Error as e:
            print("Error dropping database:", e)
            sys.exit(1)
            
    def create_table(self):
        try:
            # Create a cursor object
            with self.conn.cursor() as cur:
                # Create table if not exists
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS aws_checks (
                        assessment_start_time TIMESTAMP,
                        finding_unique_id VARCHAR(255),
                        provider VARCHAR(255),
                        check_id VARCHAR(255),
                        check_title VARCHAR(255),
                        status VARCHAR(255),
                        status_extended TEXT,
                        severity VARCHAR(255),
                        resource_type VARCHAR(255),
                        description TEXT,
                        risk TEXT,
                        related_url VARCHAR(255),
                        remediation_other VARCHAR(255),
                        recommendation_text TEXT,
                        recommendation_url VARCHAR(255),
                        account_id VARCHAR(255),
                        region VARCHAR(255),
                        resource_id VARCHAR(255),
                        resource_arn TEXT
                    );
                """)

                # Read JSON data from file
                json_data = self.__read_json_file(self.json_file_path)

                # Insert data into the table
                for item in json_data:
                    cur.execute("""
                        INSERT INTO aws_checks (
                            assessment_start_time,
                            finding_unique_id,
                            provider,
                            check_id,
                            check_title,
                            status,
                            status_extended,
                            severity,
                            resource_type,
                            description,
                            risk,
                            related_url,
                            remediation_other,
                            recommendation_text,
                            recommendation_url,
                            account_id,
                            region,
                            resource_id,
                            resource_arn
                        ) VALUES (
                            %(AssessmentStartTime)s,
                            %(FindingUniqueId)s,
                            %(Provider)s,
                            %(CheckID)s,
                            %(CheckTitle)s,
                            %(Status)s,
                            %(StatusExtended)s,
                            %(Severity)s,
                            %(ResourceType)s,
                            %(Description)s,
                            %(Risk)s,
                            %(RelatedUrl)s,
                            %(RemediationOther)s,  -- Changed from remediation_other
                            %(RecommendationText)s,  -- Changed from recommendation_text
                            %(RecommendationUrl)s,  -- Changed from recommendation_url
                            %(AccountId)s,
                            %(Region)s,
                            %(ResourceId)s,
                            %(ResourceArn)s
                        );
                    """, {
                        'AssessmentStartTime': item.get('AssessmentStartTime'),
                        'FindingUniqueId': item.get('FindingUniqueId'),
                        'Provider': item.get('Provider'),
                        'CheckID': item.get('CheckID'),
                        'CheckTitle': item.get('CheckTitle'),
                        'Status': item.get('Status'),
                        'StatusExtended': item.get('StatusExtended'),
                        'Severity': item.get('Severity'),
                        'ResourceType': item.get('ResourceType'),
                        'Description': item.get('Description'),
                        'Risk': item.get('Risk'),
                        'RelatedUrl': item.get('RelatedUrl'),
                        'RemediationOther': item.get('Remediation', {}).get('Code', {}).get('Other'),  # Extracting nested value
                        'RecommendationText': item.get('Remediation', {}).get('Recommendation', {}).get('Text'),  # Extracting nested value
                        'RecommendationUrl': item.get('Remediation', {}).get('Recommendation', {}).get('Url'),  # Extracting nested value
                        'AccountId': item.get('AccountId'),
                        'Region': item.get('Region'),
                        'ResourceId': item.get('ResourceId'),
                        'ResourceArn': item.get('ResourceArn')
                    })

                # Commit the transaction for all insertions
                self.conn.commit()

        except psycopg2.Error as e:
            print("Error executing SQL commands:", e)

    # Function to read JSON data from file
    def __read_json_file(self, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    
    def view_aws_checks(self):

        try:

            # Create a cursor object
            with self.conn.cursor() as cur:
                # Execute SQL query to select all rows from aws_checks table
                cur.execute("SELECT * FROM aws_checks")

                # Fetch all rows
                rows = cur.fetchall()

                # Print column names
                colnames = [desc[0] for desc in cur.description]
                print(colnames)

                # Print each row
                for row in rows:
                    print(row)

        except psycopg2.Error as e:
            print("Error:", e)

        finally:
            # Close the connection
            if self.conn:
                self.conn.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_json_file>")
        sys.exit(1)

    filepath = sys.argv[1]
    if not os.path.exists(filepath):
        print(f"Error: File '{filepath}' does not exist.")
        sys.exit(1)

    store = StoreDB(filepath)
    store.create_table()
    store.view_aws_checks()
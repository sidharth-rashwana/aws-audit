# Prowler Postgres Integration

Prowler Postgres Integration extends the functionality of the Prowler tool by seamlessly integrating it with PostgreSQL to store scan findings. This integration enables efficient tracking and management of security vulnerabilities and misconfigurations detected within your AWS environments.

## Installation Steps

### Step 1: Update `.env` File
Ensure to update the `.env` file with the necessary values before proceeding.

### Step 2: Run the Shell Script
Execute the following commands in your terminal:

```shell
chmod +x install.sh
sh install.sh
```

### Step 3: Initialize `.env`
Initialize the `.env` file to apply the configuration changes.

### Step 4: Manual Setup (For Testing)

If encountering connection or `getipaddr` errors, follow these manual setup steps:

1. Restart Docker:
   ```shell
   systemctl restart docker
   ```

2. Pull the PostgreSQL Docker image:
   ```shell
   sudo docker pull postgres
   ```

3. Run PostgreSQL container:
   ```shell
   sudo docker run -d --name my-postgres -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=new_password -e POSTGRES_DB=mydatabase -p 5432:5432 postgres
   ```

4. Access the PostgreSQL container shell:
   ```shell
   sudo docker exec -it <container-id/name> /bin/sh
   ```

5. Switch to the PostgreSQL user:
   ```shell
   su postgres
   ```

6. Access PostgreSQL:
   ```shell
   psql
   ```

7. Create a new database:
   ```sql
   CREATE DATABASE mydatabase;
   ```

8. Change the password for the postgres user:
   ```sql
   ALTER USER postgres WITH PASSWORD 'new_password';
   ```

### Step 5: Run the Python Script
Execute the following command to run the Python script:
```shell
python3 run.py
```

### Step 6: Store Scan Results on PostgreSQL
To store the scan results on PostgreSQL, use the following command:
```shell
python3 store.py <filename.json>
```

Follow these steps to seamlessly integrate Prowler with PostgreSQL and efficiently manage your AWS environment's security posture.
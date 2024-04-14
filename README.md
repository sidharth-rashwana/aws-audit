**Vulnerability Scanner**

Prowler is a powerful tool designed to scan AWS environments for potential security vulnerabilities and misconfigurations.  
Prowler Postgres Integration extends the functionality of the Prowler tool by seamlessly integrating it with PostgreSQL to store scan findings. This integration enables efficient tracking and management of security vulnerabilities and misconfigurations detected within your AWS environments.

**Installation Steps**

1. Update `.env` File
Ensure to update the `.env` file with the necessary values before proceeding.

2. Run the Shell Scripts  

`chmod +x install.sh`  
`sh install.sh`

3. Manual Setup 

If encountering connection or `getipaddr` errors, follow these manual setup steps:

3.1. Restart Docker:  
   `systemctl restart docker`

3.2. Pull the PostgreSQL Docker image:  
   `sudo docker pull postgres`

3.3 Run PostgreSQL container:  
   `sudo docker run -d --name my-postgres -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=new_password -e POSTGRES_DB=mydatabase -p 5432:5432 postgres`

3.4. Access the PostgreSQL container shell:  
   `sudo docker exec -it <container-id/name> /bin/sh`

3.5. Switch to the PostgreSQL user:  
   `su postgres`

3.6. Access PostgreSQL:  
   `psql`

3.7. Create a new database:  
   `CREATE DATABASE mydatabase;`

3.8. Change the password for the postgres user:  
   `ALTER USER postgres WITH PASSWORD 'new_password';`

**4: Run the Python Script**  
`python3 run.py`

**5: Store Scan Results on PostgreSQL**  
To store the scan results on PostgreSQL, use the following command:
`python3 store.py <filename.json>`

Follow these steps to seamlessly integrate Prowler with PostgreSQL and efficiently manage your AWS environment's security posture.

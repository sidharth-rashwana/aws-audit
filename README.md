Step-1: create .env with parameters:
```python
POSTGRES_URL=""
POSTGRES_USER=""
POSTGRES_DB=""
POSTGRES_PASSWORD=""
AWS_ACCESS_KEY=""
AWS_SECRET_KEY=""
```
Step-2 : Run the shell script  
2.1 `chmod +x install.sh`
2.2 `sh install.sh`  

Step-3 : Initialise `.env`  

Step-4 : [manually- for testing]
1. [run this step when connection/getipaddr error occurs] `systemctl restart docker`
2. `sudo docker pull postgres`
3. `sudo docker run -d --name my-postgres  -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=new_password  -e POSTGRES_DB=mydatabase -p 5432:5432 postgres`
4. `sudo docker exec -it <container-id/name> /bin/sh`
5. [inside container]`su postgres` 
6. [inside container]`psql`
7. [inside container]`CREATE DATABASE mydatabase;`
8. [inside container]`ALTER USER postgres WITH PASSWORD 'new_password';`

Step-5 : Run the python script : `python3 run.py`

Step-6 : To store on postgres :  `python3 store.py <filename.json>`
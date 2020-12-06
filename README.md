# certificate_test_bot

### DB Setup

create database 


    $ psql -U postgres
    postgres=# create user certificates_owner with createdb;
    postgres=# CREATE DATABASE certificate_test_bot OWNER certificates_owner;
    postgres=# GRANT ALL PRIVILEGES ON DATABASE certificate_test_bot TO certificates_owner;
  
in certificate_test_bot/ dir:
    
to create DB structure
    
    
    $ psql certificate_test_bot < schema.sql
    
    
to fill in
    
    $ psql certificate_test_bot < certificates.sql

### Environment Setup
in certificate_test_bot/ dir:

create virtual environment
    
    $ python3 -m venv /path/to/project/certificate_test_bot
    
    
activate virtual environment

    
    $ . venv/bin/activate 
    
 
install requirements

    
    $ pip3 install -r requirements.txt
    
 
 ### Run Application
 in certificate_test_bot/ dir:
    
    $ flask run
    
  see documentation on http://127.0.0.1:5000/
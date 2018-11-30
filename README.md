# Basic Data API w/ docker-compose

This module uses docker-compose to build and run an application that exposes a MySql database through a Python API.

<hr/>

## Table of Contents

- [Basic Data API w/ docker-compose](#basic-data-api-w-docker-compose)
  - [Table of Contents](#table-of-contents)
  - [Folder structure](#folder-structure)
  - [WWH](#wwh)
  - [Usage](#usage)
    - [Prerequisites](#prerequisites)
    - [Run](#run)
  - [Implementation details](#implementation-details)
  - [Resources](#resources)

<hr/>

## Folder structure

```
.
├── app
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── db
│   └── init.sql
├── build.sh
├── docker-compose.yml
└── README.md
```

## WWH

* **What** Defines an API.
* **Why** To interact with a database.
* **How** Docker-compose to connect a Flask API to a MySql DB, each running in its own container.

<hr/>

## Usage

### Prerequisites

* Make sure you have `docker` and `docker-compose` installed on the machine running the build.
  * link for [docker](https://www.docker.com/)
  * link for [docker-compose](https://docs.docker.com/compose/)

### Run

To start the database and run the API, run the following commands:

1. Build the application:
    ```bash
    (sudo) docker-compose build
    ```
2. Run the build:
    ```bash
    docker-compose up
    ```

In some cases, this may raise errors, f.e., because the image is not being rebuilt, or an previous underlying process is using the configured port.

* To simplify this, **force a clean build and run the application**:

  ```bash
  ./build.sh
  ```

<hr/>

## Implementation details

**The API**

* The API uses two different containers: 
  * the app and,
  * the db. 

**Database**

* The db directory has a `init.sql` script that:
  * initiates the database, 
  * creates a table and,
  * inserts some data into it.

* This script is executed when running `docker-compose up`.

**APP**

* The app directory has:
  * app.py - the application logic,
  * Dockerfile - how to build the application, 
  * requirements - the dependencies.
  
* The Dockerfile
  * defines the base image (Python3.6)
    ```docker
    FROM python:3.7-alpine
    ```
  * exposes a PORT (to communicate with exterior world)
    ```docker
    EXPOSE 5000
    ```
  * creates working directory and copies target files
    ```docker
    WORKDIR /app
    COPY app.py /app 
    COPY requirements.txt /app
    ```
  * installs dependencies
    ```docker
    RUN pip install -r requirements.txt 
    ```
  * runs the app
    ```docker
    CMD ["python", "app.py"]
    ```

* The app
  * sets an http listener (port 5000)
    ```python     
    if __name__ == '__main__':
      app.run(host='0.0.0.0')
    ```
  * configures the database access details
    ```python
    config = {
      'user': 'root',
      'password': 'root',
      'host': 'db',
      'port': '3306',
      'database': 'people'
    }
    ```
  * defines a route and returns the corresponding resource
    ```python
    @app.route('/')
    def index():
      #get user data
      payload = get_payload()
      return json.dumps(payload)
    ```
  * interacts with the database according to the selected route
    ```python
    def get_payload():  
    # Establish connection to DB
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    # Get data
    get = 'SELECT * FROM developers'
    cursor.execute(get)
    # Construct response
    response = [{
      "user": {
        "name": name,
        "age": age
      }
    } for (user_id, name, age) in cursor]
    # Close connection
    cursor.close()
    connection.close()
    # Respond
    return results 
    ``` 
**docker-compose.yml**

* The docker-compose creates two services:
  * the app - build from custom image, link to database, and maps containers ports to host ports.
    ```yml
    app:
      build: ./app
      links:
        - db
      ports:
        - "5000:5000"
    ```
  * the db - build from dockerhub image, maps ports, defines db password using environmental variables, and exposes a vaolume (not sure why this last is necessary).
    ```yml
    db:
    image: mysql:5.7
    ports:
      - "32000:3306"
    environment:
      MYSQL_ROOT_PASSWORD: root
    volumes:
    - ./db:/docker-entrypoint-initdb.d/:ro
    ```

<hr/>

## Resources

* [tutorial](https://medium.com/@shamir.stav_83310/dockerizing-a-flask-mysql-app-with-docker-compose-c4f51d20b40d) that was followed during the development of this project.
* docker stuff
  * [install](https://docs.docker.com/compose/install/#install-compose) docker-compose)
  * [docker cmd vs run](https://stackoverflow.com/questions/37461868/whats-the-difference-between-run-and-cmd-in-a-docker-file-and-when-should-i-use)
  * force [docker-compose rebuild](https://stackoverflow.com/questions/32612650/how-to-get-docker-compose-to-always-re-create-containers-from-fresh-images)

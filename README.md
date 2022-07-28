# peter_park_Flask_api_with_swagger

*   This is a Flask  API backend application for storing and searching the valid german number plates.

*   App uses Swagger documentation for testing the below api methods
       *   **GET /plate** (Returns all plates in the database with their corresponding timestamp)

       *   **POST /plate** (The endpoint accepts a plate, checks if it is a valid German plate and if so stores the plate
with the current timestamp in the database)
       *   **GET /search-plate?key=ABC123&levenshtein=1** (The endpoint returns all license plate which have a levensthein distance which is less or
equal than the one provided in the query (levenshtein) to a search key (key). We don’t care about hyphen in the license plates)

*   App uses sqllite as database

*   This app is powered by docker-compose which consists of 1 service
      1) flask-web (flask application micro service built using Dockerfile)

*   App can be made running using below command(prerequisites: docker, docker-compose):
      *   **git clone https://github.com/rahulpoluri/peter_park_Flask_api_with_swagger.git**
      *   **docker-compose up**
      *   To be checked in browser using [http://localhost:9095/swagger/](http://localhost:9095/swagger/)

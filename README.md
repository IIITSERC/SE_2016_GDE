Game design elements
------------------

This repository consists Game design elements realized in Flask as REST services. The installation and instruction to run the game design element project can be found in 'install.md'.

The endpoints of sample game design elements are explained/shared below.

------

### Badges

Namespace of the APIs registered is /badges

| Endpoint | Methods | Description |
|------------------------|---------|---------------------------------------------------------------------------------------------------------------------------------------|
| /users | GET | List all the users whose data exist with this GDE |
| /user/{{username}} | GET | Give all the badges awarded to user with username = {{username}} |
| /create | POST | Create a new badge in the database. 'name, description, image_name' payload is needed. (image to be manually placed in static folder) |
| /list | GET | List all the badges available in the system |
| /award | POST | Award a badge to user. 'username and badge' payload is needed. (name of badge and not id) |
| /static/{{image_name}} | GET | Serves the image of badges directly from static folder |

-------

### Leaderboard

Namespace of the APIs registered is /leaderboard

| Endpoint | Methods | Description |
|--------------------|---------|-----------------------------------------------------------------------------------------------------|
| /users | GET | List all the users whose data exist with this GDE |
| /user/{{username}} | GET | Give all the leader board with score of user with username = {{username}} |
| /create | POST | Create a new leaderboard in the database. 'name and description' payload are needed. |
| /list | GET | List all the leaderboards available in the system |
| /instance/{{name}} | GET | List all the scores of a particular leaderboard along with it's description |
| /give | POST | Award score to user. 'username, instance, amount' payload is needed. (name of instance and not id) |
| /take | POST | Take score from user. 'username, instance, amount' payload is needed. (name of instance and not id) |

---------

### File structure

srcGDE <-- contains all the code needed to implement the GDE
srcGDE/runserver.py <-- 'python runserver.py' will run the source code
srcGDE/db_*.py <-- utility file, automatically create and migrate database based on model. Run it for one GDE at a time
srcGDE/badges/models.py <-- models needed for badges GDE
srcGDE/badges/config.py <-- database config for badges GDE
srcGDE/badges/__init__.py <-- main code for badges GDE, routes, and controller is combined
srcGDE/leaderboard/* <-- same as explained for badges


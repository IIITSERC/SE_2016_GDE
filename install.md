The steps to run the Game design elements shared in this repo is as follows.

1. Install 'virtualenv' if not present by 'pip install virtualenv'
2. Create new environment for project by 'virtualenv flaskapp'
3. Activate the environment 'source flaskapp/bin/activate'
4. Install following packages using 'pip install <package_name>'
    - flask
    - flask-sqlalchemy
    - flask-autodoc (not used)
    - flask-jsonpify
    - sqlalchemy-migrate
    - flask-blueprint
    - flask-cors
5. Go to srcGDE folder.
6. Run using 'python runserver.py'

-----------------------

- To run the srcApplication folder. Run the folder directly with any server which can serve html file.
- Change the backend urls inside file according to your use.

Example:

1. sudo php -S 0.0.0.0:800
2. sudo python -m SimpleHTTPServer

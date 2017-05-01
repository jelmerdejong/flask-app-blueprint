# Flask App Blueprint
A simple Flask app blueprint. This will help you get started with an easy to learn, yet powerful technology stack. A stack that you can have up and running in less than 25 minutes, so you can focus on making the real thing. Including registration, login, insert and retrieve info from that database, and have it all deployed on Heroku.


## Technology Stack
* Language: [Python](https://www.python.org/)
* Back-end Framework: [Flask](http://flask.pocoo.org/)
* Front-end Framework: [Bootstrap](http://getbootstrap.com/)
* Database: [PostgreSQL](http://www.postgresql.org/)
* Hosting: [Heroku](https://www.heroku.com/)
* Templating Engine: [Jinja2](http://flask.pocoo.org/)
* Forms: [WTForms](https://wtforms.readthedocs.org/en/latest/index.html)
* Object-Relational-Mapper: [SQLAlchemy](http://www.sqlalchemy.org/)
* Database Migrations: [Alembic](https://alembic.readthedocs.org/en/latest/)
* Styleguide checker: [Flake8](http://flake8.readthedocs.org/)


## Getting Started
Accelerate your next web project and start with this Flask App Blueprint. For now, this Getting Started how-to is for written for OSX.

### 1. Setup your development environment
1. Install virtualenv
    1. Run `sudo pip install virtualenv`

2. Install virtualenvwrapper
    1. Run `sudo pip install virtualenvwrapper`
    2. Run `export WORKON_HOME=~/Envs`
    3. Run `mkdir -p $WORKON_HOME`
    4. Run `source /user/local/bin/virtualenvwrapper.sh`

3. Clone the repository and create a working directory
    1. Run `git clone git@github.com:jelmerdejong/flask-app-blueprint.git`
    2. Run `mv sab-basic projectname`
    2. Run `cd projectname`

4. Create virtual environment
    1. Run `mkvirtualenv projectname`
    2. Update postactate file:
        1. Run `nano $VIRTUAL_ENV/bin/postactivate`
        2. Add (and modify) the following line: `cd ~/path/to/your/project`
        3. Add second line: `export APP_SETTINGS="config.DevelopmentConfig"`

5. Install Packages
    1. Run `pip install -r requirements.txt`

### 2. Create GitHub and Heroku App and Repositories
1. Setup Github Repository
    1. Create a new repostitory in your Github account
    2. Change the remote origin to point to your new repository: `git remote set-url origin https://github.com/USERNAME/NEW_REPO.git`

2. Install Heroku Toolbelt and git it configured
    1. Follow https://devcenter.heroku.com/articles/getting-started-with-python#set-up

3. Create Staging environment on Heroku
    1. Run `heroku create projectname-staging`
    2. Run `git remote add staging https://git.heroku.com/projectname-staging.git`
    3. RUn `heroku config:set APP_SETTINGS=config.StagingConfig --remote staging`

4. Create Production environment on Heroku
    1. Run `heroku create projectname-production`
    2. Run `git remote add production https://git.heroku.com/projectname-production.git`
    3. Run `heroku config:set APP_SETTINGS=config.ProductionConfig --remote production`

### 3. Setup and Initialize Database
1. Setup local database
    1. Download and install [Postgres.app](http://postgresapp.com/)
    2. Open Postgres.app and open psql
    3. Create new database:
        1. Run in psql: `CREATE DATABASE projectname;`
    4. Update local configuration:
        1. Run `nano $VIRTUAL_ENV/bin/postactivate`
        2. Add line: `export DATABASE_URL="postgresql://localhost/projectname"`
    5. Restart environment: `workon projectname`

2. Initialize and run database migrations
    1. delete the directory named 'migrations'
    2. Run `python manage.py db init`
    3. Run `python manage.py db migrate`
    4. Run `python manage.py db upgrade`

3. Setup databases on Heroku
    1. Create databases:
        1. Run `heroku addons:add heroku-postgresql:hobby-dev --app projectname-staging`
        2. Run `heroku addons:add heroku-postgresql:hobby-dev --app projectname-production`
    2. Commit database migration and push to staging and live
        1. Run `git add .`
        2. Run `git commit -a -m "Database migrations"`
        3. Run `git push staging master`
        4. Run `git push production master`
    2. Run database migrations:
        1. Run `heroku run python manage.py db upgrade --app projectname-staging`
        2. Run `heroku run python manage.py db upgrade --app projectname-production`

### 4. Deploy
1. Run locally
    1. Open Postgres.app
    2. Run `workon projectname`
    3. Run `python manage.py runserver`
    4. Open in your browser: http://localhost:5000/

2. Deploy and run on staging
    1. Push latest version to staging: `git push staging master`
    2. Open in your browser: https://projectname-staging.herokuapp.com/

3. Deploy and run on production
    1. Push latest version to production: `git push production master`
    2. Open in your browser: https://projectname-production.herokuapp.com/


## Make it your own!
That was easy right? You are ready to go modify and built your next killer app. Few points to keep in mind:

1. Don't forget to commit your code and push to Github as backup ($ git push origin master)
2. Run $ flake8 projectname to get feedback on coding style
3. Deploy to staging as final test ($ git push staging master)
4. Finally: deploy to product ($ git push production master)

### Working with pip
When you first start using Flask App Blueprint you install all the required dependencies through pip, by running `pip install -r requirements.txt`. When you install new packages (by running `pip install SomePackage`), make sure to also update the requirements.txt file so next time you run `pip install -r requirements.txt` also the newly installed packages are part of you project. You can do this by running `pip freeze > requirements.txt`.

More on pip: https://pip.pypa.io/en/stable/user_guide/

## Questions / Feedback?
If you have questions or feedback, do not hesitate to use the Issues tool in this repository.

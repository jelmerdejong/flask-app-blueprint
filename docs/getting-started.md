# Getting Started
Accelerate your next web project and start with this Flask App Blueprint. This Getting Started how-to is for written for OS X / macOS.

## 0. Getting your machine ready, the prerequisites
1. Install Xcode
    1. Start with installing Xcode if you haven't already. You can find Xcode for free in the Apple Store
    2. You also need to install the Command Line Tools (CLT) of Xcode, do this by opening your Terminal and type: `xcode-select --install`
    3. Follow the steps presented by the wizard

2. Install HomeBrew
    1. HomeBrew is a package manager for macOS, install it by opening your Terminal and type: `/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"`
    2. Add the following line to your bash profile:
        1. Open your bash profile by typing `nano ~/.bash_profile`
        2. Add the line: `export PATH=/usr/local/bin:$PATH`

3. Install Python3 with HomeBrew
    1. Type in your Terminal `brew install python3`

4. Install PIP (a package manager for Python)
    1. In your Terminal type `sudo easy_install pip`


## 1. Setup your development environment
1. Clone the repository and create a working directory
    1. Run `git clone git@github.com:jelmerdejong/flask-app-blueprint.git`
    2. Run `mv flask-app-blueprint projectname`
    2. Run `cd projectname`

2. Create a virtual environment `python -m venv venv`

3. Activate the virtual environment `. venv/bin/activate`

6. Install Packages
    1. Run `pip install -r requirements.txt`

## 2. Setup Github, Heroku, and Mandrill
1. Setup Github Repository
    1. Create a new repostitory in your Github account
    2. Change the remote origin to point to your new repository: `git remote set-url origin https://github.com/USERNAME/NEW_REPO.git`
    3. Push the code to your new repository: `git push origin master`

2. Install Heroku Toolbelt and git it configured
    1. Follow https://devcenter.heroku.com/articles/getting-started-with-python#set-up

3. Create Staging environment on Heroku
    1. Run `heroku create projectname-staging`
    2. Run `git remote add staging https://git.heroku.com/projectname-staging.git`
    3. Run `heroku config:set APP_SETTINGS=config.StagingConfig --remote staging`

4. Create Production environment on Heroku
    1. Run `heroku create projectname-production`
    2. Run `git remote add production https://git.heroku.com/projectname-production.git`
    3. Run `heroku config:set APP_SETTINGS=config.ProductionConfig --remote production`

5. Create an account on [Mandrill](https://www.mandrill.com/)
    1. Run `nano $VIRTUAL_ENV/bin/postactivate`
    2. Add (and modify) the following line: `export MAIL_USERNAME="Your SMTP Username"`
    2. Add (and modify) the following line: `export MAIL_PASSWORD="Your Mandrill API Key"`
    2. Add (and modify) the following line: `export MAIL_DEFAULT_SENDER="your@defaultaddress.com"`

## 3. Setup and Initialize Database
1. Setup local database
    1. Download and install [Postgres.app](http://postgresapp.com/)
    2. Open Postgres.app and open psql
    3. Create new database:
        1. Run in psql: `CREATE DATABASE projectname;`

2. Initialize and run database migrations
    4. Run `flask db upgrade`

3. Setup databases on Heroku
    1. Create databases:
        1. Run `heroku addons:add heroku-postgresql:hobby-dev --app projectname-staging`
        2. Run `heroku addons:add heroku-postgresql:hobby-dev --app projectname-production`
    2. Run database migrations:
        1. Run `heroku run python flask db upgrade --app projectname-staging`
        2. Run `heroku run python flask db upgrade --app projectname-production`

## 4. Deploy
1. Run locally
    1. Open Postgres.app
    2. Run `. venv/bin/activate`
    3. Run `flask run`
    4. Open in your browser: http://localhost:5000/

2. Make changes, and get them committed
    1. Run `nose2` to ensure all tests still succeed (before running nose2 make sure a database named 'test' is created)
    2. Run `git add .`
    3. Run `git commit -a -m "Your Commit Message"`
    4. Run `git push origin master` to push to GitHub

3. Deploy and run on staging
    1. Push latest version to staging: `git push staging master`
    2. Open in your browser: https://projectname-staging.herokuapp.com/

4. Deploy and run on production
    1. Push latest version to production: `git push production master`
    2. Open in your browser: https://projectname-production.herokuapp.com/

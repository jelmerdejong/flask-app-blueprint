# Flask App Blueprint: the fast way to start your MVP

Flask App Blueprint is a boilerplate / starter project that will help you get started with an easy to learn, yet powerful technology stack. A stack that you can have up and running in less than 25 minutes, so you can focus on making the real thing. Ideal for hackathons, prototypes, MVPs, idea validation, or kickstarting your startup. Including registration, login, insert and retrieve info from a database, email integration, and have it all deployed on Heroku.

## Features
* User registration (including email confirmation through Mandrill), forgot password
* User profiles, including change password
* Admin only pages including statistics and user management
* Public and member only pages
* Database setup, including database migrations and CRUD examples
* Fast deployment on Heroku (including staging and production setup)
* Powerful stack: back-end based on Python with Flask, front-end is Bootstrap
* Including basic testing coverage and framework (nose2), and PEP8 check (flake8)


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


# Git Branch and Commit conventions

## Branch Naming Convention
`master` is the main branch. Avoid / do not work on master, but do your work in specific branch instead. Normally you work on a new feature or on a fix for a bug, make that clear in your branch name. Also make sure to link the issue / requirements that is relevant, plus a short description:
* `feat/4/password-reset`
* `fix/12/broken-profile-edit-form`
* `docs/92/how-to-deploy-with-ssl`

Options are:
* feat: A new feature
* fix: A bug fix
* docs: Documentation only changes
* style: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)
* refactor: A code change that neither fixes a bug nor adds a feature
* perf: A code change that improves performance
* test: Adding missing or correcting existing tests
* chore: Changes to the build process or auxiliary tools and libraries such as documentation generation

## How to Branch
Create the branch on your local machine and switch in this branch :

`git checkout -b [name_of_your_new_branch]`

Change working branch :

`git checkout [name_of_your_new_branch]`


## Git Commit Messages
Have a Subject of preferably less than 50 characters, able to complete the sentence "If applied, this commit will". For example:

If applied, this commit will refactor subsystem X for readability
If applied, this commit will update getting started documentation

Has a Body that describes what happened in greater detail. Can include bullets / lists.

Also add which issues it fixes:
Fixes #13

# On Hosting, SSL, and Domain Names
Of course you want to publish your project to the world. Therefor in the [Getting Started](getting-started.md) page you are immediately setup with a Heroku project for staging and production. However, this still runs on the Heroku domain (e.g. yourproject-staging.herokuapp.com). We want to change this to your own domain name and introduce SSL to the mix to ensure you are setup properly.

## 1. Use Cloudflare as DNS
1. Sign up for [Getting Started](https://www.cloudflare.com/) -- accounts are free
2. Recommendation: enable MFA on your Cloudflare account!
3. Add your domain name to your Cloudflare account, follow the steps
4. Remove the DNS records that are not applicable / defaults
5. Add two CNAME records (note we use CNAME Flattening to redirect www to non www):
  1. CNAME yourdomain.com yourapp.io.herokudns.com
  2. CNAME www yourapp.com
6. On the Crypto tab, set SSL to 'Full'
7. On the Page Rules tab, add a new rule, with input `http://*yourdomain.com/*` and the setting 'Always Use HTTPS'

## 2. Configure your Heroku app
1. Login to Heroku (and while you are here, setup MFA!)
2. Select the production app of your project (e.g. yourproject-production)
3. Select 'Settings' and scroll down to 'Domains and certificates'
4. Click 'Add Domain' and add the domain name (without www) you used in the first step


# Mandrill installation and configuration
For the emails being send to, amongst others, confirm users email addresses on registration, we are using Mandrill, the transactional email tool provided by the creators of MailChimp.

# Get Mandrill account and auth keys
First step is to browse to [mandrill.com](http://mandrill.com/) and register for an account. Then active and login to this account and ensure you have an domain added, verified and configured.

Now update config.py in the application root of this app to verify the MAIL_SERVER, MAIL_PORT, and MAIL_DEFAULT_SENDER entries. You can find this information on the 'SMTP & API login' under 'Settings' in Mandrill.

At the same 'SMTP & API login' you can find your API Keys. It's smart to create a new key by clicking '+ New API Key', create this new key and copy the key.

# Add the Mandrill login details to your local environments variables
To ensure our private credentials are not ending up in the git repo (or worse), we are storing all private keys in variables on our environment. Same for the Mandrill login credentials:

1. In your terminal enter `nano $VIRTUAL_ENV/bin/postactivate`
2. Add `export MAIL_USERNAME="Your Mandrill Username"`
3. Add `export MAIL_PASSWORD="Your Mandrill API Key"`

# Add the Mandrill login details to your Heroku instances
If you want to use Mandrill as well on your Heroku staging or production environment, you also need to add the login details there:

For staging:
1. Run `heroku config:set MAIL_USERNAME="Your Mandrill Username" --remote staging`
2. Run `heroku config:set MAIL_PASSWORD="Your Mandrill API Key" --remote staging`

And for production:
1. Run `heroku config:set MAIL_USERNAME="Your Mandrill Username" --remote production`
2. Run `heroku config:set MAIL_PASSWORD="Your Mandrill API Key" --remote production`


# Questions / Feedback?
If you have questions or feedback, do not hesitate to use the Issues tool in this repository.


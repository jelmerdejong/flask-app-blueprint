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

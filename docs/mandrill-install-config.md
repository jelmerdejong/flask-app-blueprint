# Configuring Transactional Email
The application sends confirmation and password-reset emails through `Flask-Mail`.

By default, [config.py](../config.py) still points at Mandrill / Mailchimp Transactional SMTP:

* `MAIL_SERVER=smtp.mandrillapp.com`
* `MAIL_PORT=587`

All mail settings can now be overridden with environment variables, so you do not need to edit code to change providers.

## Local development
1. Copy the example env file:
   `cp .env.example .env`
2. Set the values your SMTP provider requires:
   * `MAIL_SERVER`
   * `MAIL_PORT`
   * `MAIL_USE_TLS`
   * `MAIL_USE_SSL`
   * `MAIL_USERNAME`
   * `MAIL_PASSWORD`
   * `MAIL_DEFAULT_SENDER`

If you do not configure mail locally, the test suite still passes because test config suppresses outbound mail.

## GitHub Codespaces
Store the same values in Codespaces secrets instead of committing them to the repository. The codespace will pick them up automatically through the environment.

## Heroku
Set the values as config vars on each app:

`heroku config:set MAIL_SERVER=smtp.mandrillapp.com MAIL_PORT=587 MAIL_USE_TLS=true MAIL_USERNAME=... MAIL_PASSWORD=... MAIL_DEFAULT_SENDER=... -a yourapp-name`

Repeat for staging and production if you keep separate Heroku apps.

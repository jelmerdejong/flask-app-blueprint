# On Heroku, SSL, and Domain Names
This project still supports Heroku deployment through the checked-in `Procfile`, but the exact domain and certificate setup now depends more on your Heroku app configuration than on hard-coded dashboard steps.

## Recommended flow
1. Deploy the app to Heroku and confirm it boots correctly on the default `*.herokuapp.com` domain.
2. Add your custom domain to the Heroku app.
3. Point DNS at the Heroku target for that domain.
4. Enable Heroku managed certificates or the certificate flow that matches your account setup.
5. Force HTTPS at the edge or in the application stack you operate.

## With Cloudflare in front
If you use Cloudflare for DNS:

1. Add the domain in Heroku first so you get the canonical DNS target for the app.
2. Create the DNS record in Cloudflare using the target Heroku gives you.
3. Enable HTTPS redirect behavior only after the Heroku certificate is active.
4. Verify both the apex domain and `www` variant resolve where you expect.

## Practical note
Do not hard-code historical `herokudns.com` targets into documentation or automation. Use the domain target shown by the current Heroku app configuration for your exact app and domain.

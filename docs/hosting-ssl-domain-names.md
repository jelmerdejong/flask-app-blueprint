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

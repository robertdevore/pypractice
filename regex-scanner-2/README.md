# :mag_right: Regex Scanner 2

Scans the current directory + sub-directories for a list of various regex expressions.

![python](https://img.shields.io/badge/python-3.x-green.svg) ![license](https://img.shields.io/badge/License-GPLv3-brightgreen.svg)

File types included in the search:

* .php
* .js
* .py
* .env
* .env.*
* .config
* .config.*
* .json
* .yaml
* .yml
* .ini
* .xml
* .txt

What's being searched for:

* Slack Token
* RSA private key
* SSH (DSA) private key
* SSH (EC) private key
* PGP private key block
* AWS API Key
* Amazon MWS Auth Token
* AWS AppSync GraphQL Key
* Facebook Access Token
* Facebook OAuth
* GitHub
* Generic API Key
* Generic Secret
* Google API Key
* Google OAuth
* Google (GCP) Service-account
* Google OAuth Access Token
* Heroku API Key
* MailChimp API Key
* Mailgun API Key
* Password in URL
* PayPal Braintree Access Token
* Picatic API Key
* Slack Webhook
* Stripe API Key
* Stripe Restricted API Key
* Square Access Token
* Square OAuth Secret
* Telegram Bot API Key
* Twilio API Key
* Twitter Access Token
* Twitter OAuth

### :computer: How to use

`$ python3 regexScan.py`

### :pray: Thanks

Shout out to [RoseSecurity](https://github.com/RoseSecurity/) for their [password hunting regex](https://github.com/RoseSecurity/Red-Teaming-TTPs#password-hunting-regex)
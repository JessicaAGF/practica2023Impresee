from flask_appbuilder.security.manager import AUTH_OAUTH
from custom_sso_security_manager import CustomSsoSecurityManager

# Superset specific config
ROW_LIMIT = 10000

SUPERSET_WEBSERVER_PORT = 8088

# Flask App Builder configuration
# Your App secret key will be used for securely signing the session cookie
# and encrypting sensitive information on the database
# Make sure you are changing this key for your deployment with a strong key.
# You can generate a strong key using `openssl rand -base64 42`
PREVIOUS_SECRET_KEY = '21thisismyscretkey12eyyh'
SECRET_KEY = 'O4KtcZOpMwXyBzvjVD7oWQEwECaKW7QHsgSuW5nyVaEDldgStAO3uT6u'

ENABLE_PROXY_FIX = True
AUTH_TYPE = AUTH_OAUTH

# Uncomment to setup Full admin role name
AUTH_ROLE_ADMIN = 'Admin'

# Will allow user self registration
AUTH_USER_REGISTRATION = True

# The default user self registration role
AUTH_USER_REGISTRATION_ROLE = "Public"

PREVENT_UNSAFE_DB_CONNECTIONS = False


client_id = ('1043113000683-7th9vocmif0pnq39sgu8f678dh42hv5f'
             + '.apps.googleusercontent.com')

client_secret = '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'

api_base_url_google = 'https://www.googleapis.com/oauth2/v2/'
access_url = 'https://accounts.google.com/o/oauth2/'

OAUTH_PROVIDERS = [
                    {
                        'name': 'google',
                        'icon': 'fa-google',
                        'token_key': 'access_token',
                        'remote_app': {
                            'api_base_url': api_base_url_google,
                            'client_kwargs': {
                                'scope': 'email profile'
                            },
                            'request_token_url': None,
                            'access_token_url': access_url + 'token',
                            'authorize_url': access_url + 'auth',
                            'client_id': client_id,
                            'client_secret': client_secret
                        }
                    }]

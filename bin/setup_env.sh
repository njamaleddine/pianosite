#!/bin/bash
# First time setup for .env file
if [ -f /.env ]; then
    sudo echo "'.env' file already exists, exiting environment variable file setup..."
fi

ENV_FILE=".env"
touch $ENV_FILE
sudo echo 'ALLOWED_HOSTS=""' > ${ENV_FILE}
sudo echo 'APP_NAME=""' >> ${ENV_FILE}
sudo echo 'CONTACT_EMAIL=""' >> ${ENV_FILE}
sudo echo 'DATABASE_URL=""' >> ${ENV_FILE}
sudo echo 'DEBUG=False' >> ${ENV_FILE}
sudo echo 'DJANGO_SECRET_KEY="'$(openssl rand -hex 64)'"' >> ${ENV_FILE}
sudo echo 'EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"' >> ${ENV_FILE}
sudo echo 'EMAIL_HOST="email-smtp.us-east-1.amazonaws.com"' >> ${ENV_FILE}
sudo echo 'EMAIL_HOST_USER=""' >> ${ENV_FILE}
sudo echo 'EMAIL_HOST_PASSWORD=""' >> ${ENV_FILE}
sudo echo 'EMAIL_PORT=587' >> ${ENV_FILE}
sudo echo 'MEDIA_URL=""' >> ${ENV_FILE}
sudo echo 'OSCAR_GOOGLE_ANALYTICS_ID=""' >> ${ENV_FILE}
sudo echo 'PORT=8000' >> ${ENV_FILE}
sudo echo 'SENTRY_DSN=""' >> ${ENV_FILE}
sudo echo 'STRIPE_PUBLIC_KEY=""' >> ${ENV_FILE}
sudo echo 'STRIPE_SECRET_KEY=""' >> ${ENV_FILE}

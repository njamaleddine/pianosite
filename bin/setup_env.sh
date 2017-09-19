# First time setup for .env file
if [ -f /.env ]; then
    echo "'.env' file already exists, exiting environment variable file setup..."
fi

ENV_FILE="./.env"
echo 'ALLOWED_HOSTS=""' >> ${ENV_FILE}
echo 'CONTACT_EMAIL=""' >> ${ENV_FILE}
echo 'DATABASE_URL=""' >> ${ENV_FILE}
echo 'DEBUG=False' >> ${ENV_FILE}
echo 'DJANGO_SECRET_KEY="$(openssl rand -hex 64)"' >> ${ENV_FILE}
echo 'EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"' >> ${ENV_FILE}
echo 'EMAIL_HOST="email-smtp.us-east-1.amazonaws.com"' >> ${ENV_FILE}
echo 'EMAIL_HOST_USER=""' >> ${ENV_FILE}
echo 'EMAIL_HOST_PASSWORD=""' >> ${ENV_FILE}
echo 'EMAIL_PORT=""' >> ${ENV_FILE}
echo 'MEDIA_URL=""' >> ${ENV_FILE}
echo 'PORT=8000' >> ${ENV_FILE}
echo 'SENTRY_DSN=""' >> ${ENV_FILE}
echo 'STRIPE_PUBLIC_KEY=""' >> ${ENV_FILE}
echo 'STRIPE_SECRET_KEY=""' >> ${ENV_FILE}

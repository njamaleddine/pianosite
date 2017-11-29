#!/bin/bash
# Renew SSL
certbot renew --post-hook "service nginx reload"


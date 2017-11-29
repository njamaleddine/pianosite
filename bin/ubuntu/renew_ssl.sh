#!/bin/bash
# Renew SSL
sudo certbot renew --dry-run --post-hook "sudo service nginx reload"

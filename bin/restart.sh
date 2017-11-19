#!/bin/bash
# Restart application
# Assumes the OS is: Ubuntu 16.04
sudo systemctl restart pianosite_worker
sudo systemctl restart pianosite_scheduler
sudo systemctl restart pianosite_search
sudo systemctl restart pianosite_web

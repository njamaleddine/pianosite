#!/bin/bash
# copy over and start systemd scripts
sudo cp ./bin/ubuntu/services/pianosite_worker.service /etc/systemd/system/pianosite_worker.service
sudo cp ./bin/ubuntu/services/pianosite_scheduler.service /etc/systemd/system/pianosite_scheduler.service
sudo cp ./bin/ubuntu/services/pianosite_search.service /etc/systemd/system/pianosite_search.service
sudo cp ./bin/ubuntu/services/pianosite_web.service /etc/systemd/system/pianosite_web.service
sudo systemctl daemon-reload

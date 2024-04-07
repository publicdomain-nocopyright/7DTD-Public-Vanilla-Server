#!/bin/bash

ps aux | grep 'OpenCollective_API_image_server.py' | grep -v grep | awk '{print $2}'

curl http://localhost:8001/image.png
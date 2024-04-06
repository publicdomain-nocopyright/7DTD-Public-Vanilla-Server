#!/bin/bash

ps aux | grep 'OpenCollective_API_image_server.py' | grep -v grep | awk '{print $2}'
#!/bin/bash
APP_SETTINGS=config.DevelopmentConfig  SECRET_KEY=supersecret  SQLALCHEMY_DATABASE_URI=sqlite:///testcode.db python3 manage.py runserver

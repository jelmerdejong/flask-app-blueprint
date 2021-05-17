cd project
APP_SETTINGS=config.DevelopmentConfig  SECRET_KEY=supersecret  SQLALCHEMY_DATABASE_URI=sqlite:///testcode.db python3 ../manage.py db init
APP_SETTINGS=config.DevelopmentConfig  SECRET_KEY=supersecret  SQLALCHEMY_DATABASE_URI=sqlite:///testcode.db python3 ../manage.py db migrate

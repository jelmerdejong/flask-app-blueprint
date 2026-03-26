import os
import tempfile
import unittest

from project import create_app
from project.extensions import db


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        db_fd, db_path = tempfile.mkstemp()
        self._db_fd = db_fd
        self._db_path = db_path
        self.test_app = create_app(
            "config.TestingConfig",
            {
                "DEBUG": False,
                "SQLALCHEMY_DATABASE_URI": "sqlite:///{}".format(db_path),
            },
        )
        self.app_context = self.test_app.app_context()
        self.app_context.push()
        self.app = self.test_app.test_client()
        db.create_all()

        self.assertFalse(self.test_app.debug)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        os.close(self._db_fd)
        os.unlink(self._db_path)

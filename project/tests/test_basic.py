# project/test_basic.py
import unittest

from project import app, db


class BasicTests(unittest.TestCase):
    # SETUP AND TEARDOWN
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/test'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()
        self.assertEqual(app.debug, False)

    def tearDown(self):
        pass

    # HELPER METHODS
    def register(self, email, password, confirm):
        return self.app.post(
            '/register',
            data=dict(email=email, password=password, confirm=confirm),
            follow_redirects=True
        )

    def login(self, email, password):
        return self.app.post(
            '/login',
            data=dict(email=email, password=password),
            follow_redirects=True
        )

    def logout_user(self):
        return self.app.get(
            '/logout',
            follow_redirects=True
        )

    # TESTS
    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_valid_user_registration(self):
        response = self.register('test11@test11.com',
                                 'PasswIsGood13#$',
                                 'PasswIsGood13#$')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<strong>Success!</strong> Thanks for registering.', response.data)

    def test_invalid_user_registration_different_passwords(self):
        response = self.register('test22@test22.com',
                                 'Pass129',
                                 'Different')
        self.assertIn(b'Field must be equal to password.', response.data)

    def test_invalid_user_registration_duplicate_email(self):
        response = self.register('test33@test33.com',
                                 '%^#@12sa',
                                 '%^#@12sa')
        self.assertEqual(response.status_code, 200)
        response = self.register('test33@test33.com',
                                 '89298dka',
                                 '89298dka')
        self.assertIn(b'<strong>Error!</strong> Unable to process registration.', response.data)


if __name__ == "__main__":
    unittest.main()

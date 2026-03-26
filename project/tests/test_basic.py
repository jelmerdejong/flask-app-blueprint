# project/test_basic.py
import unittest

from project.tests.base import BaseTestCase


class BasicTests(BaseTestCase):
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
        return self.app.post(
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
        self.assertIn(b'Success! Thanks for registering.', response.data)

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
        self.assertIn(b'Error! Unable to process registration.', response.data)


if __name__ == "__main__":
    unittest.main()

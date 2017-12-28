# project/test_users.py
import unittest

from project import app, db, mail
from project.models import User


class UserTests(unittest.TestCase):
    # SETUP AND TEARDOWN
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/test'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

        mail.init_app(app)
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

    def create_admin_user(self):
        new_user = User(email='admin@flaskappblueprint.com', password='adminpassword123')
        new_user.role = 'admin'
        new_user.email_confirmed = True
        db.session.add(new_user)
        db.session.commit()

    def create_email_confirmed_user(self):
        new_user = User(email='confirmed@flaskappblueprint.com', password='C0nFirmed!')
        new_user.email_confirmed = True
        db.session.add(new_user)
        db.session.commit()


    # TESTS
    def test_user_registration_form_displays(self):
        response = self.app.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Get started with a free account', response.data)

    def test_valid_user_registration(self):
        self.app.get('/register', follow_redirects=True)
        response = self.register('test11@test11.com', 'c0mple*p$ssword!', 'c0mple*p$ssword!')
        self.assertIn(b'Thanks for registering', response.data)

    def test_duplicate_email_user_registration_error(self):
        self.app.get('/register', follow_redirects=True)
        self.register('test@test.com', 'N98=Q\?r-Y=!=jjg', 'N98=Q\?r-Y=!=jjg')
        self.app.get('/register', follow_redirects=True)
        response = self.register('test@test.com', 'N98=Q\?r-Y=!=jjg', 'N98=Q\?r-Y=!=jjg')
        self.assertIn(b'Unable to process registration.', response.data)

    def test_missing_field_user_registration_error(self):
        self.app.get('/register', follow_redirects=True)
        response = self.register('test@test.com', ')gm@c8Zqw)Q4+B3P', '')
        self.assertIn(b'This field is required.', response.data)

    def test_login_form_displays(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Log In', response.data)
        self.assertIn(b'Sign up for free!', response.data)
        self.assertIn(b'Forgot your password?', response.data)

    def test_valid_login(self):
        self.create_email_confirmed_user()
        self.app.get('/login', follow_redirects=True)
        response = self.login('confirmed@flaskappblueprint.com', 'C0nFirmed!')
        self.assertIn(b'confirmed@flaskappblueprint.com', response.data)
        self.assertIn(b'You are now successfully logged in.', response.data)

    def test_login_without_registering(self):
        self.app.get('/login', follow_redirects=True)
        response = self.login('nonexistinguser@flaskappblueprint.com', 'LZ-u}>(R-wn!q45g')
        self.assertIn(b'Incorrect login credentials.', response.data)

    def test_valid_logout(self):
        self.create_email_confirmed_user()
        self.app.get('/login', follow_redirects=True)
        response = self.login('confirmed@flaskappblueprint.com', 'C0nFirmed!')
        self.assertIn(b'You are now successfully logged in.', response.data)
        response = self.app.get('/logout', follow_redirects=True)
        self.assertIn(b'You are now logged out.', response.data)

    def test_invalid_logout_within_being_logged_in(self):
        response = self.app.get('/logout', follow_redirects=True)
        self.assertIn(b'Log In', response.data)

    def test_user_profile_page(self):
        self.create_email_confirmed_user()
        self.app.get('/login', follow_redirects=True)
        response = self.login('confirmed@flaskappblueprint.com', 'C0nFirmed!')
        response = self.app.get('/user_profile')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Email Address', response.data)
        self.assertIn(b'Account Actions', response.data)
        self.assertIn(b'Statistics', response.data)
        self.assertIn(b'Member since', response.data)

    def test_extra_verification_email_after_logging_in(self):
        self.app.get('/register', follow_redirects=True)
        response = self.register('test11@test11.com', 'c0mple*p$ssword!', 'c0mple*p$ssword!')
        self.assertIn(b'Thanks for registering', response.data)
        self.app.get('/login', follow_redirects=True)
        response = self.login('test11@test11.com', 'c0mple*p$ssword!')
        self.assertIn(b'Email sent to confirm your email address', response.data)

    def test_user_profile_without_logging_in(self):
        response = self.app.get('/user_profile')
        self.assertEqual(response.status_code, 302)
        self.assertIn(b'You should be redirected automatically to target URL:', response.data)
        self.assertIn(b'/login?next=%2Fuser_profile', response.data)

    def test_change_email_address_page(self):
        self.create_email_confirmed_user()
        self.app.get('/login', follow_redirects=True)
        response = self.login('confirmed@flaskappblueprint.com', 'C0nFirmed!')
        response = self.app.get('/email_change')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Change Email Address', response.data)

    def test_change_email_address(self):
        self.create_email_confirmed_user()
        self.app.get('/login', follow_redirects=True)
        response = self.login('confirmed@flaskappblueprint.com', 'C0nFirmed!')
        self.app.post('/email_change', data=dict(email='confirmednew@flaskappblueprint.com'), follow_redirects=True)
        response = self.app.get('/user_profile')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Email Address', response.data)
        self.assertIn(b'confirmednew@flaskappblueprint.com', response.data)
        self.assertNotIn(b'confirmed@flaskappblueprint.com', response.data)

    def test_change_email_address_with_existing_email(self):
        self.create_email_confirmed_user()
        self.app.get('/login', follow_redirects=True)
        response = self.login('confirmed@flaskappblueprint.com', 'C0nFirmed!')
        response = self.app.post('/email_change', data=dict(email='confirmed@flaskappblueprint.com'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sorry, that email already exists!', response.data)
        self.assertIn(b'Change Email Address', response.data)

    def test_change_email_without_logging_in(self):
        response = self.app.get('/email_change')
        self.assertEqual(response.status_code, 302)
        self.assertIn(b'You should be redirected automatically to target URL:', response.data)
        self.assertIn(b'/login?next=%2Femail_change', response.data)
        response = self.app.post('/email_change', data=dict(email='testemail@test.com'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Log In', response.data)
        self.assertIn(b'Sign up for free!', response.data)

    def test_change_password_page(self):
        self.create_email_confirmed_user()
        self.app.get('/login', follow_redirects=True)
        response = self.login('confirmed@flaskappblueprint.com', 'C0nFirmed!')
        response = self.app.get('/password_change')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Change Password', response.data)

    def test_change_password(self):
        self.create_email_confirmed_user()
        self.app.get('/login', follow_redirects=True)
        response = self.login('confirmed@flaskappblueprint.com', 'C0nFirmed!')
        response = self.app.post('/password_change', data=dict(password='MyNewPassword1234'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Password has been updated!', response.data)
        self.assertIn(b'User Profile', response.data)

    def test_change_password_logging_in(self):
        response = self.app.get('/password_change')
        self.assertEqual(response.status_code, 302)
        self.assertIn(b'You should be redirected automatically to target URL:', response.data)
        self.assertIn(b'/login?next=%2Fpassword_change', response.data)
        response = self.app.post('/password_change', data=dict(password='MyNewPassword1234'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Log In', response.data)
        self.assertIn(b'Sign up for free!', response.data)

    def test_admin_site_valid_access(self):
        self.create_admin_user()
        self.app.get('/login', follow_redirects=True)
        response = self.login('admin@flaskappblueprint.com', 'adminpassword123')
        self.assertIn(b'admin@flaskappblueprint.com', response.data)
        self.assertIn(b'View Users (Admin)', response.data)
        response = self.app.get('/admin_view_users')
        self.assertIn(b'Admin: All Users', response.data)

    def test_admin_site_invalid_access(self):
        response = self.app.get('/admin_view_users')
        self.assertEqual(response.status_code, 302)
        self.assertIn(b'You should be redirected automatically to target URL:', response.data)
        self.assertIn(b'/login?next=%2Fadmin_view_users', response.data)
        self.create_email_confirmed_user()
        self.app.get('/login', follow_redirects=True)
        response = self.login('confirmed@flaskappblueprint.com', 'C0nFirmed!')
        self.assertIn(b'confirmed@flaskappblueprint.com', response.data)
        self.assertNotIn(b'View Users (Admin)', response.data)
        response = self.app.get('/admin_view_users')
        self.assertEqual(response.status_code, 403)
        self.assertIn(b'403', response.data)
        self.assertIn(b'Forbidden', response.data)


if __name__ == "__main__":
    unittest.main()

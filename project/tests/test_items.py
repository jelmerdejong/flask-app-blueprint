import unittest

from project import app, db, mail
from project.models import Items, User


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

    def register_user(self):
        new_user = User(email='user1@flaskappblueprint.com', password='User$$1!')
        new_user.email_confirmed = True
        db.session.add(new_user)
        db.session.commit()

    def register_user2(self):
        new_user = User(email='user2@flaskappblueprint.com', password='User$$2&')
        new_user.email_confirmed = True
        db.session.add(new_user)
        db.session.commit()

    def login_user(self):
        self.app.get('/login', follow_redirects=True)
        self.login('user1@flaskappblueprint.com', 'User$$1!')

    def login_user2(self):
        self.app.get('/login', follow_redirects=True)
        self.login('user2@flaskappblueprint.com', 'User$$2&')

    def logout_user(self):
        self.app.get('/logout', follow_redirects=True)

    def add_items(self):
        self.register_user()
        self.register_user2()
        user1 = User.query.filter_by(email='user1@flaskappblueprint.com').first()
        user2 = User.query.filter_by(email='user2@flaskappblueprint.com').first()
        item1 = Items('Lorem ipsum', 'Consectetur adipiscing elit', user1.id)
        item2 = Items('Aliquam felis', ' Pellentesque volutpat consequat est.', user1.id)
        item3 = Items('Sed a dapibus', 'Fusce gravida posuere turpis, ut leo suscipit at.', user1.id)
        item4 = Items('Vestibulum', 'Nullam fermentum scelerisque sem', user2.id)
        item5 = Items('Sed sodales', 'Mauris pellentesque leo a erat finibus semper', user2.id)
        db.session.add(item1)
        db.session.add(item2)
        db.session.add(item3)
        db.session.add(item4)
        db.session.add(item5)
        db.session.commit()

    # TESTS
    def test_main_page(self):
        self.add_items()
        self.login_user()
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Lorem ipsum', response.data)
        self.assertIn(b'Aliquam felis', response.data)
        self.assertIn(b'user1@flaskappblueprint.com', response.data)
        self.assertNotIn(b'Vestibulum', response.data)
        self.assertNotIn(b'Sed sodales', response.data)

    def test_add_item_page(self):
        self.register_user()
        self.login_user()
        response = self.app.get('/add_item', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Add Item', response.data)

    def test_add_item(self):
        self.register_user()
        self.login_user()
        response = self.app.post(
            '/add_item',
            data=dict(name='Rare Item',
                      notes='Test if Special Item is Added'),
            follow_redirects=True)
        self.assertIn(b'Item added successfully!', response.data)
        self.assertIn(b'Rare Item', response.data)
        self.assertIn(b'Test if Special Item is Added', response.data)

    def test_add_invalid_item(self):
        self.register_user()
        self.login_user()
        response = self.app.post(
            '/add_item',
            data=dict(name='',
                      notes='Test if item without title is added'),
            follow_redirects=True)
        self.assertIn(b'This field is required.', response.data)

    def test_item_edit_valid_user(self):
        self.add_items()
        self.login_user()
        response = self.app.get('/edit_item/2', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Aliquam felis', response.data)
        self.assertIn(b'user1@flaskappblueprint.com', response.data)

    def test_item_edit_invalid_user(self):
        self.add_items()
        self.login_user2()
        response = self.app.get('/edit_item/2', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Incorrect permissions to access this item.', response.data)

    def test_item_edit_invalid_item(self):
        self.add_items()
        self.login_user2()
        response = self.app.get('/edit_item/98', follow_redirects=True)
        self.assertIn(b'Item does not exist.', response.data)

    def test_item_delete_valid_user(self):
        self.add_items()
        self.login_user()
        response = self.app.get('/delete_item/2', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'was deleted', response.data)

    def test_item_delete_invalid_user(self):
        self.add_items()
        self.login_user2()
        response = self.app.get('/delete_item/2', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Incorrect permissions to delete this item', response.data)

    def test_item_delete_invalid_item(self):
        self.add_items()
        self.login_user2()
        response = self.app.get('/delete_item/99', follow_redirects=True)
        self.assertEqual(response.status_code, 404)

    def test_item_all_items(self):
        self.add_items()
        self.login_user()
        response = self.app.get('/all_items', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Lorem ipsum', response.data)
        self.assertIn(b'Aliquam felis', response.data)
        self.assertIn(b'Sed a dapibus', response.data)
        self.assertNotIn(b'Vestibulum', response.data)
        self.assertNotIn(b'Sed sodales', response.data)
        self.logout_user()
        self.login_user2()
        response = self.app.get('/all_items', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Vestibulum', response.data)
        self.assertIn(b'Sed sodales', response.data)
        self.assertNotIn(b'Lorem ipsum', response.data)
        self.assertNotIn(b'Aliquam felis', response.data)
        self.logout_user()


if __name__ == "__main__":
    unittest.main()

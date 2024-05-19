import unittest
from app import create_app, db
from app.models import Drink

class DatabaseOperationTestCase(unittest.TestCase):
    def setUp(self):
        # Setup the application with the testing configuration
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_drink(self):
        drink = Drink(name='Mojito', type='alcoholic', description='A minty classic cocktail.')
        db.session.add(drink)
        db.session.commit()
        self.assertTrue(Drink.query.filter_by(name='Mojito').first() is not None)

    def test_read_drink(self):
        drink = Drink(name='Lemonade', type='non-alcoholic', description='Fresh and sweet.')
        db.session.add(drink)
        db.session.commit()
        query_drink = Drink.query.filter_by(name='Lemonade').first()
        self.assertIsNotNone(query_drink)
        self.assertEqual(query_drink.type, 'non-alcoholic')

    def test_update_drink(self):
        drink = Drink(name='Pina Colada', type='alcoholic', description='Tropical drink.')
        db.session.add(drink)
        db.session.commit()
        drink_to_update = Drink.query.filter_by(name='Pina Colada').first()
        drink_to_update.description = 'A refreshing tropical cocktail.'
        db.session.commit()
        updated_drink = Drink.query.filter_by(name='Pina Colada').first()
        self.assertEqual(updated_drink.description, 'A refreshing tropical cocktail.')

    def test_delete_drink(self):
        drink = Drink(name='Margarita', type='alcoholic', description='Sour tequila drink.')
        db.session.add(drink)
        db.session.commit()
        Drink.query.filter_by(name='Margarita').delete()
        db.session.commit()
        self.assertIsNone(Drink.query.filter_by(name='Margarita').first())

if __name__ == '__main__':
    unittest.main()

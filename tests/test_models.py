import unittest
from functools import reduce

from redshift.models.dao import Dao


class TestModel(unittest.TestCase):
    dao = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.dao = Dao(echo=True)

    @classmethod
    def tearDownClass(cls) -> None:
        del cls.dao

    def setUp(self):
        self.dao.reset_engine()

    def tearDown(self):
        self.dao.reset_engine()

    def test_create_drop(self):
        """test creating & dropping tables

        methods:
          * dao.create_all
          * dao.drop_all
          * dao.all_tables

        """
        exp = {
            'sales', 'listing', 'event', 'users', 'venue', 'category', 'date'
        }
        tables = self.dao.all_tables()
        if exp == set(tables):
            return
        else:
            self.dao.drop_all()
            self.dao.create_all()
            self.assertEqual(exp, set(self.dao.all_tables()))

    def test_load(self):
        """test load sample & count

        methods:
          * dao.load_sample
          * dao.count_<table_name>

        """
        mappings = [(self.dao.count_users, 49990), (self.dao.count_venue, 202),
                    (self.dao.count_category, 11), (self.dao.count_date, 365),
                    (self.dao.count_event, 8798),
                    (self.dao.count_listing, 192497),
                    (self.dao.count_sales, 172456)]

        if reduce(lambda x, y: x and y, (f() == exp for f, exp in mappings)):
            return
        else:
            self.dao.drop_all()
            self.dao.create_all()
            self.dao.load_sample()

            for f, exp in mappings:
                self.assertEqual(f(), exp)

    def test_total_sales(self):
        dt = '2008-01-05'
        exp = 210
        self.assertEqual(exp, self.dao.total_sales(dt))


if __name__ == '__main__':
    unittest.main(verbosity=2)

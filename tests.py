import unittest
import model
from model import Url, Visit
from sqlalchemy import Column, Integer, DateTime, String, ForeignKey, Text, desc, join, func

"""Note: we would obviously not be committing tests to a production database
but I think this is the best way of demoing testing for simplicity"""

class ModelTests(unittest.TestCase):

	def setUp(self):
		self.empty = []
		self.code = "VDuNHc"
		self.url = "https://google.com"

	def test_empty(self):
		self.assertTrue(model.is_empty(self.empty))
		self.assertFalse(model.is_empty(self.code))

	def test_create_code(self):
		#due to the not so great nature of adding false entries to 
		#the database, I'm grouping a few tests here
		model.db_connect()
		less = model.db.query(func.count(Url.code)).first()
		code = model.create_code(self.url)
		greater = model.db.query(func.count(Url.code)).first()
		self.assertGreater(greater, less)
		self.assertEqual(len(code), 6)
		model.db.query(Url).filter_by(code=code).delete()
		model.db.commit()

	def test_url_info_url(self):
		url = model.url_info(self.code)
		self.assertEqual(url.url, "https://www.heroku.com/")

	def test_url_info_code(self):
		url = model.url_info(self.code)
		self.assertEqual(url.code, self.code)

	def test_url_info_visits(self):
		url = model.url_info(self.code)
		self.assertGreater(url.visits, 4)

	def test_recently_shortened(self):
		recent = model.recently_shortened()
		self.assertFalse(model.is_empty(recent))

	def test_most_popular_len(self):
		popular = model.most_popular()
		self.assertEqual(len(popular), 10)

	def test_most_popular_empty(self):
		popular = model.most_popular()
		self.assertFalse(model.is_empty(popular[1]["url"]))

	def test_most_popular_code(self):
		popular = model.most_popular()
		self.assertEqual(len(popular[1]["code"]), 6)

	def test_most_popular_visits(self):
		popular = model.most_popular()
		self.assertGreater(popular[1]["visits"], 0)

	def test_log_visit(self):
		#due to the not so great nature of adding false entries to , 
		#I'm grouping a few tests here
		less = model.db.query(func.count(Visit.id)).first()
		original = model.url_info(self.code)
		model.log_visit(self.code)
		greater = model.db.query(func.count(Visit.id)).first()
		new = model.url_info(self.code)
		self.assertGreater(greater, less)
		self.assertEqual(original.url, new.url)

if __name__ == '__main__':
    unittest.main()
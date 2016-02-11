from django.test import TestCase
from sway.models import EventLocations

class AddLocationTest(TestCase):
	def setUp(self):
		EventLocations.objects.create(event_location_name="test")

	def test_location_not_null(self):
		location = EventLocations.objects.get(event_location_name="test")
		self.assertEqual(location.event_location_name, "test")
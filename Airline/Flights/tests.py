from django.test import Client, TestCase
from .models import Flight, Passenger, Airport
from django.db.models import Max

# Create your tests here.

class Test(TestCase):

    def setUp(self):
        a1 = Airport.objects.create(code="BLR", city='Bangalore')
        a2 = Airport.objects.create(code='LND', city='London')

        Flight.objects.create(origin=a1, destination=a2, duration=415)
        Flight.objects.create(origin=a1, destination=a1, duration=425)
        Flight.objects.create(origin=a1, destination=a2, duration=-420)

    def test_departures_count(self):
        a = Airport.objects.get(code="BLR")
        self.assertEqual(a.departures.count(), 3)

    def test_arrivals_count(self):
        a = Airport.objects.get(code='BLR')
        self.assertEqual(a.arrivals.count(), 1)

    def test_valid_flight(self):
        a1 = Airport.objects.get(code='BLR')
        a2 = Airport.objects.get(code='LND')
        f1 = Flight.objects.get(origin=a1, destination=a2, duration=415)
        self.assertTrue(f1.is_valid_flight())

    def test_invalid_flight_destination(self):
        a1 = Airport.objects.get(code='BLR')
        f1 = Flight.objects.get(origin=a1, destination=a1, duration=425)
        self.assertFalse(f1.is_valid_flight())

    def test_invalid_flight_duration(self):
        a1 = Airport.objects.get(code="BLR")
        a2 = Airport.objects.get(code='LND')
        f1 = Flight.objects.get(origin=a1, destination=a2, duration=-420)
        self.assertFalse(f1.is_valid_flight())

    def test_index(self):
        c = Client()
        response = c.get('/Flights/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['flights'].count(), 3)

    def test_valid_flightpage(self):
        a1 = Airport.objects.get(code='BLR')
        f = Flight.objects.get(origin=a1, destination=a1)

        c = Client()
        response = c.get(f'/Flights/{f.id}')
        self.assertEqual(response.status_code, 200)

    def test_invalid_flightpage(self):
        max_id = Flight.objects.all().aggregate(Max("id"))['id__max']

        c = Client()
        response = c.get(f'/Flights/{max_id + 1}')
        self.assertEqual(response.status_code, 404)

    def test_flight_passenger(self):
        f = Flight.objects.get(pk=1)
        p = Passenger.objects.create(first='John', last='Mathews')
        f.passengers.add(p)

        c = Client()
        response = c.get(f'/Flights/{f.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['passengers'].count(), 1)

    def test_flight_invalidpassenger(self):
        f = Flight.objects.get(pk=1)
        p = Passenger.objects.create(first='Peter', last='Andrew')

        c = Client()
        response = c.get(f'/Flights/{f.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['non_passengers'].count(), 1)







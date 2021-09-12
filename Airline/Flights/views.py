from django.shortcuts import render
from .models import Flight, Passenger
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse


# Create your views here.
def index(request):
    return render(request, 'Flights/index.html', {
        "flights": Flight.objects.all()
    })


def flight(request, flight_id):

    try:
        f = Flight.objects.get(pk=flight_id)
    except Flight.DoesNotExist:
        raise Http404(f'Flight {flight_id} is not present')

    p = f.passengers.all()
    non_passengers = Passenger.objects.exclude(flight=f).all()
    return render(request, 'Flights/flight.html', {
        "flight": f,
        "passengers": p,
        "non_passengers": non_passengers
        })


def book(request, flight_id):
    if request.method == "POST":
        f = Flight.objects.get(pk=flight_id)
        passenger_id = int(request.POST["passengerid"])
        p = Passenger.objects.get(pk=passenger_id)
        p.flight.add(f)
        return HttpResponseRedirect(reverse("flight", args=(flight_id,)))

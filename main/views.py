from django.db.models import Count
from django.shortcuts import render
from django.contrib.auth import logout as django_logout
from services.models import Service, ServiceHistory

def home(request):
    # Get the 5 most popular services to display on the homepage
    service_counts = ServiceHistory.objects.values('service').annotate(
        request_count=Count('service')).order_by('-request_count')[:5]

    # Get the actual service objects with their request counts
    popular_services = []
    for item in service_counts:
        service = Service.objects.get(id=item['service'])
        service.request_count = item['request_count']
        popular_services.append(service)

    return render(request, "main/home.html", {'popular_services': popular_services})

def logout(request):
    django_logout(request)
    return render(request, "main/logout.html")


def most_requested_services(request):
    # Get the count of requests for each service
    service_counts = ServiceHistory.objects.values('service').annotate(
        request_count=Count('service')).order_by('-request_count')[:10]

    # Get the actual service objects with their request counts
    popular_services = []
    for item in service_counts:
        service = Service.objects.get(id=item['service'])
        service.request_count = item['request_count']
        popular_services.append(service)

    return render(request, 'services/most_requested.html', {
        'popular_services': popular_services
    })

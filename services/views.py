from django.core.checks import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect

from users.models import Company, Customer, User

from .models import Service, ServiceHistory
from .forms import CreateNewService, RequestServiceForm


def service_list(request):
    services = Service.objects.all().order_by("-date")
    return render(request, 'services/list.html', {'services': services})


def index(request, id):
    service = Service.objects.get(id=id)
    return render(request, 'services/single_service.html', {'service': service})


def create(request):
    if not request.user.is_authenticated or not request.user.is_company:
        messages.error(request, "You need to be logged in as a company to create services.")
        return redirect('login_user')

    # Get the company's field to restrict service creation
    company = Company.objects.get(user=request.user)
    allowed_fields = []

    # If the company is "All in One", they can create any type of service
    if company.field == 'All in One':
        allowed_fields = [
            ('Air Conditioner', 'Air Conditioner'),
            ('Carpentry', 'Carpentry'),
            ('Electricity', 'Electricity'),
            ('Gardening', 'Gardening'),
            ('Home Machines', 'Home Machines'),
            ('House Keeping', 'House Keeping'),
            ('Interior Design', 'Interior Design'),
            ('Locks', 'Locks'),
            ('Painting', 'Painting'),
            ('Plumbing', 'Plumbing'),
            ('Water Heaters', 'Water Heaters')
        ]
    else:
        # Otherwise, they can only create services of their field
        allowed_fields = [(company.field, company.field)]

    if request.method == 'POST':
        form = CreateNewService(request.POST, choices=allowed_fields)
        if form.is_valid():
            # Get the form data
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            price_hour = form.cleaned_data['price_hour']
            field = form.cleaned_data['field']

            # Create a new service
            service = Service(
                company=company,
                name=name,
                description=description,
                price_hour=price_hour,
                field=field
            )
            service.save()

            messages.success(request, f"Your service '{name}' has been created successfully!")
            return redirect('company_profile', name=request.user.username)
    else:
        form = CreateNewService(choices=allowed_fields)

    return render(request, 'services/create.html', {'form': form})


def service_field(request, field):
    # search for the service present in the url
    field = field.replace('-', ' ').title()
    services = Service.objects.filter(
        field=field)
    return render(request, 'services/field.html', {'services': services, 'field': field})


def request_service(request, id):
    service = get_object_or_404(Service, id=id)

    if not request.user.is_authenticated or not request.user.is_customer:
        messages.error(request, "You must be logged in as a customer to request services.")
        return redirect('login_user')

    if request.method == 'POST':
        form = RequestServiceForm(request.POST)
        if form.is_valid():
            address = form.cleaned_data['address']
            service_time = form.cleaned_data['service_time']

            # Get the customer
            customer = Customer.objects.get(user=request.user)

            # Calculate price
            price = service_time * service.price_hour

            # Create service history record
            ServiceHistory.objects.create(
                customer=customer,
                service=service,
                address=address,
                service_time=service_time,
                price=price
            )

            messages.success(request, f"You've successfully requested {service.name} service!")
            return redirect('customer_profile', name=request.user.username)
    else:
        form = RequestServiceForm()

    return render(request, 'services/request_service.html', {
        'form': form,
        'service': service
    })
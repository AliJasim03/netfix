import datetime

from django.contrib import messages
from django.shortcuts import render, redirect

from services.models import Service, ServiceHistory
from users.models import User, Company, Customer


def home(request):
    return render(request, 'users/profile.html', {'user': request.user})


def customer_profile(request, name):
    try:
        user = User.objects.get(username=name)
        if not user.is_customer:
            messages.error(request, "This user is not a customer.")
            return redirect('home')

        # Get customer's age from date of birth
        customer = Customer.objects.get(user=user)
        today = datetime.date.today()
        user_age = None
        if customer.date_of_birth:
            user_age = today.year - customer.date_of_birth.year - (
                        (today.month, today.day) < (customer.date_of_birth.month, customer.date_of_birth.day))

        # Get service history
        service_history = ServiceHistory.objects.filter(customer=customer).order_by('-request_date')

        return render(request, 'users/profile.html', {
            'user': user,
            'user_age': user_age,
            'sh': service_history
        })
    except User.DoesNotExist:
        messages.error(request, "Customer not found.")
        return redirect('home')


def company_profile(request, name):
    # Fetch the company user and all of the services available by it
    try:
        user = User.objects.get(username=name)
        if not user.is_company:
            messages.error(request, "This user is not a company.")
            return redirect('home')

        services = Service.objects.filter(
            company=Company.objects.get(user=user)).order_by("-date")

        return render(request, 'users/profile.html', {
            'user': user,
            'services': services
        })
    except User.DoesNotExist:
        messages.error(request, "Company not found.")
        return redirect('home')
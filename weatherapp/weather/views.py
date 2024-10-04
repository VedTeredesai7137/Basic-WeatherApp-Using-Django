import requests
from django.shortcuts import render, redirect
from .models import City
from .forms import CityForm


def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=271d1234d3f497eed5b1d80a07b3fcd1'

    err_msg = ''
    message = ''
    message_class = ''

    # Handle deletion if the 'city_id' is present in the POST request
    if request.method == 'POST' and 'city_id' in request.POST:
        city_id = request.POST.get('city_id')
        City.objects.get(id=city_id).delete()
        return redirect('/')  # Redirect to refresh the page after deletion


    # Handle city addition
    if request.method == 'POST' and 'city_id' not in request.POST:
        form = CityForm(request.POST)
        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()

            if existing_city_count == 0:
                r = requests.get(url.format(new_city)).json()
                print(r)
                if r['cod'] == 200:
                    form.save()
                else:
                    err_msg = 'City does not exist in the world'
            else :
                err_msg ='City already exist'

        if err_msg:
            message = err_msg
            message_class = 'is-danger'

        else:
            message = 'City added Sucessfully'
            message_class = 'is-success'



    print(err_msg)



    form = CityForm()

    cities = City.objects.all()

    weather_data = []

    for city in cities:
        r = requests.get(url.format(city)).json()

        # Check if the response contains 'main' key
        if r.get('main'):
            city_weather = {
                'id': city.id,  # Add ID to use in delete functionality
                'city': city.name,
                'temperature': r['main']['temp'],
                'humidity': r['main']['humidity'],
                'description': r['weather'][0]['description'],
                'icon': r['weather'][0]['icon'],
            }
            weather_data.append(city_weather)
        else:
            # Handle cases where the API response doesn't contain expected data
            print(f"Error fetching data for city: {city.name}. Response: {r}")

    context = {'weather_data': weather_data, 'form': form, 'message': message, 'message_class' : message_class }

    return render(request, 'weather/weather.html', context)
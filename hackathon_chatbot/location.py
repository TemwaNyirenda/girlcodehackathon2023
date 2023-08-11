from geopy.geocoders import Nominatim

def get_city(longitude, latitude):
    geolocator = Nominatim(user_agent="geoapiExercises")

    print("2nd lat " + latitude )
    print("2nd long " + longitude )

    location = geolocator.reverse(latitude+", "+longitude)

    print("location " + str(location))

    address = location.raw['address']

    print("address " + str(address))

    city = address.get('city', '')

    print("city" + city)

    return city


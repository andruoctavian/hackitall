
LOCATION_KEY = 'location'
STOPOVER_KEY = 'stopover'
ROUTES_KEY = 'routes'


def adapt_google(way_points):
    google_formatted = []
    for way_point in way_points:
        google_formatted.append({
            LOCATION_KEY: str(way_point[1]) + ',' + str(way_point[0]),
            STOPOVER_KEY: True
        })

    return google_formatted


def check_google_response(google_response):
    if len(google_response[ROUTES_KEY]) == 0:
        return False

    return True

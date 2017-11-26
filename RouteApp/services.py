
LOCATION_KEY = 'location'
STOPOVER_KEY = 'stopover'


def adapt_google(way_points):
    google_formatted = []
    for way_point in way_points:
        google_formatted.append({
            LOCATION_KEY: str(way_point[0]) + ',' + str(way_point[1]),
            STOPOVER_KEY: True
        })

    return google_formatted


def adapt_invert(coordinates):
    if coordinates is None:
        return None

    coord1, coord2 = coordinates.split(",")

    return coord2 + "," + coord1

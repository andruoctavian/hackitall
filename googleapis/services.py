
def adapt_routes_object(object):
    lat_north = object['routes'][0]['bounds']['northeast']['lat']
    long_east = object['routes'][0]['bounds']['northeast']['long']
    lat_south = object['routes'][0]['bounds']['southwest']['lat']
    long_west = object['routes'][0]['bounds']['southwest']['long']

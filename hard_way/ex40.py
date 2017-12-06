cities = {'CA':'San Fancisco','MI':'Detroit','FL':'Jacksonvile'}
cities['NY'] = 'New Yourk'
cities['OR'] = 'Portland'

def find_city(themap,state):
    if state in themap:
        return themap[state]
    else:
        return "Not found."

#ok pay attention !
cities['_find'] = find_city


while True:
    print "State?(ENTER to quit)",
    state = raw_input(">")
    if not state:break
    #this line is the most important ever!study!
    city_found = find_city(cities,state)
    print city_found
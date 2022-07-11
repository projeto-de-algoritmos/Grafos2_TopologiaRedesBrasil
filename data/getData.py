import pandas as pd
from geopy import distance


edges = [("DF", "TO"), ("DF", "GO"), ("DF", "AC"), ("DF", "RJ"), ("DF", "MG"),
         ("DF", "MA"), ("DF", "CE"), ("DF", "AM"), ("DF",
                                                    "SP"), ("GO", "MT"), ("GO", "TO"),
         ("TO", "PA"), ("MT", "MS"), ("MT", "RO"), ("RO", "AC"), ("MS", "PR"), ("PR", "RS"), ("RS", "SC"), ("SC", "SP"), ("SP", "PR"), ("RS", "SP"), ("PR", "SC"), ("SP", "RJ"), ("SP",
                                                                                                                                                                                  "RJ"), ("SP", "MG"), ("SP", "CE"), ("RJ", "MG"), ("RJ", "ES"), ("ES", "BA"), ("MG", "BA"), ("BA", "CE"), ("BA", "SE"), ("SE", "AL"), ("AL", "PE"), ("PA", "MA"),
         ("BA", "PB"), ("PE", "PI"), ("PI",
                                      "MA"), ("AM", "RR"), ("RR", "CE"), ("CE", "RN"),
         ("PE", "PB"), ("RN", "PB"), ("RN", "PB"), ("PB", "PB"),
         ("AM", "AP"), ("AP", "PA")]

# CREATE A DICTIONARY OF CAPITAL AND DISTANCE
capitals_distances = []


path = './br_cities.csv'
csv_file = pd.read_csv(path)

# GET THE DISTANCE BETWEEN states in city_connections and that match the edges
for row in csv_file.iterrows():
    for row2 in csv_file.iterrows():
        if row[1]['state'] != row2[1]['state'] and (row[1]['state'], row2[1]['state']) in edges:
            dist = distance.distance(
                (row[1]['lat'], row[1]['lng']),
                (row2[1]['lat'], row2[1]['lng'])
            ).km
            # print(row[1]['city'], row2[1]['city'], dist)
            capitals_distances.append(
                (row[1]['state'], row2[1]['state'], dist))
            # csv_file.loc[row[0], 'distance'] = dist


# # print in a pretty format
print(pd.DataFrame(capitals_distances, columns=[
      'state1', 'state2', 'distance']))

# export capital distances to csv
# pd.DataFrame(capitals_distances, columns=['state1', 'state2', 'distance']).to_csv(
# './states_distances.csv')

print(capitals_distances)

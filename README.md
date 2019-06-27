## Horse-Racing-Data-Extraction ## 

### Objective: ###
Harvest 6 months of online historical data of horse races. This extraction included demographic information from the horse, the jockey's name,  different details in regards to the venue, and off course, the horse's position at the end of the race.

The extractor:
Programming language: Python
Packages / libraries: html, request, csv, datetime, time, pandas and NumPy

The extractor was divided into two main scripts: one in charge of harvesting the URL of each race that happen between July 1st, 2018 and December 31st, 2018; and the other used to grab the desired information from each of those URLs. It is worth mentioning that from each race (each URL) the same information for all the participants of the race was grabbed.

The features:
From each race, the following information was collected:

Location: city in which the race took place.
Date: date of the race.
Time: time of the day of the race.
Going: condition of the surface.
Surface: type of surface.
Lenght: lenght of the track.
From each participant of the race (horse), the following information was collected:

Position: position at the end of the race.
Distance from first: distance between the horse and the winner.
Stall: stall where the horse started the race.
Name: name of the horse.
Age: age of the horse.
Weight: weight of the horse.
Odds: odds of winning (given by the public).
Trainer: trainer's name.
Jockey: jockey's name.

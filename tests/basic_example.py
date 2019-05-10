from dataknead import Knead

# Convert csv to json
Knead("input/cities.csv").write("output/cities.json")

# Get city names and write to csv
Knead("input/cities.csv").map("city").write("output/city-names.csv")

# Get only cities located in Italy
Knead("input/cities.csv").filter(lambda r:r["country"] == "it").write("output/cities-italy.csv")
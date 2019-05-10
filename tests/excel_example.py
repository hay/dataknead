from dataknead import Knead

# Single sheet Excel
print(Knead("input/cities.xlsx"))

# Multisheet Excel
print(Knead("input/cities-multisheet.xlsx"))

# Convert from CSV to XLS
Knead("input/cities.csv").write("output/cities.xls")
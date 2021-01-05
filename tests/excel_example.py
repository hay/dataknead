from dataknead import Knead

# Print single sheet Excel
print(Knead("input/cities.xlsx"))

# Print multisheet Excel
print(Knead("input/cities-multisheet.xlsx"))

# Print multisheet Excel and use the header for dict keys
print(Knead("input/cities-multisheet.xlsx", has_header = True))

# Convert from CSV to XLSX
Knead("input/cities.csv").write("output/cities.xlsx")

# Convert from JSON to XLSX
Knead("input/names.json").write("output/names.xlsx")

# Test a weird format that will fail
Knead("input/books.xml").write("output/books.xlsx")
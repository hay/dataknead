from dataknead import Knead

# Print single sheet Excel
Knead("input/cities.xlsx").write("output/cities-excel.csv")

# Print multisheet Excel
Knead("input/cities-multisheet.xlsx").write("output/cities-multisheet-excel.json", indent = 4)

# Print multisheet Excel and use the header for dict keys
Knead("input/cities-multisheet.xlsx", has_header = True).write("output/cities-multisheet-excel-header.json", indent = 4)

# Convert from CSV to XLSX
Knead("input/cities.csv").write("output/cities.xlsx")

# Convert from JSON to XLSX
Knead("input/names.json").write("output/names.xlsx")

# Test a weird format that will fail
Knead("input/books.xml").write("output/books.xlsx")
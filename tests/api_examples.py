from _context import dataknead
from dataknead import Knead

# Read data from file
Knead("input/entity.json")

# Pass data directly
Knead([1,2,3])

# Parse data from string
Knead("[1,2,3]", parse_as="csv")

# Read data from file without a file extension, give the file format
Knead("input/entity", read_as="json")
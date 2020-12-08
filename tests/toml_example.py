from dataknead import Knead

# Convert from JSON to TOML
Knead("input/entity.json").write("output/entity.toml")

# Convert from TOML to JSON
Knead("input/example.toml").write("output/toml_example.json", indent = 4, default = str)
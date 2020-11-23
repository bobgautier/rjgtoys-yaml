
import sys

from rjgtoys.yaml import yaml_load_path, yaml_dump

for path in sys.argv[1:]:
    print(f"Loading {path}")
    data = yaml_load_path(path)
    # Note attribute-style access
    print(f"  Loaded {data.name}: {data.title}")
    yaml_dump(data, sys.stdout)


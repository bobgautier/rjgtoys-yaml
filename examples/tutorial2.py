
import os
from rjgtoys.yaml import yaml_load


path = os.path.join(os.path.dirname(__file__), 'tutorial2.yaml')

with open(path, 'r') as src:
    data = yaml_load(src)

print(data)


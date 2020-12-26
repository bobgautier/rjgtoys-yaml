
import os
from rjgtoys.yaml import yaml_load_path


path = os.path.join(os.path.dirname(__file__), 'tutorial2.yaml')

data = yaml_load_path(path)

print(data)



from rjgtoys.yaml import yaml_load

data = yaml_load("""
top:
  first: 1
  second: 2
  inner:
    a: hello
    b: world
""")

assert data.top.first + data.top.second == 3

greeting = "%s, %s" % (data.top.inner.a, data.top.inner.b)
print(greeting)


import os

from rjgtoys.yaml import yaml_load


def test_loads():

    data = """---
x:
 a: 2
 b: 2
"""

    obj = yaml_load(data)

    assert obj['x']['a'] == 2


def test_load_file():

    d = os.path.dirname(__file__)

    srcpath = os.path.join(d, 'data1.yaml')

    with open(srcpath) as stream:
        data = yaml_load(stream)

    assert data.sequence == [1, 2, 3]

    assert data.mapping.a == 97
    assert data.mapping == dict(a=97, b=98, c=99)

    # from data2.yaml

    assert data.included.data2.name == 'data2'
    assert data.included.data2.id == 42

    # from data3.yaml

    assert data.included.data2.inner.data3 == 333


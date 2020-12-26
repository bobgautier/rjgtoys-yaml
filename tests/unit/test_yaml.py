
import os
import io

import pytest

from rjgtoys.thing import Thing

from rjgtoys.yaml import yaml_load, yaml_load_path, yaml_dump, YamlCantLoad


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

def test_yaml_dump():

    # Keys are deliberately not in alphabetical order

    data = Thing(b=2, a=1)

    out = io.StringIO()

    yaml_dump(data, stream=out)

    result = out.getvalue()
    assert result == """b: 2\na: 1\n"""

def test_load_path_file():

    d = os.path.dirname(__file__)

    srcpath = os.path.join(d, 'data3.yaml')

    data = yaml_load_path(srcpath)

    assert data.data3 == 333

def test_load_path_dir():

    d = os.path.dirname(__file__)

    srcpath = os.path.join(d, 'data.d')

    data = yaml_load_path(srcpath)

    assert len(data) == 2

    s = { x for d in data for x in d.items() }

    assert s == {
        ('file1','content1'),
        ('file2','content2')
    }

def test_load_path_fails():

    with pytest.raises(YamlCantLoad):
        yaml_load_path('/dev/null')

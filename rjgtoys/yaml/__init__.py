# The URL in the below is too long.
# pylint: disable=line-too-long

"""

Deal with YAML

See: https://stackoverflow.com/questions/5121931/in-python-how-can-you-load-yaml-mappings-as-ordereddicts


"""
import io
import os
import stat
import sys

import ruamel.yaml as yaml

from rjgtoys.xc import Error, Title

from rjgtoys.thing import Thing


class YamlCantLoad(Error):
    """Raised on an attempt to load YAML from something that is neither file nor directory."""

    path: str = Title("The path that couldn't be read")

    detail = "Can't read YAML from non-file, non-directory '{path}'"


class IncludeLoader(yaml.Loader):
    # from https://stackoverflow.com/questions/528281/how-can-i-include-a-yaml-file-inside-another
    """
    yaml.Loader subclass handles "!include path/to/foo.yml" directives in config
    files.  When constructed with a file object, the root path for includes
    defaults to the directory containing the file, otherwise to the current
    working directory. In either case, the root path can be overridden by the
    `root` keyword argument.

    When an included file F contain its own !include directive, the path is
    relative to F's location.

    Example:
        YAML file /home/frodo/one-ring.yml
            ---
            Name: The One Ring
            Specials:
                - resize-to-wearer
            Effects:
                - !include path/to/invisibility.yml

        YAML file /home/frodo/path/to/invisibility.yml:
            ---
            Name: invisibility
            Message: Suddenly you disappear!

        Loading:
            data = IncludeLoader(open('/home/frodo/one-ring.yml', 'r')).get_data()

        Result:
            {'Effects': [{'Message': 'Suddenly you disappear!', 'Name':
                'invisibility'}], 'Name': 'The One Ring', 'Specials':
                ['resize-to-wearer']}
    """

    DEFAULT_INCLUDE_TAG="!include"

    DEFAULT_MAPPING_TYPE=Thing

    def __init__(self, *args, **kwargs):
        super(IncludeLoader, self).__init__(*args, **kwargs)

        self.add_constructor(self.DEFAULT_INCLUDE_TAG, self._include)

        self.add_constructor(
            yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
            self._construct_mapping
        )

        self.root = os.path.curdir
        if 'root' in kwargs:
            self.root = kwargs['root']
        else:
            try:
                self.root = os.path.dirname(self.stream.name)
            except AttributeError:
                pass

        self._mapping_type = kwargs.get('mapping_type', self.DEFAULT_MAPPING_TYPE)

    def _construct_mapping(self, loader, node):
        """Construct a mapping instance by making a :class:`Thing`."""

        loader.flatten_mapping(node)
        return self._mapping_type(loader.construct_pairs(node))

    def _include(self, loader, node):
        oldRoot = self.root
        filename = os.path.join(self.root, loader.construct_scalar(node))
        self.root = os.path.dirname(filename)
        data = yaml_load_path(filename)
        self.root = oldRoot
        return data


def yaml_load(stream):
    """Parse YAML from a stream or string, and return the object."""

    if isinstance(stream, str):
            stream = io.StringIO(stream)

    return yaml.load(stream, IncludeLoader)


def yaml_load_path(path):
    """Load YAML from a path: if a file, read that, if a directory, read all the files."""

    s = os.stat(path)

    if stat.S_ISREG(s.st_mode):
        with open(path) as f:
            return yaml_load(f)

    if not stat.S_ISDIR(s.st_mode):
        raise YamlCantLoad(path=path)

    return list(yaml_load_path(os.path.join(path, part)) for part in os.listdir(path))


def _thing_to_yaml(rep, thing):
    """Represent :class:`Thing` as a plain dict, and avoid sorting the keys."""

    # https://stackoverflow.com/questions/16782112/can-pyyaml-dump-dict-items-in-non-alphabetical-order

    value = []

    for item_key, item_value in thing.items():
        node_key = rep.represent_data(item_key)
        node_value = rep.represent_data(item_value)

        value.append((node_key, node_value))

    return yaml.nodes.MappingNode(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, value)


yaml.add_representer(Thing, _thing_to_yaml)


def yaml_dump(obj, stream=None):
    """Dump an object as YAML to a stream sink."""

    return yaml.dump(obj, stream or sys.stdout, default_flow_style=False)

rjgtoys.yaml: Reading and writing YAML
================================================================================

This is a thin layer on top of ruamel.yaml_ that does YAML I/O with some tricks
that I find useful:

1. It dumps structures with the layout that I like;
2. It preserves order of keys in mappings when dumping them;
3. Mappings are returned as objects that allow both attribute- and item-access;
4. Multiple files can be loaded from a directory, in a single call;
5. YAML source files can reference others, and merge them automatically, using
   an `!include` tag.


.. _ruamel.yaml: https://yaml.readthedocs.io/en/latest/



.. toctree::
   :maxdepth: 2

   tutorial
   reference
   getting
   todo




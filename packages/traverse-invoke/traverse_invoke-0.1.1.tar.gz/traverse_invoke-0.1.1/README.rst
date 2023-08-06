===============
Traverse invoke
===============


.. image:: https://img.shields.io/pypi/v/traverse_invoke.svg
        :target: https://pypi.python.org/pypi/traverse_invoke

.. image:: https://img.shields.io/travis/DaniloZZZ/traverse_invoke.svg
        :target: https://travis-ci.org/DaniloZZZ/traverse_invoke

.. image:: https://readthedocs.org/projects/traverse-invoke/badge/?version=latest
        :target: https://traverse-invoke.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


A nested method [computation model] for nested data

This shit is a blessing. I don't know anything like this except maybe lambda. 
I'll think about Turing-completeness and meta complexity of this.

Please do yourself a favor and read the source. 

Docs not yet available, since the whole computation model needs to be formed, 
which requires some experience of using current version.


* Documentation: https://traverse-invoke.readthedocs.io   (uder development. maybe).


Features
--------

* Invoke methods by their path in module tree.
* Pass arguments as nested closures for methods.
* Modify invocation path in runtime (the most exiting thing).


Basic Usage
===========

**Invoke method**

.. code-block:: python

   import sys, traverse_invoke

   method = 'sys.version'
   names = {
   'sys':{'version':sys.version}}
   }
   args = { 'version':'foobar'}

   traverse_invoke.entry_traverse(args, method, names)

This will invoke ``sys.version(**{version:foobar})``

**Traverse**

see test

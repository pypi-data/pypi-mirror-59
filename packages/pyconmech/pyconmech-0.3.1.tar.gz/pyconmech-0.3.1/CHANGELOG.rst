
=========
Changelog
=========

.. # with overline, for parts
.. * with overline, for chapters
.. =, for sections
.. -, for subsections
.. ^, for subsubsections
.. ", for paragraphs

TODO
----
- Even when applying the lumped nodal loads in Karamba, the results still look different to the ones from conmech. See `developer_notes/karamba_comparision` for more details.

0.3.1
----------

Added
^^^^^^^

- Added unit tests for `std::throw` in parsing material properties

0.3.0
----------

Changed
^^^^^^^

- Changed `try/catch` in the C++ file parsing to `std::throw` 

0.2.0
-----

Changed
^^^^^^^

- The original ``stiffness_checker`` extension module is wrapper as ``_stiffness_checker``.
  All the cpp modules are wrapper under a top-level python classes/functions, to give more
  flexibility.
- **API change**: ``stiffness_checker`` class is renamed to ``StiffnessChecker`` to conform
    to the class naming convention. All other APIs within this class are left unchanged.
- Delete ``radius`` entry from ``material_properties``.


Added
^^^^^

- documentation is hosted on readthedocs!
- add grasshopper examples - parse/save files, karamba comparsion, solve/get result in GH via ghpython-remote
- supports material / cross sectional properties for each element. 
- supports uniformly distributed load
- add gravity magnitude and direction

0.1.0
-----

Initial version

.. |travis| image:: https://travis-ci.com/gjeusel/ticts.svg?branch=master
  :target: https://travis-ci.com/gjeusel/ticts
.. |readthedocs| image:: https://readthedocs.org/projects/ticts/badge/?version=latest
  :target: http://ticts.readthedocs.io/en/latest/?badge=latest
  :alt: Documentation Status
.. |codecov| image:: https://codecov.io/gh/gjeusel/ticts/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/gjeusel/ticts
.. |pypi| image:: https://badge.fury.io/py/ticts.svg
  :target: https://pypi.python.org/pypi/ticts/
  :alt: Pypi package
.. |python| image:: https://img.shields.io/badge/python-3.6%2B-blue.svg
  :target: https://www.python.org/downloads/release/python-360/
  :alt: Python version 3.5+

.. |logo| image:: docs/_static/img/logo.svg
   :target: https://github.com/gjeusel/ticts
   :width: 50px
   :height: 20px

.. |example| image:: docs/_static/img/example.png

============
ticts |logo|
============
|codecov| |travis| |python| |pypi| |readthedocs|


A Python library for unevenly-spaced time series analysis.
Greatly inspired by `traces <https://github.com/datascopeanalytics/traces>`_.

|example|

Get Started `Notebook <https://mybinder.org/v2/gh/gjeusel/ticts/master?filepath=docs%2FTutorial.ipynb>`_.

Usage
-----

.. code:: python

   from ticts import TimeSeries
   ts = TimeSeries({
      '2019-01-01': 1,
      '2019-01-01 00:10:00': 2,
      '2019-01-01 00:11:00': 3,
   })

   not_in_index = '2019-01-01 00:05:00'
   assert ts[not_in_index] == 1  # step function, previous value

   ts['2019-01-01 00:04:00'] = 10
   assert ts[not_in_index] == 10

   assert ts + ts == 2 * ts

   ts_evenly_spaced = ts.sample(freq='1Min')

   # From ticts to pandas, and the other way around
   assert ts.equals(
      ts.to_dataframe().to_ticts(),
   )


Installation
------------

.. code:: bash

    pip install ticts


Contributing
------------

.. code:: bash

   pip install pre-commit
   pre-commit install --hook-type pre-push

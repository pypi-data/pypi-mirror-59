.. sqlfaker documentation master file, created by
   sphinx-quickstart on Sun Nov 10 09:58:30 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to sqlfaker's documentation!
====================================

.. image:: /badges/total.svg
   :alt: Total number of tests executed
   :align: left

.. image:: /badges/failures.svg
   :alt: Total number of tests executed
   :align: left

.. image:: /badges/errors.svg
   :alt: Total number of tests executed
   :align: left

sqlfaker is a python package that lets you define relational datastructurs and
export them to DDL afterwards. In order to be even more useful, the package
comes with a data generation engine that lets you also create fake data for 
your data structure. To do so, sqlfaker uses python's ``faker`` library. Using
this tool, you can automatically create fake names, addresses and other data 
and directly put them into your data structure. sqlfaker allows to also
generate DML scripts that can be used to export the fake data to your database.

.. toctree::
   :maxdepth: 4
   :caption: Contents:


Indices and tables
==================

* :ref:`genindex`
* :ref:`search`


Package Classes
================

Below, you can find a description of the classes that are part of this
package. You can also use the Module Index to navigate through these objects.

Database Class
----------------

This class lets you create a database object that is capable of holding
multiple tables.

.. autoclass:: sqlfaker.database.Database
    :members:


Table Class
----------------

This class lets you create a table object that is capable of holding
multiple columns.

.. autoclass:: sqlfaker.table.Table
    :members:


Column Class
----------------

This class lets you create multiple columns.

.. autoclass:: sqlfaker.column.Column
    :members:

PrimaryKey Class
----------------

This class lets you create a **primary key** object that is acting as a key
column of any table. This class inherits from Column.

.. autoclass:: sqlfaker.primary_key.PrimaryKey
    :members:


ForeignKey Class
----------------

This class lets you create a **foreign key** object that is referencing a key
column of another table. This class inherits from Column.

.. autoclass:: sqlfaker.foreign_key.ForeignKey
    :members:

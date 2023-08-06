# Sequelize to Excel

Why Should I Use This?
----------------------
This library is intended to extract column names , field names , table name and other information from your node model file developed in standard Sequelize format

The excel will help you to have sneak peak of complete file at once , along with the corresponding database field name

This can also be used as standalone app , as well as library

Installation
------------

.. code-block:: console

    pip install sequelize-to-excel


Using SequelizeToExcel
----------------------

1. Import the package and call the method from initalize object

.. code-block:: console

    from sequelize_to_excel import SequelizeToExcel
    objSeq = SequelizeToExcel("<filename>")
    objSeq.extract_and_export()

2. you will find the generate excel file in the same folder .
    Make sure you provide the input file preferrably in the same folder.


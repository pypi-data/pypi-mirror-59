mds-import-product
==================
Tryton module to import products from csv-file.

Install
=======

pip install mds-import-product

Requires
========
- Tryton 5.2

HowTo
=====

Use the action button on the Products list to start the 
'Import CSV-file' wizard. The assignment of the columns in the 
file to the fields of the products takes place in the 
second step. Use product attributes to add more columns to the product.

Changes
=======

*21.01.2020 - ver 5.2.2*

- number of fields now 30
- run on_change_fieldname-events

*10.01.2020 - ver 5.2.1*

- added translations

*09.01.2020*

- first public

Jirafs csv_table Macro
======================

Adds a macro used for including a CSV file as a Jira table::

  <jirafs:csv-table src="my_file.csv" />

if you have a file named `my_file.csv` containing the content::

  ,Canada,United States of America,Mexico, Guatemala
  Capital,"Ottawa, Ontario","Washington, DC","Mexico City, DF","Guatemala City"
  Population (millions),35.16,318.9,122.3,15.47

will be automatically transformed into JIRA's special markup::

  || ||Canada||United States of America||Mexico||Guatemala||
  |Capital|Ottawa, Ontario|Washington, DC|Mexico City, DF|Guatemala City|
  |Population (millions)|35.16|318.9|122.3|15.47|

which, when rendered by JIRA, will look something like this:

+------------+-----------------+--------------------------+-----------------+----------------+
|            | Canada          | United States of America | Mexico          | Guatemala      |
+============+=================+==========================+=================+================+
| Capital    | Ottawa, Ontario | Washington, DC           | Mexico City, DF | Guatemala City |
+------------+-----------------+--------------------------+-----------------+----------------+
| Population | 35.16           | 318.9                    | 122.3           | 15.47          |
| (millions) |                 |                          |                 |                |
+------------+-----------------+--------------------------+-----------------+----------------+

Parameters
----------

* `src`: Path to CSV file to include as a table.
* `delimiter`: (Default: ",") Delimiter used for separating each column's
  values.  You can use standard python string escape sequences; so for using
  a tab as your file's field delimiter, you can provide the value of "\t".
* `has_header`: (Default: True) If the first row of your CSV is not headers

Requirements
------------

This version requires a Jirafs version of at least 2.0.0.

Installation
------------

1. Install from PIP::

    pip install jirafs_csv_table

2. Enable for a ticket folder::

    jirafs plugins --enable=csv_table

Note that you can globally enable this (or any) plugin by adding the
``--global`` flag to the above command::

    jirafs plugins --global --enable=csv_table


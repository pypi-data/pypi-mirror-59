# The Cloudframe Data Scientist Simple Enabler

At Cloudframe we employ teams of Data Scientists, Data Engineers, and Software Developers.  Check us out at [http://cloudframe.io](http://cloudframe.io "Cloudframe website")

If you're interested in joining our team as a Data Scientist see here: [Bid Prediction Repo](https://github.com/cloudframe/texas-bid-prediction).  There you'll find a fun problem and more info about our evergreen positions for Data Scientists, Data Engineers, and Software Developers.

This package contains some convenience functions meant help a Data Scientist get data into a format that is useful for training models.  It is a light version of some of our proprietary enablers that we use to deliver data-informed products to our clients.

## Installation

`pip install datascientist`

## Dependencies

In addition to the following packages, `datascientist` requires that you have the credentials (et cetera) to perform the operation required.  For example, when connecting to an Oracle database you must install and configure [Instant Client](https://docs.oracle.com/en/database/oracle/r-enterprise/1.5.1/oread/installing-oracle-database-instant-client.html "Oracle Instant Client Instructions") or something like that.  This package does not do that for you.  

* `pandas`
* `numpy`
* `psycopg2`
* `mysql.connector`
* `cx_Oracle`

## Structure

```
data-scientist/
|
|-- connections/
|   |-- __init__.py
|   |-- connection_convenience.py
|   |-- rsconnect.py
|
|-- workflow/
|   |-- __init__.py
|   |-- tracker.py
|
|-- Manifest.in
|-- README.md
|-- setup.py
|-- bash_profile_example
```

## Usage

### `connections.connection_convenience`

A sample bash profile is provided for reference with values removed.  Some of the functions will look for environment variables named according the conventions there.  If it can't find them it will prompt you for the appropriate strings.  Strings set via prompts are NOT saved for security reasons.  It's up to you to make sure that if you set environment variables in a more permanent way that they remain secure.

This module replicates the functionality of `pandas.read_sql()`, but is a little friendlier; handling the connection object for you while performing the same according to %timeit.

```
import connections.connection_convenience as cc

sql = '''
select * from my_table
where my_field in ('cloud', 'frame');
'''

df = cc.pg2df(sql)

# input at the prompts if necessary
```

### `connections.rsconnect`

This is a special case of `connection_convenience` for Redshift with a bunch more functionality.  In addition to merely establishing connections and fetching data, this sub-module can perform do things like:

* Infer the schema of your DataFrame
* CREATE and DROP tables
* WRITE data to a table 
* Perform an UPSERT operation
* Get the names of tables in your cluster
* Et cetera

For example, upsert data or write a new table:

```
import connections.rsconnect as rs

tname = 'my_table'

fields = rs.infer_schema(df)
bucket, key = rs.df_to_s3(df, 
                          bucket = 'my-bucket', 
                          key = 'location/on/s3/my-file.csv',
                          primary = 'my_primary_key')

if rs.table_check(tname):
    _ = rs.upsert_table(tname, 
                        fields, 
                        bucket = bucket,
                        key = key,
                        primary = 'my_primary_key')

else:
    _ = rs.create_table(tname, 
                        fields,
                        primary = 'my_primary_key')
    _ = rs.write_data(tname,
                      bucket,
                      key)
```

Note also that the function to fetch data is: `rs.sql_to_df()`.

### `workflow.tracker`

The `workflow.tracker` provides a lightweight tool for tracking a data science workflow.  It is intended to help data scientists produce human-readable artifacts and obviate the need for things like complex naming conventions to keep track of the state of modeling experiments.  It also has features to enable reproducibility, iterative improvment, and model deployent in a cloud environment (AWS right now).

The fundamental object of this library is the `Project` class.  A Project is conceptually is a single effort to build a Machine Learning function to address a particular problem.  Individual experiments are conceptualized as 'runs'.  A Run covers the data science workflow from data conditioning (post ETL and feature generation) through model validation and testing.  

For more information and to learn how to use the Workflow Tracker, see the sample notebooks in the ['cloud-event-modeling'](https://github.com/cloudframe/cloud-event-modeling/) repository.  
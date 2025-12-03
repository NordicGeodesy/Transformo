# About DataSources

A DataSource is a collection of coordinate data for one or more points of interest.
Often that would a geodetic station but can be any object with a known coordinate.
In the following the term "station" will be used troughout to refer to a point of
interest in a DataSource.

A DataSource requires several data points for each station in a DataSource. They
are

1. Station name
2. Coordinate tuple (x,y,z)
3. Uncertainty estimate of the coordinate (standard deviation)
4. Timestamp

Optionally, a weight can be given to reflect the importance of a given station
when deriving coordinat transformation parameters.

All DataSource components can be used as both source and target data. DataSource
components can pull data from a number of different sources, for instances simple
files or a selection from a connected database. The specifics are detailed for each
available DataSource.

In a Transformo configuration file a DataSource's are configured as follows:

```yaml
...
source_data:
- name: ITRF2014 data for Danish GNSS stations
  type: csv
  filename: test/data/dk_cors_itrf2014.csv

target_data:
- type: csv
  filename: test/data/dk_cors_etrs89.csv
...
```

Here CSV DataSource component is used, other DataSources can be used as well.
In this the source DataSources are given a name whereas the target DataSource
is left unnamed. Naming components is not required but it can make it easier
to make sense of the output from Transformo, particularly if many different
DataSources are in use.

## Data overrides

Data in a DataSource can be overridden in two ways:

1. for the entire datasource
2. on a station basis

The following fields can be changed for entirety of a data source:

  t, sx, sy, sz, w

This gives the opportunity to change weighting of coordinates across
the whole data source, as well as adjust the epoch in case it is not
registered correctly in the original source data.

Similarly, coordinate data can be adjusted at a station level. Here
all aspects of a coordinate can be changed. The available fields are:

  station, t, x, y, z, sx, sy, sz, w

This is useful in case the source data has errors in it or if it would
be helpful to weigth a particular station differently that the rest.

Below is an example of both overriding data across a DataSource and
specific changes at the station level.

```yaml
- name: ITRF2014
  type: csv
  filename: test/data/dk_cors_itrf2014.csv

  # changes across the whole data source
  sx: 0.02
  sy: 0.02
  sz: 0.04
  w: 0.8
  t: 2019.32

  # changes to data from specific stations
  overrides:
    BUDP:
      sz: 0.03
      w: 1.0
      t: 2099.0
    HIRS:
      station: XXXX
```

In this example the entire DataSource is weighted down by a factor of
0.8 and the uncertainties are set to 0.02 m for the horisontal parts
and 0.04 m for the vertical. The epoch of all coordinates are set to
2019.32.
On the station level the coordinate for the BUDP station is weighted
higher, the vertical uncertainty set to 0.03 m and the epoch changed
to a time far in the future. The HIRS station is renamed. This can be
useful in case two DataSources contain stations with the same names,
which will cause problems when merging the data.

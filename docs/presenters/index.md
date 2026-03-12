# Presenters

Presenters are Transformo components that provide information about the
configured transformation. A Presenter can return a wide variety of results,
for instance residual statitics of a derived transformation model, a
description of a derived transformation given in a standardised format
or insights into the data used to create a transformation model.

The output of all the Presenters used in a Transformo configuration are
collected in the final report, wether it is returned as a PDF-file, a
MarkDown-file or printed in the terminal. Some Presenters produce artifacts
such as GeoJSON-files which will be available in the specified location.

In a Transformo configuration Presenters are set up in the `presenters`
section:

```yaml
...
presenters:
- type: proj_presenter
  name: PROJ String
- type: residual_presenter
  name: Coordinate differences
  coordinate_type: cartesian
  geojson_file: residuals.geojson
...
```

See the documentation pages for the individual Presenters to learn about
their configuration options.

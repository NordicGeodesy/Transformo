
# Using Transformo

Transformo is a command line application that expects a YAML-file as input.
The YAML-file defines a pipeline of datasources, operators and presenters.
Once the pipeline has been processed by Transformo the results can be displayed
in the terminal or saved to a file in various formats.

Here's an example:

```sh
transformo pipeline.yaml --pdf pipeline.yaml
```

which will produce a PDF-file with the results of the processed pipeline.

The file `pipeline.yaml` might look something like:

```yaml
source_data:
- name: ITRF2014
  type: csv
  filename: test/data/dk_cors_itrf2014.csv
target_data:
- name: ETRS89
  type: csv
  filename: test/data/dk_cors_etrs89.csv
operators:
- type: helmert_translation
presenters:
- name: PROJ string
  type: proj_presenter
- name: Coordinates
  type: coordinate_presenter
```

Note that some pipeline entries are named and some aren't. The name attribute
is optional but are useful when working with bigger pipelines. For named
presenters the name will used as section headers for the presenter output in the
report.

In the `examples/` directory a number of example pipelines are available, that
can be used as inspiration for creating your own. Run them from the root of the
Transformo repository:

```sh
transformo --report-in-terminal examples/bells_and_whistles.yaml
```

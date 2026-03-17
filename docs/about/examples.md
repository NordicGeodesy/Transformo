# Examples

Transformo is run from a command line and configured using a YAML-file. The YAML-file follows
a specific layout that aligns with the pipeline architecture of Transformo. The file
has four mandatory sections: `source_data`, `target_data`, `operators` and `presenters`. In each
section several elements can be added depending on the use case. Additional optional sections
exists as well for running pre- and post-processing commands before the Transformo pipeline
is executed.

In the following sections aspects of Transformo is demonstrated by examples of pipeline
files and the output they produce when run in a terminal.

## Dummies

The absolute simples Transformo setup up uses dummies that doesn't do anything. They have been
created as devices for testing but can occasitionally be useful. In this example they are useful
for demonstrating the structure of a Transformo configuration file.

=== "`dummy_example.yaml`"

    ```yaml
    --8<-- "./examples/dummy_example.yaml"
    ```

=== "Output"

    ```sh
    $ transformo --report-in-terminal examples/dummy_example.yaml
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃                                Transformo Results                          ┃
    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

    Created with Transformo version 0.2.0, 2026-03-05 11:54:41.323899.


                                    A Dumb Presenter

    This section intentionally left blank.
    ```

!!! note

    More examples to come!

# Operators

Operators represent the core functionality of Transformo. Operators are pipeline
components that compose the transformation model in a given setup.

All operators have the ability to manipulate coordinates, generally in the sense
of a geodetic transformation. In addition operators *can* implement a method to
derive parameters for said coordinate operation. Most operators do, but not all.

So, operators have two principal modes of operation:

    1. Coordinate operations, as defined in the ISO 19111 terminology
    2. Estimating parameters for the coordinate operations

The abilities of a operator are determined by the functionality they implement.
*All* Operator's must implement a forward operation and they *can* implement
functions for estimating parameters and doing the inverse operation. If only
the forward operation is implemented the operator will exist as a coordinate
operation that can't estimate parameters.

In a Transformo configuration Operators are set up in the `operators` section:

```yaml
...
operators:
- name: Offset coordinates
  type: proj_operator
  proj_string: +proj=helmert +x=1000

- name: Estimate offset in x axis
  type: helmert_translation
...
```

The example above demonstrates a multistep pipeline of Operators. The first Operator
performs a transformation of the input data using PROJ and the second Operator
estimates parameters for a 3 parameter Helmert transformation.

See the documentation pages for the individual Operators to learn about their
configuration options.

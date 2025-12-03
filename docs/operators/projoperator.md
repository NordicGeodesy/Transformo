# PROJ Operator

The PROJ operator exposes PROJ transformations directly within Transformo. It allows using any transformation available in the PROJ library.

## Type

`type: proj_operator`

## Options

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `proj_string` | `string` | Yes | - | PROJ pipeline string |

## PROJ String

The `proj_string` parameter accepts any valid PROJ pipeline string. For more information about PROJ strings, see the [PROJ documentation](https://proj.org/).

## Examples Transformations

### Helmert Transformation

```yaml
operators:
- name: Helmert via PROJ
  type: proj_operator
  proj_string: +proj=helmert +x=100 +y=50 +z=25
```

### Coordinate Conversion

```yaml
operators:
- name: UTM
  type: proj_operator
  proj_string: +proj=utm +zone=32
```

### Pipeline Transformations

Multiple transformations can be chained using a pipeline:

```yaml
operators:
- name: Complex transformation
  type: proj_operator
  proj_string: +proj=pipeline +step +proj=helmert +x=1000 +step +proj=utm +zone=32
```

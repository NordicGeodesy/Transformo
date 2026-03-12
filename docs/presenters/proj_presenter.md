# PROJ Presenter

The PROJ Presenter displays transformation parameters as a PROJ string, which can be used directly with the PROJ library for coordinate transformations.

## Type

`type: proj_presenter`

## Options

This presenter has no additional options.

## Output

The presenter generates a PROJ string representation of the transformation. For multi-step pipelines, it creates a PROJ pipeline string.

### Single transformation

```
+proj=helmert +x=0.5 +y=1.2 +z=-0.9 +rx=0.001 +ry=0.002 +rz=0.003 +s=0.005 +convention=coordinate_frame
```

### Multi-step pipeline

```
+proj=pipeline +step +proj=helmert +x=1000 +step +proj=helmert +x=0.5 +y=1.2 +z=-0.9
```

## Example

```yaml
presenters:
- type: proj_presenter
  name: PROJ String
```

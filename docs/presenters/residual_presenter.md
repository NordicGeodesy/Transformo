# Residual Presenter

The Residual Presenter calculates and displays residuals between transformed coordinates and target coordinates in Cartesian space.

## Type

`type: residual_presenter`

## Options

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `coordinate_type` | `string` | Yes | - | Type of coordinates (`cartesian`) |
| `json_file` | `string` | No | - | Path to output residuals as JSON |
| `geojson_file` | `string` | No | - | Path to output residuals as GeoJSON |

## Output

### Station Residuals Table

| Column | Description |
|--------|-------------|
| Station | Station name |
| Rx | Residual in X direction (mm) |
| Ry | Residual in Y direction (mm) |
| Rz | Residual in Z direction (mm) |
| Norm | Total residual vector length (mm) |

### Residual Statistics Table

| Measure | Description |
|---------|-------------|
| avg | Average residual in each direction |
| std | Standard deviation of residuals |

## Coordinate Type

The `coordinate_type` option determines how coordinates are interpreted:

- `cartesian`: Geocentric Cartesian coordinates (ECEF)

## Example

```yaml
presenters:
- type: residual_presenter
  name: Coordinate differences
  coordinate_type: cartesian
```

### With file output

```yaml
presenters:
- type: residual_presenter
  name: Coordinate differences
  coordinate_type: cartesian
  json_file: residuals.json
  geojson_file: residuals.geojson
```

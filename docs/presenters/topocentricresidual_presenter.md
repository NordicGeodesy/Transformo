# Topocentric Residual Presenter

The Topocentric Residual Presenter calculates and displays residuals in a topocentric (local) coordinate system, providing East (E), North (N), and Up (U) components relative to each station.

## Type

`type: topocentricresidual_presenter`

## Options

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `coordinate_type` | `string` | Yes | - | Type of coordinates (`cartesian`, `degrees`, or `projected`) |
| `json_file` | `string` | No | - | Path to output residuals as JSON |
| `geojson_file` | `string` | No | - | Path to output residuals as GeoJSON |

## Coordinate Types

Three coordinate types are supported:

### `cartesian`

Geocentric Cartesian coordinates (ECEF). Coordinates are converted to topocentric space using PROJ's topocentric projection centered on each station.

### `degrees`

Latitude, longitude, height above ellipsoid. Coordinates are first converted to Cartesian, then to topocentric space.

### `projected`

Coordinates in a projected CRS. These are assumed to already be in a local coordinate system and are used directly.

## Output

### Station Residuals Table

| Column | Description |
|--------|-------------|
| Station | Station name |
| East | Residual in East direction (mm) |
| North | Residual in North direction (mm) |
| Up | Residual in Up direction (mm) |
| Planar residual | 2D residual length (E,N) in mm |
| Total residual | 3D residual length in mm |

### Residual Statistics Table

| Measure | Description |
|---------|-------------|
| avg | Average residual in each direction |
| std | Standard deviation of residuals |

## Example

```yaml
presenters:
- type: topocentricresidual_presenter
  name: ENU Residuals
  coordinate_type: cartesian
```

### With degrees coordinates

```yaml
presenters:
- type: topocentricresidual_presenter
  name: ENU Residuals
  coordinate_type: degrees
```

### With file output

```yaml
presenters:
- type: topocentricresidual_presenter
  name: ENU Residuals
  coordinate_type: cartesian
  json_file: residuals.json
  geojson_file: residuals.geojson
```

# Coordinate Presenter

The Coordinate Presenter displays coordinates for all stages of a transformation pipeline, including source data, intermediate results, and target data.

## Type

`type: coordinate_presenter`

## Options

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `json_file` | `string` | No | - | Path to output coordinates as JSON |
| `geojson_file` | `string` | No | - | Path to output coordinates as GeoJSON |

## Output

The presenter generates a markdown table showing coordinates for each station at each stage of the pipeline:

- **Source coordinates**: Original input coordinates
- **Step N**: Coordinates after each transformation step
- **Target coordinates**: Final target coordinates

Each table contains:
- Station name
- x, y, z coordinates
- Timestamp (t)

## Example

```yaml
presenters:
- type: coordinate_presenter
  name: Coordinates
```

### With file output

```yaml
presenters:
- type: coordinate_presenter
  name: Coordinates
  json_file: coordinates.json
  geojson_file: coordinates.geojson
```

# Comma Separated Values

The CSV DataSource reads coordinate data from generic CSV files.

## Type

`type: csv`

## Options

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `filename` | `string` | Yes | - | Path to the CSV file to read |
| `columns` | `list[CsvColumns]` | No | `[station, t, x, y, z, sx, sy, sz, weight]` | Column order mapping |
| `sx` | `float` | No | - | Standard deviation in X direction |
| `sy` | `float` | No | - | Standard deviation in Y direction |
| `sz` | `float` | No | - | Standard deviation in Z direction |
| `w` | `float` | No | - | Weight for all coordinates |
| `t` | `float` | No | - | Timestamp in decimal years |

## Column Types

The following column types are available:

| Column | Description |
|--------|-------------|
| `station` | Station name |
| `t` | Timestamp in decimal years |
| `x` | X coordinate |
| `y` | Y coordinate |
| `z` | Z coordinate |
| `sx` | Standard deviation in X |
| `sy` | Standard deviation in Y |
| `sz` | Standard deviation in Z |
| `weight` | Coordinate weight |
| `skip` | Skip this column |

## Required Columns

The following columns are required in every CSV file:

- `station`
- `x`
- `y`
- `z`

If columns `t`, `sx`, `sy` and `sz` are not available in the CSV-file, values
for them will have to be set using the override functionality.

## CSV Format

- Only commas are accepted as value separators
- The header row is automatically detected and skipped

### Example CSV file

```csv
station,x,y,z,sx,sy,sz,t,weight
BUDP,3456234.12,728455.21,5341234.56,0.01,0.01,0.02,2020.5,1.0
HIRS,3898234.56,234567.89,4901234.12,0.01,0.01,0.02,2020.5,1.0
```

## Custom Column Order

If your CSV file has columns in a different order, use the `columns` option:

```yaml
- name: my_data
  type: csv
  filename: data.csv
  columns: [station, x, y, z, skip, skip, t, weight]
  sx: 0.05
  sy: 0.05
  sz: 0.10
```

This is useful when the CSV file has extra columns that should be ignored.

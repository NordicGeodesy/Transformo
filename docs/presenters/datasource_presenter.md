# DataSource Presenter

The DataSource Presenter displays information about the data sources used in the transformation pipeline, including their configuration and parameters.

## Type

`type: datasource_presenter`

## Options

This presenter has no additional options.

## Output

The presenter generates YAML-formatted output showing:
- Source data configuration
- Target data configuration

Each section displays the full configuration of the data sources including:
- Type
- Filename
- Any overrides or modifications
- Column configurations

## Example

```yaml
presenters:
- type: datasource_presenter
  name: Data sources
```

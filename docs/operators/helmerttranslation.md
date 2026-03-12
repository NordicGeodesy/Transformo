# Helmert Translation

The 3-parameter Helmert transformation is a simple translation in the three principal directions of an earth-centered, earth-fixed coordinate system.

## Type

`type: helmert_translation`

## Options

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `x` | `float` | No | 0.0 | Translation in X direction (meters) |
| `y` | `float` | No | 0.0 | Translation in Y direction (meters) |
| `z` | `float` | No | 0.0 | Translation in Z direction (meters) |

## Example

```yaml
operators:
- name: Apply offset
  type: helmert_translation
  x: 100.0
  y: 50.0
  z: -25.0
```

## Mathematical Background

### Forward Transformation

A coordinate in vector $\mathbf{V}_a$ is transformed into vector $\mathbf{V}_b$ using:

$$
  \mathbf{V}_b = \mathbf{T} + \mathbf{V}_a
$$

Where $\mathbf{T} = (x, y, z)^T$ is the translation vector:

$$
  \mathbf{T} =
  \begin{bmatrix}
    x \\
    y \\
    z
  \end{bmatrix}
$$

### Inverse Transformation

The inverse transformation is:

$$
  \mathbf{V}_a = \mathbf{V}_b - \mathbf{T}
$$

### Parameter Estimation

The translation parameters are estimated as the weighted mean difference between source and target coordinates:

The mean translation vector is computed as:

$$
  \mathbf{T} = \bar{\mathbf{V}}_{target} - \bar{\mathbf{V}}_{source}
$$

Where the weighted means are:

$$
  \bar{\mathbf{V}}_{source} =
  \frac{\sum_{i=1}^{n} w_i \mathbf{V}_{source,i}}
      {\sum_{i=1}^{n} w_i}
  , \quad
  \bar{\mathbf{V}}_{target} =
  \frac{\sum_{i=1}^{n} w_i \mathbf{V}_{target,i}}
      {\sum_{i=1}^{n} w_i}
$$

For each coordinate component $(x, y, z)$:

$$
  \bar{v}_{source} =
  \frac{\sum_{i=1}^{n} w_i v_{source,i}}
      {\sum_{i=1}^{n} w_i}
$$

The weight $w_i$ is taken from the corresponding coordinate's weight in the weight matrix.

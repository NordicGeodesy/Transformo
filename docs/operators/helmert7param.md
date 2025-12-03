# 7-Parameter Helmert Transformation

The 7-parameter Helmert transformation performs a translation in the three principal directions of an earth-centered, earth-fixed coordinate system, as well as rotations around those axes and a scaling of the coordinates.

## Type

`type: helmert_7param_linear`

## Options

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `convention` | `string` | Yes | - | Rotation convention (`position_vector` or `coordinate_frame`) |
| `x` | `float` | No | 0.0 | Translation in X direction (meters) |
| `y` | `float` | No | 0.0 | Translation in Y direction (meters) |
| `z` | `float` | No | 0.0 | Translation in Z direction (meters) |
| `rx` | `float` | No | 0.0 | Rotation about X axis (arc seconds) |
| `ry` | `float` | No | 0.0 | Rotation about Y axis (arc seconds) |
| `rz` | `float` | No | 0.0 | Rotation about Z axis (arc seconds) |
| `s` | `float` | No | 0.0 | Scale factor (ppm) |
| `small_angle_approximation` | `bool` | No | `true` | Use small angle approximation for rotations |

## Example

```yaml
operators:
- name: ITRF to ETRS89
  type: helmert_7param_linear
  convention: coordinate_frame
  small_angle_approximation: true
  x: 0.5
  y: 1.2
  z: -0.9
  rx: 0.001
  ry: 0.002
  rz: 0.003
  s: 0.005
```

## Mathematical Background

### Forward Transformation

A coordinate in vector $\mathbf{V}_a$ is transformed into vector $\mathbf{V}_b$ using:

$$
  \mathbf{V}_b = \mathbf{T} + (1 + s \cdot 10^{-6}) \mathbf{R} \mathbf{V}_a
$$

Where:
- $\mathbf{T} = (x, y, z)^T$ is the translation vector
- $s$ is the scale factor in parts per million (ppm)
- $\mathbf{R}$ is the $3 \times 3$ rotation matrix

#### Rotation Matrix

The rotation angles (rx, ry, rz) are given in arc seconds. Using the small angle approximation:

$$
  \mathbf{R} \approx
  \begin{bmatrix}
    1    & -r_z &  r_y \\
    r_z  & 1     & -r_x \\
  -r_y &  r_x & 1
  \end{bmatrix}
$$

Where $r_x, r_y, r_z$ are the rotation angles in radians.

#### Rotation Convention

**Position Vector Convention**: The rotation is applied to the position vector:

$$
  \mathbf{V}_b = \mathbf{T} + s \cdot \mathbf{R} \mathbf{V}_a
$$

**Coordinate Frame Convention**: The rotation is applied to the coordinate frame (uses transposed rotation matrix):

$$
  \mathbf{V}_b = \mathbf{T} + s \cdot \mathbf{R}^T \mathbf{V}_a
$$

### Inverse Transformation

The inverse transformation is given by:

$$
  \mathbf{V}_a = -\mathbf{T} + \frac{1}{s} \cdot \mathbf{R}^{-1}
  \mathbf{V}_b
$$

Where $\mathbf{R}^{-1} = \mathbf{R}^T$ for proper rotation matrices.

### Parameter Estimation

The seven parameters are estimated using a least squares adjustment. For each observation $i$, the design matrix is constructed as:

For position vector convention:

$$
  \mathbf{R}_i =
  \begin{bmatrix}
    0    & -z_i &  y_i \\
    z_i  & 0     & -x_i \\
  -y_i &  x_i & 0
  \end{bmatrix}
$$

For coordinate frame convention:

$$
  \mathbf{R}_i =
  \begin{bmatrix}
    0    &  z_i & -y_i \\
    -z_i  & 0     &  x_i \\
    y_i & -x_i & 0
  \end{bmatrix}
$$

The design matrix row for observation $i$ is:

$$
  \mathbf{A}_i =
  \begin{bmatrix}
    1 & 0 & 0 &  x_i &   0 &  z_i & -y_i \\
    0 & 1 & 0 &  y_i & -z_i &   0 &  x_i \\
    0 & 0 & 1 &  z_i &  y_i & -x_i &   0
  \end{bmatrix}
$$

The observation equation is:

$$
  \mathbf{y} = \mathbf{A} \mathbf{\beta} + \mathbf{e}
$$

Where $\mathbf{\beta} = [x, y, z, k, \beta_4, \beta_5, \beta_6]^T$ and $k = 1 + s \cdot 10^{-6}$.

The parameters are estimated using weighted least squares:

$$
  \mathbf{\beta} = (\mathbf{A}^T \mathbf{W} \mathbf{A})^{-1} \mathbf{A}^T \mathbf{W} \mathbf{y}
$$

The scale and rotation parameters are then derived:

$$
  s = (k - 1) \cdot 10^6 \quad \text{[ppm]}
$$

$$
  \text{rx} = \frac{\beta_4}{k} \cdot \frac{180^\circ \cdot 3600}{\pi}, \quad
  \text{ry} = \frac{\beta_5}{k} \cdot \frac{180^\circ \cdot 3600}{\pi}, \quad
  \text{rz} = \frac{\beta_6}{k} \cdot \frac{180^\circ \cdot 3600}{\pi}
$$

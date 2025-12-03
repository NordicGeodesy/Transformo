# 7-Parameter Helmert Transformation (Non-Linear)

The 7-parameter Helmert transformation performs a translation in the three principal directions of an earth-centered, earth-fixed coordinate system, as well as rotations around those axes and a scaling of the coordinates.

## Type

`type: helmert_7param_nonlinear`

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
| `small_angle_approximation` | `bool` | No | `true` | Use small angle approximation for rotations (applies to forward/inverse transformations, not parameter estimation) |

## Example

```yaml
operators:
- name: ITRF to ETRS89 (Non-Linear)
  type: helmert_7param_nonlinear
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

## Differences from Helmert7ParamLinear

The `Helmert7ParamNonLinear` operator is similar to `Helmert7ParamLinear` in functionality but differs in the parameter estimation method:

| Aspect | Helmert7ParamLinear | Helmert7ParamNonLinear |
|--------|---------------------|------------------------|
| Estimation method | Closed-form solution using linear least squares | Iterative non-linear least squares (Levenberg-Marquardt) |
| Rotation matrix | Uses small-angle approximation by default | Always uses full rotation matrix |
| Numerical stability | May have issues with large coordinates | Uses coordinate centroid normalization for stability |
| Convergence | Single step solution | Iterative, may require more computation |

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

Or using the full rotation matrix:

$$
  \mathbf{R} = \mathbf{R}_3(r_z) \mathbf{R}_2(r_y) \mathbf{R}_1(r_x)
$$

Where $r_x, r_y, r_z$ are the rotation angles in radians and:

$$
  \mathbf{R}_1(r_x) = \begin{bmatrix} 1 & 0 & 0 \\ 0 & \cos(r_x) & -\sin(r_x) \\ 0 & \sin(r_x) & \cos(r_x) \end{bmatrix}, \quad
$$

$$
  \mathbf{R}_2(r_y) = \begin{bmatrix} \cos(r_y) & 0 & \sin(r_y) \\ 0 & 1 & 0 \\ -\sin(r_y) & 0 & \cos(r_y) \end{bmatrix}, \quad

$$
  \mathbf{R}_3(r_z) = \begin{bmatrix} \cos(r_z) & -\sin(r_z) & 0 \\ \sin(r_z) & \cos(r_z) & 0 \\ 0 & 0 & 1 \end{bmatrix}
$$

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
  \mathbf{V}_a = -\mathbf{T} + \frac{1}{s} \cdot \mathbf{R}^{-1} \mathbf{V}_b
$$

Where $\mathbf{R}^{-1} = \mathbf{R}^T$ for proper rotation matrices.

### Parameter Estimation

The 7-parameter Helmert transformation relates source coordinates $\mathbf{S}$ to target coordinates $\mathbf{T}$ through:

$$
  \mathbf{T} = \mathbf{T}_{translation} + (1 + s \cdot 10^{-6}) \cdot \mathbf{R} \cdot \mathbf{S}
$$

The estimation is done using the **full rotation matrix** (not the small-angle approximation), making this a **non-linear** problem solved iteratively using the Levenberg-Marquardt algorithm.

#### Methodology

1. **Coordinate Normalization**: To improve numerical stability, coordinates are centered around their weighted centroids:

- $\bar{x} = \sum(w_i \cdot x_i) / \sum(w_i)$
- Normalized coordinates: $X = S - \bar{x}$, $Y = T - \bar{y}$

2. **Non-linear Least Squares**: The transformation model in normalized coordinates:

$$
  \mathbf{Y} = \mathbf{t} + k \cdot \mathbf{X} \cdot \mathbf{R}^T + \varepsilon
$$

Where $k = 1 + s \cdot 10^{-6}$ and $\beta = [T_x, T_y, T_z, k, r_x, r_y, r_z]^T$ is the parameter vector.

3. **Iterative Solution**: The minimization problem $\min ||r(\beta)||^2$ is solved using Levenberg-Marquardt ([`scipy.optimize.least_squares`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.least_squares.html) with `method='lm'`).

4. **Coordinate System Transformation**: After convergence, translation parameters are transformed back to the original coordinate system:

$$
  \mathbf{T}_{orig} = \mathbf{t} - k \cdot \mathbf{R} \cdot \bar{x} + \bar{y}
$$

#### References

- [Sjöberg, L.E. (2013)](https://doi.org/10.2478/jogs-2013-0002). Closed-form and iterative weighted least squares solutions of Helmert transformation parameters. Journal of Geodetic Science, 3(1), 7-11.
- [Arun, K.S., Huang, T.S., & Blostein, S.D. (1987)](https://doi.org/10.1109/TPAMI.1987.4767965). Least-Squares Fitting of Two 3-D Point Sets. IEEE Transactions on Pattern Analysis and Machine Intelligence, PAMI-9(5), 698-700.

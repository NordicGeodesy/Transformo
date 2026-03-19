# 7-Parameter Helmert Transformation

The 7-parameter Helmert transformation performs a translation in the three principal directions of an earth-centered, earth-fixed coordinate system, as well as rotations around those axes and a scaling of the coordinates.

## Type

`type: helmert_7param`

## Parameter Estimation

This operator uses **non-linear least squares estimation** with the **full rotation matrix** (no small-angle approximation). The rotation matrix is composed of elementary rotations about the x, y, and z axes, resulting in an inherently non-linear problem that is solved iteratively using the Levenberg-Marquardt algorithm.

This method is suitable for transformations involving large rotations where the small-angle approximation is not valid. For small rotations, `Helmert7ParamSmallAngle` provides a faster closed-form solution.

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

## Example

```yaml
operators:
- name: ITRF to ETRS89 (Full Rotation)
  type: helmert_7param
  convention: coordinate_frame
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

The rotation matrix is given as

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

$$
  \mathbf{R}_3(r_z) = \begin{bmatrix} \cos(r_z) & -\sin(r_z) & 0 \\ \sin(r_z) & \cos(r_z) & 0 \\ 0 & 0 & 1 \end{bmatrix}
$$

#### Rotation Convention

Two conventions exists for the rotation matrix: Position Vector and
Coordinate Frame. The above formulation is using the Position Vector
convention. Transposing the rotation matrix $\mathbf{R}$ changes the convention:

$$
  \mathbf{R}_{position vector} = \mathbf{R}_{coordinate frame}^T
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

    * $\bar{x} = \sum(w_i \cdot x_i) / \sum(w_i)$
    * Normalized coordinates: $X = S - \bar{x}$, $Y = T - \bar{y}$

2. **Non-linear Least Squares**: The transformation model in normalized coordinates:

    <center>
    $\mathbf{Y} = \mathbf{t} + k \cdot \mathbf{X} \cdot \mathbf{R}^T + \varepsilon$
    </center>

    Where $k = 1 + s \cdot 10^{-6}$ and $\beta = [T_x, T_y, T_z, k, r_x, r_y, r_z]^T$
    is the parameter vector.

3. **Iterative Solution**: The minimization problem $\min ||r(\beta)||^2$ is solved
 using Levenberg-Marquardt ([`scipy.optimize.least_squares`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.least_squares.html) with `method='lm'`).

4. **Coordinate System Transformation**: After convergence, translation parameters are transformed back to the original coordinate system:

$$
  \mathbf{T}_{orig} = \mathbf{t} - k \cdot \mathbf{R} \cdot \bar{x} + \bar{y}
$$

#### References

- [Sjöberg, L.E. (2013)](https://doi.org/10.2478/jogs-2013-0002). Closed-form and iterative weighted least squares solutions of Helmert transformation parameters. Journal of Geodetic Science, 3(1), 7-11.
- [Arun, K.S., Huang, T.S., & Blostein, S.D. (1987)](https://doi.org/10.1109/TPAMI.1987.4767965). Least-Squares Fitting of Two 3-D Point Sets. IEEE Transactions on Pattern Analysis and Machine Intelligence, PAMI-9(5), 698-700.

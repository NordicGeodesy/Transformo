# Transformo
Transformo is a generalized software package for estimating geodetic transformation
parameters and models.

Transformo seeks to provide a framework that lets the user focus on determining the
best transformation model. To achieve that, the burden of reading coordinate data
from various sources, (re)implementing algorimths and delivering the results in
a useful an accessable form has been removed.

## Rationale
The rationale behind Transformo is to create a framework that removes the tedious
work of reading input data and presenting the results after transformation
parameters has been determined. In particular, this approch is meant to be a service
to researchers that develop new for methods geodetic coordinate transformations, as
they can focus on the core algorithms and not the supporting scaffolding.

## Problem
The main problem Transformo tries to solve can be presented on the idealized form

$$
y = f(\beta, x)
$$

Where $x$ and $y$ are the source and target coordinates, $f$ is a transformation
model and $\beta$ is the parameters for the chosen model.

The real world is rarely simple so a more realistic form would be

$$
y = f(\beta, x) + r
$$

Where $r$ is the transformation residuals.

The primary function of Transformo is to provide a set of parameters $\beta$ that
minimizesthe residual $r$. In some cases that might involve a transformation model
consisting of several steps:

$$
y = f_3(\beta_3, f_2(\beta_2, f_1(\beta_1, x))) + r
$$

With transformo we can easily specify the $x$, $y$ and $f_1$, $f_2$, and $f_3$ using
the built-in constructs, which leaves only the parameters, $\beta_1$, $\beta_2$ and
$\beta_3$, to be determined. Transformo will do that based on the specified model and
present the results in a suitable format.

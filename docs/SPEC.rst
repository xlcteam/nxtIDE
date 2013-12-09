
The config file format
======================

The config file follows the YAML structure. It has got suffix `erc` which
stands for *e*\ mulated *r*\ obot *c*\ config.

In it's current version it has the following keys:

  - inputs
  - others

inputs
------

This field specifies inputs of the robot. There are four of them. Each
input is defined by a `slot` and a `type`.

- **slot**: a place on the robot where the sensor connected to this input
  is attached. The value of slot can be in range of [1, 2, 3, 4]

- **type**: the type of the input. Its value can be one of the following:
  [light, touch, us, compass]


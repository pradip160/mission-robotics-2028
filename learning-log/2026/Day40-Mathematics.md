Day Notes — Vector Projection for Robotics

What I Learned

- Calculated displacement using:
  [
  d=B-A
  ]
- Found distance with vector magnitude:
  [
  |d|
  ]
- Converted a direction vector into a unit vector:
  [
  \hat d=\frac{d}{|d|}
  ]
- Used scalar projection to measure how much robot velocity contributes toward the desired direction:
  [
  v\cdot\hat d
  ]
- Found the useful along-path velocity:
  [
  v_{\parallel}=(v\cdot\hat d)\hat d
  ]
- Found sideways/off-path velocity:
  [
  v_{\perp}=v-v_{\parallel}
  ]

Robotics Understanding

I connected the mathematics with robot navigation: sensor/world positions can be converted into vectors, and projection can separate the robot's actual velocity into useful movement toward the goal and sideways movement.

Next

Apply these concepts in simulation when I have access to my laptop.
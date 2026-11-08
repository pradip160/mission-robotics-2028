# Mission World 2028 — Day 77 Learning Log

**Date:** Sunday, 8 November 2026  
**Project:** ROS 2 Restaurant Delivery Robot — Gazebo simulation  
**Focus:** LiDAR experiments, sensor limitations, and realistic restaurant world construction  
**Environment:** Ubuntu 24.04, ROS 2 Jazzy, Gazebo  
**Status:** LiDAR range / sampling / horizontal coverage / vertical blind-spot experiments completed; restaurant exterior enclosure and initial kitchen boundaries built  
**Previous logged session:** Day 76 — LiDAR Physics and Geometry (3 November 2026)  
**Study hours:** Not recorded; no duration claimed

## 1. Today's Objectives

I continued building my restaurant delivery robot as a practical embodied-robotics research project. I wanted to understand the actual behaviour of a simulated LiDAR, improve its coverage, and start designing an environment where mapping, localisation, sensor fusion, navigation, uncertainty handling and recovery can be tested later.

I made a deliberate decision to build a **realistic, single-floor restaurant with an open kitchen** first. Multi-floor maps and lift navigation will be later extensions. Rather than paste a complete ready-made environment, I am implementing the restaurant structures in SDF myself, checking their positions and geometry in Gazebo.

## 2. LiDAR Measurement Interpretation

I inspected Gazebo's laser-scan messages (`gz topic -e -t /lidar`) and distinguished:

- **Range:** Distance along a measurement direction to a surface, when a valid return exists.
- **Intensity:** Reported return-strength information, although the simulated GPU LiDAR does not necessarily model physically realistic optical reflectivity.
- **`inf` / `nan` range values:** No finite valid range for that direction; these must not automatically be treated as proof that the path is safe.
- **`nan` intensity values:** Invalid / undefined numeric intensity. I observed `nan` intensities corresponding to invalid range readings. Finite ranges could still have zero intensity.

### Distance validation

The test box was 0.5 m long in X and the LiDAR was mounted 0.25 m ahead of the robot origin. With the box centred at X = 2.0 m, its nearest face was at X = 1.75 m, giving an expected forward sensor range of 1.50 m.

| Box centre X | Expected nearest range | Minimum observed range |
|---|---:|---:|
| 2.0 m | 1.50 m | 1.5000917 m |
| 3.0 m | 2.50 m | 2.5001528 m |

Observed change:

$$
\Delta r \approx 2.5001528 - 1.5000917 = 1.0000611\ \mathrm{m}.
$$

The measurement changed by approximately 1 m when the box moved 1 m. This validates the **simulation geometry and response** under this controlled test; it does not establish real-world LiDAR accuracy.

## 3. Angular Sampling Experiment

Starting from a 180-degree scan with 181 samples (approximately 1-degree increments), I increased the samples to 361 while keeping the field of view fixed (approximately 0.5-degree increments).

| Box centre | 181 samples / 1° | 361 samples / 0.5° |
|---|---:|---:|
| 2.0 m | 37 finite readings | 73 finite readings |
| 3.0 m | 23 finite readings | 45 finite readings |

I initially predicted `37 × 2 = 74` at the closer distance. I corrected this by recognising that 37 inclusive directions have 36 gaps; inserting one new direction between each old pair yields **37 + 36 = 73**.

The ranges form a nearly symmetric pattern: the central ray has the shortest path to the flat box face, while angled rays travel farther. For an ideal face perpendicular to the forward axis, the geometric relationship is:

$$
r(\theta) = \frac{d}{\cos \theta}.
$$

**Conclusion:** Denser angular sampling increases the number of beams hitting an obstacle; it does not automatically increase maximum range or guarantee detection of every small obstacle.

## 4. Expanded Horizontal Coverage: 180° to 360°

I changed the simulated `gpu_lidar` from approximately 180° to 360° while retaining approximately 0.5° spacing, an 8 m configured maximum range, and 10 Hz update rate. The intended full-scan configuration uses **721 horizontal samples**, with angles approximately from `-pi` to `+pi` radians.

I tested the same obstacle in front of and behind the robot:

| Test | Minimum observed range | Observation |
|---|---:|---|
| Box centred 2 m ahead | 1.500023 m | Forward obstacle detected |
| Box centred 2 m behind | 2.000031 m | Rear obstacle detected |

The rear scan included **58 finite readings split across the beginning and end** of the array, consistent with an obstacle near the ±180° angular wraparound. This is important for later obstacle segmentation: a single rear object must not be mistaken for two objects just because its readings cross the array boundary.

The front/rear range difference is consistent with the LiDAR being mounted **0.25 m forward of the robot origin**. The observations support successful rear coverage in the tested direction, not proof of completely obstruction-free 360° visibility in every condition.

## 5. Vertical Blind-Spot Experiment and Debugging

I tested a tall obstacle and a short obstacle to investigate the limitation of a **single-plane 2D LiDAR**.

- **Experiment A:** 0.60 m tall box, centred at `(2.0, 0, 0.30)` so that it rests on the floor. The LiDAR detected it at about 1.50 m.
- **Experiment B:** 0.10 m tall box, centred at `(2.0, 0, 0.05)`. At first, the scan still detected an obstacle at the same distance.

### Debugging finding

My original world model contained a mismatch:

```xml
<collision name='obstacle_collision'>
  <geometry><box><size>0.5 1.0 0.1</size></box></geometry>
</collision>
<visual name='obstacle_visual'>
  <geometry><box><size>0.5 1.0 0.8</size></box></geometry>
</visual>
```

The collision box was 10 cm tall but the rendered visual box was still 80 cm tall. This is especially relevant for Gazebo's rendering-based `gpu_lidar`. After making **both visual and collision heights 0.1 m**, and using the correct centre height, the scan continued publishing but showed **no finite range returns from the tested obstacle**.

**Experimental conclusion:** The 60 cm obstacle intersected the observed scanning plane; the 10 cm ground-level obstacle did not. A 360° horizontal scan does not remove vertical blind spots. Also, the simulated sensor and physics engine may respond to different geometry when visual and collision sizes disagree.

**Caution:** The precise sensor height above the world floor and all potential self-occlusions were not independently measured. The experiment demonstrates the observed blind spot in this configuration.

## 6. Restaurant Layout Decision

I chose a **24 m × 18 m single-floor restaurant** as our primary Gazebo research environment, with a ground plane enlarged to **30 m × 24 m**. The design will eventually include:

- A northwestern **7 m × 6 m open kitchen**.
- Dedicated robot food pickup and clear routes through the dining room.
- Multiple dining tables/chairs and a bar.
- Customer toilets, staff facilities and storage.
- A porter / pot-wash area with a **separate dirty-dish return route** to avoid crossing the clean-food pickup path.
- Exterior walls, entrances, interior partitions, realistic furniture and later dynamic obstacles.

I explicitly decided **not to copy a complete generated world**. I am writing the SDF components, understanding their geometry and testing them incrementally.

## 7. Exterior Walls Implemented in Gazebo

Using model-centre coordinates, I constructed the exterior enclosure around the nominal footprint `x ∈ [-12,12]`, `y ∈ [-9,9]`.

| Segment | Centre `(x,y,z)` m | Size `(x,y,z)` m |
|---|---|---|
| South left | `(-6.6,-8.9,1.4)` | `(10.8,0.2,2.8)` |
| South right | `(6.6,-8.9,1.4)` | `(10.8,0.2,2.8)` |
| West | `(-11.9,0,1.4)` | `(0.2,17.6,2.8)` |
| East | `(11.9,0,1.4)` | `(0.2,17.6,2.8)` |
| North left | `(-9.3,8.9,1.4)` | `(5.4,0.2,2.8)` |
| North right | `(3.3,8.9,1.4)` | `(17.4,0.2,2.8)` |

The six segments form four exterior sides while leaving planned entrance gaps: **2.4 m for the southern customer entrance** and **1.2 m for the northern service entrance**. Door lintels and actual doors were discussed but not confirmed as built.

I independently implemented the south-right wall and submitted the code for review. One error was found and corrected in the left wall: the visual height was `2.9` m while collision height was `2.8` m.

A Gazebo screenshot confirmed that the exterior enclosure appeared visually. **Collision and robot traversal tests are still pending.**

## 8. Materials, Lighting and SDF Debugging

I added visual materials and scene lighting. I encountered an SDF warning because I accidentally wrote `<sence>` instead of `<scene>`; correcting the XML element resolved the warning.

A diagnostic test changed a wall to bright red, which appeared correctly in Gazebo and demonstrated that the updated material was being loaded. I then chose to **keep a dark walnut colour for the floor** for now. The appearance under Gazebo's lighting and grid can differ from the raw RGB values.

The key lesson is to isolate one variable when debugging: a deliberately obvious colour helps distinguish a material-loading problem from a subtle lighting or colour-contrast issue.

## 9. Kitchen Boundaries Implemented

The northwestern kitchen is designed using these nominal inner boundaries:

- West `x = -11.8`, east `x = -4.8` → 7 m.
- South `y = 2.8`, north `y = 8.8` → 6 m.

The eastern boundary uses two low counter sections with a **2 m robot access opening** at `y = 3.9` to `5.9`:

| Model | Centre `(x,y,z)` | Size `(x,y,z)` |
|---|---|---|
| `kitchen_east_counter_north` | `(-4.8,7.35,0.55)` | `(0.2,2.9,1.1)` |
| `kitchen_east_counter_south` | `(-4.8,3.35,0.55)` | `(0.2,1.1,1.1)` |

The southern kitchen boundary uses two partition segments and reserves a **1.6 m opening** for the dirty-dish / porter-side connection:

| Model | Centre `(x,y,z)` | Size `(x,y,z)` |
|---|---|---|
| `south_partition_west` | `(-11.2,2.8,1.4)` | `(1.2,0.2,2.8)` |
| `south_partition_east` | `(-6.9,2.8,1.4)` | `(4.2,0.2,2.8)` |

A screenshot of Gazebo's Entity Tree showed the two kitchen counters and two south partition models loaded, and the scene showed the beginning of the internal kitchen structure. A precise top-down clearance check was **planned but not yet performed**.

## 10. Learning Evidence and Current Limits

**Evidence from this study conversation:** Real `gz topic` scan readings for distance, angular sampling, front/rear coverage and height tests; SDF code excerpts; Gazebo screenshots of the exterior walls and initial kitchen partitions; debugging of XML, sensor geometry and material changes.

**What I demonstrated today:**

- Connected LiDAR range data to physical dimensions and sensor mounting offsets.
- Compared mathematical beam-count predictions with observations.
- Investigated scan wraparound at ±180°.
- Identified a vertical sensing limitation and debugged visual-versus-collision geometry.
- Constructed and visually tested exterior walls, entrances and kitchen boundaries in my existing SDF world.
- Improved understanding of SDF `pose`, `visual`, `collision`, `material`, `static` and world `scene` elements.

**Not yet completed or claimed:**

- A validated real sensor-noise or reflectivity model.
- Verified scan metadata in every experiment, or systematic collision-clearance testing.
- Connecting the actual Gazebo LiDAR data to a ROS 2 `LaserScan` processing node and RViz2 visualisation.
- IMU physics/integration, odometry fusion, SLAM, localisation, Nav2 navigation, or automated delivery.
- Bar, toilets, storage, complete porter room, dining furniture or dynamic obstacles.
- A fully functioning autonomous restaurant robot.

## 11. Exact Next Steps

1. Review the kitchen entrances from a clear top-down view and verify robot turning clearance.
2. Design and construct the open-kitchen cooking/preparation/plating stations.
3. Create a separate porter / dish-return passage, storage and staff/customer facilities.
4. Add the bar, tables, chairs and realistic navigation bottlenecks.
5. Test wall and counter collision geometry and real Gazebo LiDAR observations in the completed environment.
6. Learn IMU physics and uncertainty in depth; then integrate and test a simulated IMU.
7. Bridge actual Gazebo sensor streams to ROS 2, visualise in RViz2, and progress toward sensor fusion, mapping, localisation, navigation, recovery and generalisation.

## 12. Reflection

Today I moved from isolated LiDAR calculations to **controlled simulated experiments and a real environment-building workflow**. The most useful finding was that an obstacle could appear to be 10 cm tall in collision geometry but still be detected because its *visual* geometry remained 80 cm tall. By correcting the inconsistency and retesting, I demonstrated a vertical blind spot rather than accepting misleading data.

I also made progress implementing the restaurant architecture directly. The environment is deliberately unfinished: it will become progressively more realistic while I learn the physics, mathematics, ROS 2 integration and validation methods behind embodied robotic autonomy.

**Mission World 2028 focus:** Build reliable research skills through theory → derivation → implementation → controlled experiments → critical analysis, in preparation for a funded, research-based robotics Master's.

---

**Session status:** Stop after initial kitchen boundaries. Resume with kitchen-route verification and interior design; do not mark LiDAR integration, autonomous navigation, or IMU work as complete.

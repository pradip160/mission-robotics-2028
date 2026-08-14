# Mission Robotics 2028

> Building from the foundations toward robotics research — one project, experiment, mistake, and improvement at a time.

## The Mission

Mission Robotics 2028 represents my future, my goal, and my ambition.

I started this journey after graduating with a 2:2 degree and struggling to begin the career I wanted. I started robotics from almost zero, later than many others, but I believe consistency, discipline, and the work I build from now on can demonstrate more about my ability than one academic result alone.

I am building this journey while working in a restaurant and studying alongside it.

This repository records where I started, what I learn, what I build, the mistakes I make, and the engineer and researcher I am working to become.

---

## Why This Repository Exists

I created this repository to keep evidence of my progress instead of allowing the journey to disappear with time.

I regularly push my code, experiments, and learning notes. Since Day 1, I have tried to record:

- what I learned
- what problems I faced
- how I approached and debugged them
- what I changed
- where the related code can be found

One day I want to be able to return to the beginning of this repository, compare it with where I reached, and know that the effort was worth it.

**I keep track of the journey from Day 1.**

---

## Current Focus

I am currently building my foundation in robotics through ROS 2 while developing my restaurant robot project.

I recently started robot simulation and am gradually connecting the ROS 2 concepts I previously learned to a robot that I can actually see, test, and control.

Alongside robotics, I am also studying the mathematics required for more advanced robotics and future research.

### How I Learn

I am not a textbook-only learner.

I learn best by understanding a concept, attempting to implement it, making mistakes, finding out why something failed, improving it, and trying again.

**Learn → Try → Make mistakes → Understand → Improve → Repeat**

I followed this approach while learning ROS 2 and am now applying the same method to simulation and robotics development.

---

## Main Project — Restaurant Robot

My main project is a ROS 2 based restaurant robot.

Working inside restaurants has made me familiar with busy kitchen and restaurant environments and the physical demands placed on people working long shifts.

That experience strongly influences the kind of robotics problems I want to explore.

The restaurant robot is currently my learning and experimentation platform for navigation, robot safety, sensing, decision making, communication between ROS 2 nodes, and simulation.

### Current Capabilities

The robot can currently:

- move forward and backward
- turn left and right
- receive obstacle information
- make simple navigation decisions
- choose a clear direction when obstacles are reported
- perform recovery behaviour
- enter safe stop conditions
- stop safely when an unknown motor command is received
- convert navigation decisions into velocity commands
- physically move and respond inside Gazebo simulation

The current obstacle information is still produced by simulated ROS 2 sensor publishers.

The next major step is connecting actual Gazebo sensors such as LiDAR so that obstacles in the simulated environment are detected by the robot itself.

---

## Technology Stack

### Programming
- Python
- C++ — planned as the next major programming language

### ROS 2
- Publishers and subscribers
- Topics
- Custom messages
- Services
- QoS
- Parameters
- Launch files

### Robot Description & Simulation
- URDF
- TF
- RViz
- Gazebo
- Differential drive
- ROS 2 ↔ Gazebo communication

### Development
- Ubuntu Linux
- Git
- GitHub

Python is currently my primary robotics language. As I develop my C++ skills, I plan to use both languages where they are most appropriate rather than replacing one completely.

---

## Long-Term Research Direction

My long-term goal is to develop robots that can work safely and intelligently alongside humans in busy and constantly changing environments such as commercial kitchens.

I am interested in robots that can:

- navigate safely through crowded environments
- distinguish between objects and understand their surroundings
- anticipate human movement from behaviour
- cooperate naturally with human coworkers
- grasp and manipulate objects reliably
- handle tools and ingredients safely
- manage tasks according to human orders
- monitor stock and operational state
- manage battery and long-duration operation
- maintain safe physical behaviour in unpredictable environments

A kitchen is an environment where a wrong movement or grasp can be costly or dangerous. Because of this, I am especially interested in reliable perception, manipulation, human-aware navigation, and safe decision making.

My biggest interest is not simply making robots execute predefined movements.

I want to understand how a robot can:

**observe → understand → predict → decide → act safely**

Eventually, I want to explore robotic systems capable of understanding human behaviour and cooperating with people more naturally, closer to the way human coworkers continuously adapt to one another.

---

## Progress & Evidence

The main evidence of my work is contained inside this repository.

If you want to understand how I have developed, I recommend starting with the **daily learning logs**.

Each log records the topic I studied, what I understood, problems I encountered, debugging attempts, changes I made, and links or locations for the related implementation.

### Explore

- [Daily Learning Logs](learning-log/2026/)
- [Restaurant Robot Project](projects/ros2-restaurant-delivery-robot/)
- [Roadmap](roadmap.md)
- [Portfolio Summary](portfolio-summary.md)

If you are interested in a particular topic, the learning logs are organized by topic and day so that the progression can be followed from the beginning.

---

## 2028 Goal

By 2028, I want this repository to contain much more than student exercises.

My goal is to develop it into a research-oriented robotics portfolio containing:

- strong robotics projects
- autonomous robot simulations
- physical robot experiments
- research paper reproductions
- controlled experiments and evaluation
- advanced navigation and perception work
- manipulation
- human–robot interaction
- original research work

My academic goal is to become capable of contributing meaningfully to a robotics research laboratory and competitive for funded graduate study.

Most importantly, I want this repository to preserve where I started, how I changed direction, what I struggled with, what I built, and how far the journey eventually took me.

---

**Mission Robotics 2028 is a work in progress.**

So am I.

# Mission Korea 2028 — Day 72 Learning Notes

**Date:** Wednesday, 28 October 2026  
**Project:** Humanoid Robot — Two-Link Leg  
**Topics:** Jacobian matrix, velocity vectors, swing-foot trajectories, differentiation and the chain rule  
**Repository:** `mission-robotics-2028`  
**Study time:** Not recorded (do not count toward logged hours without confirmation)  
**Session type:** Mathematics, theory, handwritten calculations and graph interpretation  
**Status:** Today's lessons reviewed; acceleration deferred to the next session

## 1. Today's Objective

Continue from the two-link leg kinematics lessons and understand how mathematical equations describe **the movement of a humanoid robot's foot**:

- Relate joint angular velocities to foot velocity using the Jacobian.
- Distinguish velocity components, total speed and direction.
- Plan a simple foot path that rises above an obstacle.
- Explain how differentiation converts position into velocity.
- Apply the chain rule with radians and interpret the sign of velocity.

## 2. Two-Link Leg: Jacobian Completed

**Assumptions and coordinate convention**

- Thigh length: $L_1 = 0.4\ \mathrm{m}$.
- Shin length: $L_2 = 0.4\ \mathrm{m}$.
- Hip angle: $\theta_1=0^\circ$; knee angle: $\theta_2=90^\circ$.
- Hip at the origin; $+x$ points forward and $+z$ points upward.
- Joint angular velocities are in **rad/s**.

Forward kinematics:

$$
x_f=L_1\sin\theta_1+L_2\sin(\theta_1+\theta_2)
$$

$$
z_f=-L_1\cos\theta_1-L_2\cos(\theta_1+\theta_2)
$$

Jacobian:

$$
J=\begin{bmatrix}
\dfrac{\partial x_f}{\partial\theta_1} & \dfrac{\partial x_f}{\partial\theta_2}\\[6pt]
\dfrac{\partial z_f}{\partial\theta_1} & \dfrac{\partial z_f}{\partial\theta_2}
\end{bmatrix}
=\begin{bmatrix}0.4&0\\0.4&0.4\end{bmatrix}
$$

For $\dot\theta_1=0.5\ \mathrm{rad/s}$ and $\dot\theta_2=1.0\ \mathrm{rad/s}$:

$$
\begin{bmatrix}\dot x_f\\\dot z_f\end{bmatrix}
=J\begin{bmatrix}0.5\\1.0\end{bmatrix}
=\begin{bmatrix}0.2\\0.6\end{bmatrix}\ \mathrm{m/s}
$$

**Interpretation:** The foot is moving **forward at 0.2 m/s** and **upward at 0.6 m/s** at this instant, relative to the hip in this model. Jacobian entries have units of m/rad, so multiplying by rad/s gives m/s.

**What I corrected:** I initially set both joint angles to $0^\circ$ when evaluating a Jacobian component. The knee angle was actually $90^\circ$, so $\partial z_f/\partial\theta_1=0.4$, not zero.

## 3. Velocity Magnitude, Direction and Signs

The total foot **speed** is the magnitude of the velocity vector:

$$
\lVert\vec v_f\rVert=\sqrt{(0.2)^2+(0.6)^2}=\sqrt{0.40}\approx0.6325\ \mathrm{m/s}.
$$

Velocity direction measured upward from the $+x$ axis:

$$
\alpha=\operatorname{atan2}(0.6,0.2)\approx71.565^\circ.
$$

A comparison vector $(0.6,0.2)$ m/s has the **same speed** but a shallower direction (about $18.435^\circ$). Magnitude does not determine direction, and neither of these velocities alone determines the leg's pose.

For $\vec v=(0.5,-0.3)$ m/s:

- $+0.5$ means **forward** horizontal velocity.
- $-0.3$ means **downward** vertical velocity.
- The direction lies **below** the $+x$ horizontal axis.
- A minus sign is interpreted using the axis on which it occurs.

**Corrections from practice:** I initially mixed up which of two robots had the larger upward velocity, and made an error calculating the direction angle. After review, I correctly interpreted velocity signs and directions without a calculator.

## 4. Planning a Swing-Foot Trajectory

**Problem:** Move a foot $D=0.40$ m forward over $T=2$ s, rising to maximum height $H=0.15$ m.

Simple introductory model, valid for $0\le t\le2$ s:

$$
x(t)=\frac{D}{T}t=0.20t
$$

$$
z(t)=H\sin\left(\frac{\pi t}{T}\right)=0.15\sin\left(\frac{\pi t}{2}\right)
$$

| Time $t$ | Forward position $x(t)$ | Height $z(t)$ | Meaning |
|---:|---:|---:|---|
| 0.0 s | 0.00 m | 0.0000 m | Foot starts at ground level |
| 0.5 s | 0.10 m | 0.1061 m | Foot rising |
| 1.0 s | 0.20 m | 0.1500 m | Maximum height |
| 1.5 s | 0.30 m | 0.1061 m | Foot descending |
| 2.0 s | 0.40 m | 0.0000 m | Foot reaches ground level |

For a **narrow** obstacle of height 0.10 m at $x=0.20$ m (assuming the height function describes the foot's lowest point and perfect tracking), vertical clearance at its centre is:

$$
C=0.15-0.10=0.05\ \mathrm{m}=5\ \mathrm{cm}.
$$

**My reasoning:** Start and end positions alone are insufficient; the robot also needs a path that accounts for the lift, swing, landing, and nearby obstacles. I suggested a 25% extra clearance margin as an example, but this is **not a universal safety rule**. Real clearance depends on foot geometry, obstacle width, sensor errors and control errors.

**What I corrected:** I initially obtained $z(1)\approx0.00411$ m because my calculator was set to **degrees (DEG)** while the expression used **radians (RAD)**. Correctly evaluating $\sin(\pi/2)$ gives 1, so $z(1)=0.15$ m.

## 5. Derivatives: Position to Vertical Velocity

**Key meaning:** A derivative measures how quickly one quantity changes with respect to another. Here, differentiating height with respect to time gives **instantaneous vertical velocity**:

$$
\dot z(t)=\frac{dz(t)}{dt}.
$$

- Positive $\dot z$: foot rising.
- Zero $\dot z$: instantaneously no vertical movement (it can still move horizontally).
- Negative $\dot z$: foot descending.

**Chain rule:** For constant $A$ and $k$,

$$
\frac{d}{dt}[A\sin(kt)]=Ak\cos(kt).
$$

I independently answered the practice question:

$$
\frac{d}{dt}[4\sin(3t)]=12\cos(3t).
$$

For the original $H=0.15$ m, $T=2$ s trajectory:

$$
\dot z(t)=0.15\frac{\pi}{2}\cos\left(\frac{\pi t}{2}\right)
\approx0.23562\cos\left(\frac{\pi t}{2}\right)\ \mathrm{m/s}.
$$

In particular, $\dot z(1)=0$ m/s at the highest point, although $\dot x=0.20$ m/s remains positive in this simple model.

### Follow-up exercise: 0.20 m height over 4 seconds

$$
z(t)=0.20\sin\left(\frac{\pi t}{4}\right)
$$

I independently derived the **correct** chain-rule result:

$$
\boxed{\dot z(t)=0.20\frac{\pi}{4}\cos\left(\frac{\pi t}{4}\right)}
$$

Equivalently:

$$
\dot z(t)\approx0.15708\cos\left(\frac{\pi t}{4}\right)\ \mathrm{m/s}.
$$

- At $t=2$ s: $\cos(\pi/2)=0$, so $\dot z(2)=0$ m/s; foot at its peak ($z=0.20$ m).
- At $t=4$ s: $\cos(\pi)=-1$, so $\dot z(4)=-0.15708$ m/s; foot is moving **downward immediately before landing**.

**What I corrected:** I first reported about $0.1569$ m/s at $t=2$ s because the calculator was again in **DEG mode**. I identified the settings mistake, changed to **RAD mode**, and later correctly explained the negative landing velocity.

**Engineering limitation:** The simple sine trajectory commands a **nonzero downward velocity at touchdown** (and nonzero upward velocity at takeoff). We must improve the endpoint behaviour before using it for a realistic soft landing.

## 6. Learning Evidence and Honest Self-Assessment

**Evidence from today's conversation:**

- Independently calculated Jacobian-based foot velocity: $(0.2,0.6)$ m/s.
- Correctly explained why Jacobian units multiplied by rad/s produce m/s.
- Independently interpreted forward/downward velocity signs.
- Calculated midpoint trajectory height after correcting calculator mode: $z(0.5)\approx0.1061$ m.
- Shared a **handwritten calculation and sketched sine-shaped height-versus-time graph** during the lessons. (Image shared in chat; not yet added to the repository.)
- Independently differentiated $4\sin(3t)$ and $0.20\sin(\pi t/4)$ correctly.
- Correctly interpreted the foot's downward landing velocity at $t=4$ s.

**Strengths:** Connecting mathematical results to physical robot movement; recognising and correcting unit/calculator mistakes; applying the basic sine chain rule to new expressions.

**Still needs practice:** Evaluating trig functions consistently in radians; carefully distinguishing height, velocity and acceleration; writing clear physical explanations; deriving the full trajectory independently without prompts.

**Not claimed today:** No new Python implementation, ROS 2 run, automated test, simulation, or Git commit was reported as completed during this session. Study minutes were not recorded.

## 7. Next Session — 29 October 2026

**Main topic:** Acceleration (rate of change of velocity).

Continue from this exercise, **without marking it completed yet**:

$$
a_{\mathrm{avg}}=\frac{v_1-v_0}{t_1-t_0}
$$

Given $v_0=+0.15708$ m/s at $t_0=0$ s and $v_1=0$ m/s at $t_1=2$ s:

1. Calculate average vertical acceleration in **m/s²**.
2. Explain how a foot can still move upward while having **negative** vertical acceleration.
3. Differentiate the vertical-velocity equation to obtain **instantaneous acceleration**.
4. Compare a safe contact trajectory against the current sine trajectory's nonzero landing velocity.

**Teaching plan:** Theory → physical meaning → small mathematical example → my independent attempt → supervisor review. No large code dumps.

---

**Session takeaway:** *The Jacobian relates joint motion to foot motion. A trajectory specifies foot position over time. Differentiating position gives velocity; next, differentiating velocity will give acceleration.*

**Mission Korea objective:** Build the mathematical, programming and experimental skills needed for a competitive funded robotics Master's application in South Korea in 2028.

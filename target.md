# Mission World 2028 — Robotics Research Targets

**Target intake:** Fall 2028, subject to each programme's calendar

**Last reviewed:** 25 November 2026

**Status:** Preparation and provisional research shortlist; no 2028 admission, supervision or funding is confirmed.

## My goal

My primary goal is to secure a fully funded direct PhD or integrated Master's–PhD in embodied robotics, targeting 2028 entry. A funded research-based Master's with substantial laboratory work remains a practical alternative if direct doctoral entry is not academically feasible.

I want to become an independent robotics researcher capable of identifying problems, developing hypotheses, building systems, conducting controlled experiments and defending conclusions using evidence. My interests are embodied intelligence, autonomous mobile robots, physical interaction, reliable decision-making and service robotics. My restaurant delivery robot is the foundation, not the final research objective.

My long-term ambition is to contribute to useful robotics in Nepal, particularly kitchen and service automation, and eventually establish a research-driven robotics company. My experience working as a chef gives me firsthand exposure to operational constraints, food transport, hygiene, workflow and safety. That experience is a source of research questions, not a substitute for engineering evidence.

## My starting position and constraints

- BSc (Hons) Computer Science, University of West London, completed in 2026, with a UK 2:2 classification.
- My undergraduate results are a significant admissions constraint, especially for direct PhD routes. I must verify minimum grades and degree equivalence before investing heavily in any application.
- My current experience is primarily self-directed robotics development and simulation, not established academic research. I do not claim publications, physical robot validation or advanced research competence without evidence.
- I work in hospitality while preparing for postgraduate study. My working target is approximately 20 focused study hours per week, adjusted to my shifts and personal commitments.
- Funding is a core requirement because I have living costs and family responsibilities. I will not treat uncertain employment or a hoped-for later scholarship as guaranteed funding.
- I need to strengthen mathematical foundations, technical independence, scientific writing and experimental methodology. Consistency and focused practice matter more than accumulating tutorials.

## The learning environment I want

I want to spend substantial time in an active lab: building and testing robots, discussing problems, learning from other students and getting guidance when I reach the limits of my current understanding.

Independent reading, mathematics and programming will remain part of my work. I want a lab community that helps me connect that study to experiments and develop increasing independence.

My priorities are:

- A supervisor who gives regular, useful feedback.
- A clear onboarding process and someone I can approach for technical guidance.
- Research students who participate in lab meetings, experiments and shared projects.
- Opportunities to learn alongside peers and more experienced researchers.
- Access to robot hardware, simulation tools and appropriate safety training.
- Funding that makes sustained study and research financially realistic.

## Research interests and current preparation

| Area | Questions I want to explore |
| --- | --- |
| Localization, SLAM and sensor fusion | How can a robot estimate its state reliably under slip, noise, drift and sensor failure? |
| Navigation and safety | How can uncertainty, obstacles and sensor freshness influence safe autonomous decisions? |
| Dynamics and food transport | How do payload mass, stiffness, damping, speed and floor disturbances affect vibration and liquid stability? |
| Embodied decision-making | How can a robot adapt its motion to task demands and physical feedback rather than fixed manually tuned rules? |
| Human-aware service robotics | How can robots operate predictably in shared, changing restaurant and kitchen environments? |
| Manipulation and robot learning | How can perception, control and physical interaction eventually support useful kitchen tasks? |

My [current portfolio](README.md) is centred on a ROS2 Jazzy and Gazebo restaurant delivery robot. Work to date includes sensor-status handling, safe-stop logic, recovery concepts, differential-drive odometry, coordinate transforms and LiDAR experiments. I have studied IMU behaviour, sensor uncertainty, vibration, natural frequency, damping and payload-aware motion decisions. These are foundations; integrated sensor fusion, robust SLAM, validated adaptive control and manipulation are not claimed as completed. The repository and experiment logs must establish the exact implementation status.

## Research learning system

For each substantial topic I will follow **UNDERSTAND → DERIVE → IMPLEMENT → EXPERIMENT → ANALYSE → IMPROVE → DOCUMENT**. I will begin with physical meaning and a realistic case, derive the necessary mathematics, attempt pseudocode and implementation independently, then seek feedback and test against evidence.

My daily research notes will be written in my own words, recording the question, hypothesis, assumptions, method, observations, interpretation, limitations and next experiment. I will distinguish measured results from predictions. Git commits should represent meaningful, reproducible progress rather than activity alone.

## Technical roadmap and measurable evidence

| Period (planning targets) | Focus | Evidence required |
| --- | --- | --- |
| Now–March 2027 | Reliable robot simulation, LiDAR/IMU/odometry, frames, basic dynamics and safety | Reproducible launch and tests; sensor failure cases; documented model assumptions and baseline metrics |
| April–August 2027 | Localization, SLAM, sensor fusion, navigation and control | Compare estimated pose against simulation ground truth; quantify position/heading error, recovery and navigation performance under varied noise and slip |
| September–December 2027 | Payload-aware motion and embodied decision-making | Compare fixed-speed and adaptive policies over matched routes, payloads and disturbances; measure acceleration, jerk, vibration, completion time and failures |
| January–Spring 2028 | Consolidation, research report, supervisor outreach and applications | Reproducible experiments, clear figures, literature review, concise research proposal, CV, transcript and verified eligibility/funding records |
| Later, when foundations are reliable | Manipulation, physical platforms and robot learning | A justified research question and validated baseline before adding complexity |

Mathematical priorities: linear algebra, calculus, probability and statistics, coordinate transformations, differential equations, rigid-body dynamics, estimation, feedback control and optimization. I will connect each to a robot problem rather than study formulas in isolation.

A possible research question is whether payload-aware speed and acceleration control can reduce disturbance during service robot transport without unacceptable delivery delays. This is a candidate question, not a claim of novelty. A liquid payload needs an appropriate slosh model or physical validation; platform acceleration alone does not prove that soup will not spill.

## Objective readiness gates

- [ ] Explain core algorithms and mathematical assumptions without relying on generated answers.
- [ ] Independently implement, debug and explain a substantial part of the robot system.
- [ ] Maintain a reproducible integrated simulation with setup instructions, versioned configurations and tests.
- [ ] Complete at least three documented controlled experimental comparisons with baselines, repeated trials, quantitative metrics and limitations.
- [ ] Produce a research-style report and a literature review that identifies a defensible question and related work.
- [ ] Demonstrate safe behaviour under sensor loss and difficult operating conditions; distinguish simulation results from physical evidence.
- [ ] Obtain feedback from researchers or qualified mentors and address substantive criticism.
- [ ] Verify degree eligibility, funding and supervisor fit for each application route; secure appropriate references.

These are self-imposed preparation targets, not guarantees of admission. Review them weekly using actual evidence of what I learned, implemented, tested and independently demonstrated.

## How I will evaluate a target

| Criterion | Evidence to collect |
| --- | --- |
| Research fit | Recent papers and projects connected to my interests; a feasible research question for the intended degree. |
| Supervision | Expected meeting frequency, feedback process and who supports new students. |
| Peer learning | Whether students on my intended route join group meetings, shared experiments, code reviews or team projects. |
| Practical access | When students can join the lab, use robots and receive training; whether access depends on a thesis or separate selection. |
| Funding | Written details of tuition, stipend or salary, deductions, duration, renewal conditions and expected costs. |
| Admission eligibility | Official assessment of my degree, transcript, subject prerequisites and language evidence. |
| Working language | Languages used in everyday lab discussion, supervision, safety training and administration. |

**Decision rule:** Keep a target provisional until academic eligibility and a viable funding plan are established. Among viable options, give strong weight to supervision, peer learning and practical research access.

Unknown information means further investigation is needed. A university's reputation or a lab's equipment list does not establish the quality of day-to-day mentoring.

## Country strategy

My search is worldwide. South Korea remains an important starting point, but country prestige or preference must not override research fit, academic eligibility and guaranteed financial viability.

- **South Korea:** Investigate UST–KIST and relevant groups at UNIST, KAIST, DGIST, GIST, POSTECH and Korea University; prioritize suitable integrated or research degree routes where eligible.
- **China:** Investigate Tsinghua, SUSTech and other relevant robotics groups; verify international doctoral or integrated routes, supervisor requirements and scholarship coverage.
- **Germany and wider Europe:** Investigate funded doctoral routes where my degree qualifies, and research Master's alternatives; distinguish tuition-free study from fully funded living costs.
- **USA and other countries:** Investigate funded direct PhD or integrated routes with relevant faculty and explicit international eligibility.

These additional institutions are discovery leads, not verified matches or confirmed openings. I will build a broad but targeted application pipeline, not send indiscriminate mass emails. If no viable doctoral route is available, I will prioritize a funded research Master's; if no funded route materializes in 2028, reassess and strengthen my preparation rather than commit to an unaffordable degree.

## Initial shortlist

These are retained starting points from my October 2026 shortlist, not a ranking. Their published details have not been reverified in this revision. The entries include a research-training route, a programme with a student team, and an individual research group.

| Target | Why it belongs on my list | Main checks still needed | Stage |
| --- | --- | --- | --- |
| **UST–KIST, South Korea** — specific lab and supervisor to identify | A route worth exploring for institute-based research training. KIST is an institution, so I need to identify an individual group working on mobile robotics, perception or autonomy. | Relevant supervisors; Master's places for 2028; recent projects; mentoring and peer interaction; eligibility; language requirements; net funding after tuition and other deductions. | Investigating |
| **H-BRS, Germany — M.Sc. Autonomous Systems / Institute for AI and Autonomous Systems / b-it-bots** | Particularly relevant to my wish for collaborative learning. Official pages describe a student robotics team, onboarding, ROS/Python/C++ work and domestic or industrial robot projects. | Official admission assessment; costs and funding; access to the team; thesis supervision; frequency of guidance; how team activity connects to assessed research. | Investigating |
| **University of Bonn, Germany — Autonomous Intelligent Systems (AIS)** | Research includes mobile and service robotics, perception, mapping, navigation and human–robot interaction. Its official opportunities page describes a Computer Science Master's route with robotics specialization. | Master's admission requirements; a suitable supervisor and project; lab access; current opportunities; funding; whether assistant work is available and sufficient. | Investigating |

### Previously recorded official sources and cautions

**UST–KIST**

- [UST international admissions guides](https://admission.ust.ac.kr/prog/entschGuideline/admission_eng/sub02_01_01/list.do)
- [UST tuition and financial support](https://admission.ust.ac.kr/admission_eng/sub01_06.do)
- Next step: identify specific KIST groups through the applicable admissions guide and official faculty pages. Check that each group accepts Master's students in the intended intake.
- Confirm which costs come out of any stipend. Treat UST funding and separate scholarships such as GKS as distinct routes with their own requirements.

**H-BRS / b-it-bots**

- [Research and study opportunities](https://www.h-brs.de/en/a2s/join-us)
- [b-it-bots team and onboarding](https://www.h-brs.de/en/a2s/b-it-bots)
- [Autonomous Systems admission requirements](https://www.h-brs.de/en/inf/admission-application-master-autonomous-systems)
- The published entry requirement includes a German-equivalent grade of 2.5 or better. My eligibility needs an official assessment; portfolio strength does not replace this requirement.
- The programme's FAQ currently says the university and faculty do not offer scholarships. External or partner support needs separate verification and a complete budget.
- Team participation is described as voluntary. It does not itself establish paid employment, funded admission or an assigned research supervisor.

**University of Bonn / AIS**

- [AIS research areas](https://www.ais.uni-bonn.de/research.html)
- [Study, research and employment opportunities](https://www.ais.uni-bonn.de/jobs.html)
- Funded PhD advertisements do not establish Master's funding. Any student assistant opportunity needs a separate check for availability, eligibility, pay and duration.

These pages support the initial shortlist. They do not confirm openings or financial terms for Fall 2028.

## Questions for a supervisor or current research student

1. When can a new student on my intended degree route join the lab, and what does the first semester usually involve?
2. How often do students meet their supervisor? Who helps with technical onboarding and day-to-day research questions?
3. Do students on this route regularly work with one another and with PhD students? Can you describe a recent example?
4. What robot platforms can students on this route use, and what training or project approval is required?
5. How are projects chosen, and what level of independence is expected at the beginning?
6. What language is normally used in group meetings, informal technical discussion and safety training?
7. What funding is available for the full degree, what costs remain, and what conditions apply to renewal?
8. What do current students wish they had known before joining?

These are preparation questions. No contact with a lab is recorded in this file yet.

## Funding and eligibility checks before committing

- [ ] Confirm whether a UK 2:2 Bachelor's permits direct PhD, integrated degree or research Master's entry; ask about formal exceptions only where available.
- [ ] Confirm doctoral funding covers the expected full duration and whether teaching or research assistant duties are required.

- [ ] Confirm academic eligibility using the actual transcript and the programme's official assessment process.
- [ ] Confirm required language evidence and any waiver in writing.
- [ ] Separate admission, supervisor acceptance and scholarship decisions; establish which are required.
- [ ] Record tuition, mandatory fees, insurance, housing and realistic living costs.
- [ ] Record guaranteed funding, deductions, payment dates, duration and renewal conditions.
- [ ] Account for travel, deposits, initial setup and any required proof of funds.
- [ ] Check whether the plan remains workable without uncertain part-time employment.
- [ ] Verify the rules and deadlines for the actual 2028 intake.

## Next actions

1. Identify specific supervisors whose recent work connects to embodied robotics, robot dynamics, autonomous systems or service robotics.
2. Separate targets into direct PhD, integrated Master's–PhD and funded research Master's routes; screen academic eligibility early.
3. Read at least two relevant papers per high-priority group and record the problem, methods, limitations and connection to my work.
4. Develop my robot portfolio and research notes according to the readiness gates above.
5. Investigate suitable academic references and obtain feedback on my research preparation.
6. Prepare tailored supervisor outreach, targeting early 2028 or earlier when official deadlines require it. Verify deadlines individually; do not assume all applications open in spring.
7. Review research progress weekly and shortlist eligibility, funding and openings monthly.

## Record template for each specific lab

Copy this section when a target is ready for deeper investigation.

### [Lab name] — [University / institute, country]

- **Supervisor and official page:**
- **Degree route and intended intake:**
- **Minimum academic requirements and UK 2:2 assessment:**
- **Application and funding deadlines:**
- **Research connection to my project:**
- **Two recent papers and my notes:**
- **Possible research question:**
- **Evidence about supervision and peer learning:**
- **Robot access and onboarding:**
- **Working language:**
- **Admission eligibility and evidence:**
- **Funding, remaining costs and conditions:**
- **Contact history:** None recorded / add date and factual outcome.
- **Status:** Investigating / ready to contact / contacted / applying / closed.
- **Last verified and sources:**
- **Next action:**
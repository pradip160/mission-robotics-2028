# Dat 7 : Robot Input Validaction 

## Learning Evdience
- YouTube video:[https://youtu.be/x2TU5zsWDTc]
- Inside the vedio i explain what i learn and achive today. 
- Code file: project/ros2-restaurant-delivery-robot/control/Day06_robot_functions.py
- Topic: Input validation, reusable functions, try/except

## Goal 
My goal was to improve myself and make  better than  yesterday. I wanted to improve my previous day6 code. because i dont feel like the structure was okay and i through i need to make better pipeline.
so i create resuable functions to make code less messy. and i did add three of them myself and with help of gpt. by help of gpt i dodnt mean i copy everything. i learn concept and write myself and give gpt to check mistake. I used it like my teacher.

## Why Input Validation Matters in Robotics
Input Validation Mtters in Robotics becasue withouut clear input robot cant ack properly and make correct decision. Robot should never make decison based on half correct data. Imagine a restaurent robot operating live in a hall and someone isntruct it to deliver food, and it cant properly get the path data clearly if its operate in that situation it have very high risk of being crash.

## Reusable Yes/No Function
We can call this function inside the another function and it does what we put inside it. If i put like this can accept yes and y it will apply this rule in whichever file we call it.

## Reusable Number Function
In my code i put this function like: get_float(question). i can call it in whichever function i want or useful. it will make our job easy. i dont need to write it everywhere i need. i can just call it.

## Try and Except
If we want to run something riskey we can use this function. we use Try to run riskey code and Except ot recover it.

## Battery Validation
Battery Validation shows the valid range. the valid battery  range is fom 0 to 100. And battery cant be more than 100 and less than 0. If battery is less than 20 it consider as low battery and out robot should return to the base(charging station).


## Emergency Stop Validation
Emergency Stop Validation should treat as top pirority. so it need clear instruction like yes and no. we cant use maybe here because maybe is confusion and robot shouldnt act confuse in emergency case.

## Obstacle and path Validation  
Robot can face obstacle in many situation. In my code, if robot face a obstacle it wait for 3 sec and check if the path is clear or not. If the path is clear it follows the mission. if not then it looks for the alternative route. if there no alternative it shows like mission paused no alternative. if there alernative it cheks for the if that route is safe or not. if it safe it follows toward the distance validation if not it return mission paused.

## Distance Validation 
I add the new resuable distanec fucntion which i can resue whenever i need. In distance float() is best to use becuse distance can be folat sometimes and with out folat() if we put 8.4 it shows error.

## Main Control Flow Cleanup
In main control flow i put every function in logic order to run. it like where i control the program. 


## Tests completed
Test one : emrgency : yes 
status: Passed

test two : 
   emergency_stop: no 
   battery: 99
   obstacle: no
   distance: 0

status: passed

Test 3: 
    emergency_stop = no
    battery: 1
return: battery low returning to the charging station
status: passed

 And i also complete the all obstacle and distance tests.
- I also check the yes_no() and it worked. i test by typing y/n it worked. 
- i also check the resuable number function. it also passed.

 

## What i Learned

Things i learned today 
- I learn how to make resuable function
- I learned how to use get_yes_no(question) for emergency stop, obstacle, and path saftey.
- I learned how to use get_float(question) for number input like battery and distance.
- I learned that try/except prevents the program from crashing when the usert types.
- I learned that input validation is important becasue a robot should not move based on unclear data.
- I learned that return True and return False send saftey results back to the main robot control flow.
- I learned that each function should have one clear responsbility.
- I learned that move_robot() should return the movement result,and run_mission() should decide the final mission message




## Next Step 
In Day 8, I want to learn missoin loops and continious robot movement. Right now the robot checks distance once and stops. Nexr, i want the robot to keep checking distance until delivery is complete.

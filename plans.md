 𝓐𝖍𝖆𝖗𝖔𝖓_𝓢𝖊𝖌𝖆𝖑 ‧₊˚♪ 𝄞₊˚⊹ #️⃣ *️⃣ 0️⃣ 1️⃣ 2️⃣ 3️⃣ 4️⃣ 5️⃣ 6️⃣ 7️⃣ 8️⃣ 9️⃣ 🔟 ⭐ 🌟 ❌ ❗ 🚨 🔴🟠🟡🟢🔵🟣  🟥🟪🟦🟩🟨🟧


+----------------------+
|       GOAL           |
+----------------------+

🟢 a program that can
    - manage the dorms in the base
    - to help assign soldiers to dorms in a good maner
    - to give a status of the dorms accoupational state - who is here and who is not

🟢 THE MAIN GOAL 
    -   to make a program that recives a csv file by api 
        with a list of soldiers that need to be assigned a dorm
    -   the program will automaticly assign the soldiers to the dorm based on 
        set paramaters


⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘


________________________
------------------------

 ~ THE MAIN COMPONENTS
______________________

1️⃣ THE SOLDIERS REQUESTING TO BE ASSINGED TO A DORM
מספר אישי,שם פרטי,שם משפחה,מין,עיר מגורים,מרחק מהבסיס

revived from csv:
    ps (personal_id): int -> all start with 8 and have a len of 7
    first_name: str -> first name
    last_name: str  -> last name
    gender: str     -> male or female (not a bool field)
    lives_at: str   -> soldiers home
    distasnce: int  -> distance from base

generated in code:
    state: str -> 2 options is_assigned or waiting (not a bool)

🟡 when getting the list we assume that all soldiers in the list are expecting a dorm
______________________

2️⃣ THE DORMS

DORM A -> 10 rooms
DORM B -> 10 rooms

each room can house 8 soldiers

CAPACITY = len(DOORMS) * 8

currently  = 80 * 2 = 160

each dorm is a table
each room is a row and has the 8 soldiers in that row 


🚨 the code needs to be scalble to be able to add more dorms
________________________

3️⃣ THE WAITLIST

a waitlist of soldiers waiting to get assinged to a dorm
________________________


⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘


🟢 THE REQUIERMENTS
    1️⃣   import lIst from csv file

    2️⃣   rerun the doorm assignmets 

    3️⃣   display dorm status

    4️⃣   display waiting list

    5️⃣   things to consider
            - scalble to handle adding dorms
            - handling edge case -> number of rows in csv is smaller than number of rooms
            - handling edge cases -> any i can think of
            - handling incorect fields in csv

    6️⃣    future additions
            - adding dorms
            - option to request room
            - adding more filds (profile, rank, service_type)
        
    ⭐ custom additions
        NEW FIELD TO SOLDIER -> timstap for each soldier when assigned to dorm

🟢 EXECUTION -> START POINT
    1️⃣    - endpoint to recive csv
            - parse csv to obj  
            - ready to be added to db
            - assign all -> state: "waiting"

    2️⃣   - assignment_strategy
            assign based on distance from base
            querry based on distance then give the top CAPACITY
                and assining them to rooms
                setting each to state: "assinged"
        🟡 if the final 2 have the same distance then the defaul chosen is ok 

    
⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘

SERVER ROUTS


1️⃣   POST: assign_with_csv

2️⃣   

 3️⃣ 4️⃣ 5️⃣ 6️⃣ 7️⃣ 8️⃣ 9️⃣ 🔟


ROUTS


            
    





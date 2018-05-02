import pyodbc
import os
#COLOR LIST APPLIES TO TOUCHING STATE LIST! NOT THE STATE LIST!

def find_touching(state_arr, touch_arr, color_arr):    
    previous_state = 0
    current_state = 0
    next_state = 0
    color_subset = []    
    # Pointer array holds the indices of the first occurrence of each state, 0 will always be the first state
    pointers = [0]
    # To increment through each state
    p = 0
    

    while current_state < len(state_arr):
        # List for the colors of the states touching the current state
        
        # This tells the program what the next state is
        num_occur = state_arr.count(state_arr[current_state]) 
        next_state = next_state + num_occur
        print(f"State: {state_arr[current_state]} num_occur: {num_occur}")
        # Adds the next state to the pointer list
        
        #Creates a subset of the colors only from the touching states
        for num in range(current_state,next_state):
            if num < len(color_arr):                
                color_subset.append(color_arr[num])
                
        
            
        state_color = get_color(color_subset)      
        print(f"State Color: {state_color}")
        while len(color_subset) > 0:
            color_subset.pop()
        # If state_color returns -1, the map is invalid and the code needs to backtrack
        if state_color != -1 and next_state != len(state_arr):
            
            # Applies colors to every instance of the current state from touch_arr to color_arr
            for i in range(len(touch_arr)):
                if state_arr[current_state] == touch_arr[i]:             
                    color_arr[i] = state_color
            # Goes to the next state
            
            previous_state = current_state
            current_state = next_state
            if current_state < len(state_arr):
                pointers.append(current_state)
                p += 1
            
        elif state_color == -1:
            break
            
    #print(f"Pointer: {state_arr[pointers[p]]}")
    for m in range(0, len(state_arr)-1):
        print(f"State: {state_arr[pointers[m]]} Color: {color_arr[pointers[m]]}")
            
             
        
def get_color(colors):
    is_used = [True, False, False, False, False]

    # Sets every color from color_subset to true
    for color in colors:
        is_used[color] = True

    # The returns the first false value from is_used
    for i in range(len(is_used)):
        if is_used[i] is False:
            return i
        
    # returns -1 incase the program needs to go backwards
    return -1
    print(is_used)


def check_lengths(state_arr, touch_arr, color_arr):
    if len(state_arr) != len(touch_arr) or len(state_arr) != len(color_arr):
        print(f"""
State list: {len(state_arr)}
Touching State list: {len(touch_arr)}
Color Array: {len(color_arr)}
Arrays aren't equal lengths!
""")
    else:
        print("Lists are equal lengths.")

    
conn_str = (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
    r'DBQ=C:\Users\William\Desktop\FourColorMap\States1.accdb;'
    )
cnxn = pyodbc.connect(conn_str)
cursor = cnxn.cursor()

"""
SAMPLE LISTS:

# list of states
state_arr = ["A", "A", "B", "B", "B", "C", "C", "C", "D", "D"]
# list of states touching those states
touch_arr = ["B", "C", "A", "C", "D", "A", "B", "D", "B", "C"]
# Every instance of that state will be colored, refers to the states in touch_arr
color_arr = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# Outputs the colors of the states to final_color_arr for easier output to the form
final_color_arr = [0, 0, 0, 0]
"""
state_arr = []
touch_arr = []
color_arr = []
final_color_arr = []

cursor.execute("SELECT Abbreviation,Adjacent,Color FROM qryGetColors ORDER BY Abbreviation")
for row in cursor:
    state_arr.append(row.Abbreviation)
    touch_arr.append(row.Adjacent)
    color_arr.append(row.Color)
    






check_lengths(state_arr, touch_arr, color_arr)
find_touching(state_arr, touch_arr, color_arr)
print(f"Done \nColor_arr: {color_arr}")




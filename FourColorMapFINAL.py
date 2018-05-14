import pyodbc
# COLOR LIST APPLIES TO TOUCHING STATE LIST! NOT THE STATE LIST!
"""
TODO: Use current_touching_states to change the colors of every adjacent state to 0,
    then set all pointers back to 0 and run through the whole list again.
"""


# returns a list of unique states, colors, indexes for each unique state, and adjacent states
def get_unique_lists(state_arr, touch_arr):
    unique_state = []
    unique_color = []
    unique_index = []
    unique_adjacent = []
    i = 0
    for state in state_arr:
        if state not in unique_state:
            unique_state.append(state)
            unique_color.append(0)
            unique_index.append(i)
        i += 1
    unique_index.append(len(touch_arr))

    for i in range(len(unique_state)):
        unique_adjacent.append([None])
        for k in range(unique_index[i], unique_index[i+1]):
            unique_adjacent[i].append(touch_arr[k])

    # Gets rid of None from list
    for i in range(len(unique_adjacent)):
        unique_adjacent[i] = list(filter(None.__ne__, unique_adjacent[i]))

    # --------------Diagnostic----------------
    for i in range(len(unique_adjacent)):
        print(f"{unique_state[i]}: {unique_adjacent[i]}")

    return unique_state, unique_color, unique_index, unique_adjacent


# Finds how many states touch the current state
def find_touching(curr_state, state_arr, touch_arr, color_arr):
    i = 0    
    for state in state_arr:
        if state == curr_state:
            i += 1
    return i


# True = color is okay False = back up program
def check_color(current_color, adjacent, states, colors):
    print(f"color: {current_color} adjacent states: {adjacent}")
    color_indexes = []
    for i in range(len(adjacent)):
        for j in range(len(states)):
            if adjacent[i] == states[j]:
                color_indexes.append(j)
        if current_color == colors[color_indexes[i]]:
            return False
    return True


def color_map(unique_state, unique_color, unique_index, unique_adjacent):
    pointer = 0
    color = 1
    i = 0
    # ----------Diagnostic----------
    # print(f"state: {len(unique_state)} color: {len(unique_color)} index: {len(unique_index)} "
    #       f"adjacent: {len(unique_adjacent)}")

    while i < len(unique_state):
        if color == 5:
            color = 1
        check = check_color(color, unique_adjacent[i], unique_state, unique_color)
        # Set state's color if true
        if check:
            unique_color[i] = color
            i += 1
        if not check:
            unique_color[i] = 0
            i -= 1
        print(i)
        color += 1
    print(unique_color)

# -----------------------------------------------------------------------------------------------


# makes sure lists are the same length
def check_lengths(s, t, c):
    if len(state_arr) != len(touch_arr) or len(state_arr) != len(color_arr):
        print(f"""
        State list: {len(s)}
        Touching State list: {len(t)}
        Color Array: {len(c)}
        Arrays aren't equal lengths!
        """)
    else:
        print("Lists are equal lengths.")


conn_str = (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
    r'DBQ=C:\Users\William\Desktop\finalcode\States1.accdb;'
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
unique_state, unique_color, unique_index, unique_adjacent = get_unique_lists(state_arr, touch_arr)
color_map(unique_state, unique_color, unique_index, unique_adjacent)


# for i in range(0,len(unique_state)):
#     print(f"{i+3}: States: {unique_state[i]} Colors: {unique_color[i]} Index: {unique_index[i]}")
# print(state_arr[3])
# print(find_touching("AL", state_arr, touch_arr, color_arr))
# print(f"Done \nColor_arr: {color_arr}")

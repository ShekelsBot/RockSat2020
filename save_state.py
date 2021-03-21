# Save_State 
# Andrew Bruckbauer
# 3/10/2021
import pickle

#array holder for state
current_state = []

# take input of the data
raw = int(input('Enter a save sate: '))
current_state.append(raw)

# open a file, where you ant to store the data
file = open('save_state', 'wb')

# dump information to that file
pickle.dump(current_state, file)

# close the file
file.close()

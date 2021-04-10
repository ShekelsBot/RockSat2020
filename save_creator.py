# Save_State 
# Andrew Bruckbauer
# 3/10/2021
import pickle

#array holder for state
current_state = [0]

# open a file, where you ant to store the data
file = open('save_state', 'wb')

# dump information to that file
pickle.dump(current_state, file)

# close the file
file.close()

# Save_State 
# Andrew Bruckbauer
# 3/10/2021
import pickle

# take user input to take the amount of data
#number_of_data = int(input('Enter the number of data : '))
current_state = []

# take input of the data
'''
for i in range(number_of_data):
    raw = input('Enter a save sate '+str(i)+' : ')
    current_state.append(raw)
'''
raw = int(input('Enter a save sate  '))
current_state.append(raw)

# open a file, where you ant to store the data
file = open('save_state', 'wb')

# dump information to that file
pickle.dump(current_state, file)

# close the file
file.close()

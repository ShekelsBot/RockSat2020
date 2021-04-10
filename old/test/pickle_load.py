# Pickle_Load
# Andrew Bruckbauer
# 3/19/2021
import pickle

# open a file, where you stored the pickled data
file = open('save_state', 'rb')

# dump information to that file
data = pickle.load(file)

# close the file
file.close()

print('Showing the pickled data:')

cnt = 0
for item in data:
    print('The data ', cnt, ' is : ', item)
    cnt += 1

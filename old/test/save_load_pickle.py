# Andrew Bruckbauer
# 3/10/2021
# Pickle Save State Test
import pickle

filename = 'save_state'
infile = open(filename, 'rb')
new_holder = pickle.load(infile)
infile.close()
test_holder = new_holder

print ("Save State Test Script")
print ("Input a number to test if it saved")
print ("Current Value is "+str(new_holder)+".")

while (1):
    test_holder = input('Enter Number: ')
    print ('Updated Value is: '+test_holder)
    outfile = open (filename,'wb')
    pickle.dump(test_holder,outfile)
    outfile.close()
    exit



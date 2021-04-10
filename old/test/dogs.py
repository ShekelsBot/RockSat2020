# Andrew Bruckbauer
# 3/9/2021
# Pickle Testing
# Figure out Pickle module for saving state of code
import pickle

dogs_dict = { 'Ozzy': 3, 'Filou': 8, 'Luna': 5, 'Skippy': 10, 'Barco': 12, 'Balou': 9, 'Laika': 16 }

filename = 'dogs'
outfile = open(filename,'wb')
# filename is file W = Wirte B = binary
pickle.dump(dogs_dict,outfile)
# Two inputs varabile to be saved and filename
outfile.close()

infile = open(filename,'rb')
# filename is file r = read b = binary
new_dict = pickle.load(infile)
infile.close()

print(new_dict)
print(new_dict == dogs_dict)
print(type(new_dict))

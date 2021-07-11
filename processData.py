import csv
import os
import itertools
	
def getString(file, line):
    reader = csv.reader(open(file, 'r'))
    string = next(itertools.islice(reader, line, None))
    return string	

def run():
    row_count = 0
    a = 0
    Building = 0
    Door = 0
    Fence = 0
    Streetlight = 0
    Tree = 0
    Window = 0
    Hedge = 0
    Garage = 0	
    
    file = 'Input File'
    writeFile = 'Output File'
    crimeID = None
    images = []
    
    with open(file) as openFile:
            row_count = sum(1 for row in openFile)

    
    csvreader = csv.reader(open(file, 'r'))		
    writer = csv.writer(open(writeFile, 'w+', newline=''))


    while(a <= row_count-1):
        string = getString(file, a)

		Building = int(string[1])
        Door = int(string[2])
        Fence = int(string[3])
        Streetlight = int(string[4])
        Tree = int(string[5])
        Window = int(string[6])
        Hedge = int(string[7])
        Garage = int(string[8])
		
        if(Building != 0 and Door != 0 and Fence != 0 and Streetlight != 0 and Tree != 0 and Window != 0 and Hedge != 0 and Garage != 0):		
            
            writer.writerow(string)

        a += 1
                
 
if __name__ == '__main__':
    run()

import matplotlib.pyplot as plt
import numpy as np
import random
import csv

def main():
        
    f=open("pelda.txt", "r")
    seeds=[]
    breaks=[]
    jobs=[]
    machines=[]
    trys=[]
    n_trys=[]
    
    line=f.readline().replace('\n','').split(" ")
    seeds+=line  
    print(line)         
    
    line=f.readline().replace('\n','').split(" ")
    breaks+=line
    print(line)    
    
    line=f.readline().replace('\n','').split(" ")
    jobs+=line
    print(line)
    
    line=f.readline().replace('\n','').split(" ")
    machines+=line
    print(line)    
    
    line=f.readline().replace('\n','').split(" ")
    trys+=line
    print(line)     
    
    line=f.readline().replace('\n','').split(" ")
    n_trys+=line
    print(line) 
    
    f.close()
        
def job_generator(machines,jobs,result):
    
    result=open("r.txt", "w") 
    m_jobs=[]
    m_jobs= [[0 for x in range(machines)] for y in range(jobs)]
    
    for i in range (jobs):
        result.write("J"+str(i)+"\t")

    for m in range(machines):
        for j in range(jobs):
            m_jobs[j][m]=random.randint(1,10)
            result.write(str(m_jobs[j][m]))
            result.write("\t")
    result.close()
    return 0
if __name__=="__main__":
    main()   
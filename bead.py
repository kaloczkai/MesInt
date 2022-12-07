from numpy.random import seed
from numpy.random import randint
import numpy as np
import math
from scipy import constants 
import itertools

JOB_SIZE_ARRAY = [10, 20]
MACHINE_SIZE_ARRAY = [5, 10]

MAX_ITERATION_NUMBER = 100
BOLTZMAN_KONST=constants.k

PAUSES = [[7,12],[18,23]]

#Function which generates the execution time of the jobs
#[input]    sizeOfJobs
#[input]    sizeOfMachines
#[output]   array[n x m]
def generateJobs(size_of_jobs,size_of_machines):
    seed(1)
    job_matrix = randint(1, 10 ,size= (size_of_jobs,size_of_machines))
    return job_matrix

def calculateCMax(job_matrix_tmp,job_schedule, pauses):

    nr_of_rows = len(job_matrix_tmp[0])
    nr_of_columns = len(job_matrix_tmp[0])+(len(job_matrix_tmp)-1)

    job_matrix = np.zeros((len(job_matrix_tmp),len(job_matrix_tmp[0])),dtype = int)
    end_array = np.zeros((nr_of_rows,nr_of_columns),dtype = int)

    #Changeing the order of the job
    for i in range(len(job_schedule)):
        job_matrix[i] = job_matrix_tmp[job_schedule[i]-1]
    
    for i in range(len(job_matrix)):
        for j in range(len(job_matrix[0])):
            tmp_value = 0
            # first value
            if i == 0 and j == 0:
                tmp_value = job_matrix[i][j]
            #first row
            elif j == 0 :
                tmp_value = job_matrix[i][j] + end_array[j][i+j-1] 
            else:
                if end_array[j-1][i+j-1] > end_array[j][i+j-1]:
                    tmp_value = job_matrix[i][j] + end_array[j-1][i+j-1]
                else:
                    tmp_value = job_matrix[i][j] + end_array[j][i+j-1]
            #can start?/pauses?
            machine_can_start = whenCanMachinStart(current_start=(tmp_value-job_matrix[i][j]),work_time=(job_matrix[i][j]),pauses = pauses)
            
            if machine_can_start != 0:
                end_array[j][i+j] = machine_can_start + job_matrix[i][j]
            else:
                end_array[j][i+j] = tmp_value
            print(end_array)
    #CMax
    return np.max(end_array)

def whenCanMachinStart(current_start,work_time,pauses):
    #check pauses
    tmp_start = 0
    for i in range(len(pauses)):
        #start time is between the pause start and end
        if current_start >= pauses[i][0] and current_start < pauses[i][1]:
            tmp_start = pauses[i][1] 
        elif current_start + work_time > pauses[i][0] and current_start + work_time < pauses[i][1]:
            tmp_start = pauses[i][1]
        elif current_start <= pauses[i][0] and current_start + work_time >= pauses[i][1]:
            tmp_start = pauses[i][1]
        elif i != 0 and tmp_start >= pauses[i-1][0] and tmp_start + work_time > pauses[i][0]:
            tmp_start = pauses[i][1]
    
    return tmp_start

def logToFile(outfile,string):
    outfile.write(string+'\n')

def main():

    output_file = open("bead_log.txt","w")

    for job_size in JOB_SIZE_ARRAY:
        print('Job size: ',job_size)
        for machine_size in MACHINE_SIZE_ARRAY:

            logToFile(output_file,'Current Job size: '+str(job_size))
            logToFile(output_file,'Current Machine size: '+str(machine_size))

            print('Machine size: ',machine_size)
            overall_smallest_CMax = -1
            job_matrix = generateJobs(job_size,machine_size)
            logToFile(output_file,'Generated jobs:\n'+str(job_matrix))
            
            for iteration,jobs_order in enumerate(itertools.permutations(range(1,job_size+1))):
                if(iteration == MAX_ITERATION_NUMBER):
                    break
                current_CMax = calculateCMax(job_matrix,jobs_order,PAUSES)
                            
                if overall_smallest_CMax == -1:
                    overall_smallest_CMax = current_CMax

                if current_CMax < overall_smallest_CMax:
                    overall_smallest_CMax = current_CMax

                simulated_value = math.exp(-((overall_smallest_CMax-current_CMax)/((BOLTZMAN_KONST*iteration+1)*100000)))
                if simulated_value == 1:
                    print('\tAccepted job order: '+str(jobs_order)+' with CMax: '+str(current_CMax)+ ' Iteration: '+str(iteration))
                    logToFile(output_file,'\tAccepted job order: '+str(jobs_order)+' with CMax: '+str(current_CMax)+ ' Iteration: '+str(iteration))

    output_file.close()
main()





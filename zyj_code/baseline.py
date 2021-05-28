from solver import Solver
from task_scheduler import TaskScheduler
from DAG_scheduler import DAGScheduler
from data_loader import DataLoader
import numpy as np
import logging
import time



def DepthBasedBaseline(file_path="../ToyData.xlsx"):
    """
    Depth Based Baseline, implemented by Yanjie Ze
    """
    f = open('depthbased_baseline.txt', 'w')
    f.close()
    start_time = time.time()
    task_scheduler = TaskScheduler(file_path=file_path)
    solver = Solver(file_path=file_path)
    cur_depth = 0
    max_depth = task_scheduler.max_depth

    data_center = None
    placement = None
    finish_time = None
    task_set = None
    task_set_new = None
    final_placement = []
    final_time = 0
    while(cur_depth<=max_depth):
        if cur_depth ==0:
            task_set = task_scheduler.get_taskset(cur_depth)
            data_center = task_scheduler.get_datacenter()
            placement, finish_time = solver.get_placement(task_set, data_center)
            time_cost = np.max(finish_time)
            with open('depthbased_baseline.txt', 'a') as f:
                f.write("depth %d cost time %f\n"%(cur_depth, time_cost))
                f.close()
            print("time cost:", time_cost)
            final_time += time_cost
            cur_depth += 1
            final_placement.append(placement)
            continue

        task_set_new = task_scheduler.get_taskset(cur_depth)  
        data_center = solver.update_datacenter(placement, task_set_new, task_set, data_center)

        placement, finish_time = solver.get_placement(task_set_new, data_center)
        
        final_placement.append(placement)
        time_cost = np.max(finish_time)
        print("time cost:", time_cost)
        with open('depthbased_baseline.txt', 'a') as f:
            f.write("depth %d cost time %f\n"%(cur_depth, time_cost))
            f.close()
        final_time += time_cost
        task_set = task_set_new

        cur_depth += 1

    
    final_placement_show_depthbased(final_placement, task_scheduler)
    print("-----Depth Based Baseline Finish. Final Time:%f----\n"%final_time)
    end_time = time.time()
    print("-----Execution Time of Depth Based Baseline:-----",end_time-start_time)
    with open('depthbased_baseline.txt', 'a') as f:
        f.write("-----Depth Based Baseline Finish. Final Time:%f----\n"%final_time)
        f.write("-----Execution Time of Depth Based Baseline: %f----\n"%(end_time-start_time))
        f.close()


def JobStepBasedBaseline(file_path="../ToyData.xlsx", threshold=5):
    """
    Job Step Based Baseline, implemented by Yanjie Ze
    """
    f = open('jobbased_baseline.txt', 'w')
    f.close()
    start_time = time.time()
    print('Job Step Based Baseline, threshold = %d '%threshold)
    task_scheduler = TaskScheduler(file_path=file_path, threshold=threshold)
    solver = Solver(file_path=file_path)
    cur_step = 0
    max_step = task_scheduler.max_step
    
    data_center = None
    placement = None
    finish_time = None
    task_set = None
    task_set_new = None
    final_time = 0
    final_placement = []
    while(cur_step<=max_step):
        if cur_step ==0:
            task_set = task_scheduler.get_taskset_jobbased(cur_step)
            data_center = task_scheduler.get_datacenter()
            placement, finish_time = solver.get_placement(task_set, data_center)
            time_cost = np.max(finish_time)
            with open('jobbased_baseline.txt', 'a') as f:
                f.write("step %d cost time %f\n"%(cur_step, time_cost))
                f.close()
            final_time += time_cost
            cur_step += 1
            final_placement.append(placement)
            continue

        task_set_new = task_scheduler.get_taskset_jobbased(cur_step)  
        new_data_center = solver.update_datacenter(placement, task_set_new, task_set, data_center)

        placement, finish_time = solver.get_placement(task_set_new, new_data_center)
        time_cost = np.max(finish_time)
        with open('jobbased_baseline.txt', 'a') as f:
            f.write("step %d cost time %f\n"%(cur_step, time_cost))
        # print("time cost:", time_cost)
        final_time += time_cost
        task_set = task_set_new
        final_placement.append(placement)
        cur_step += 1
    
    print("-----Job Step Based Baseline Finish. Final Time:%f----\n"%final_time)

    ## show result
    final_placement_show_jobbased(final_placement, task_scheduler)
    end_time = time.time()
    print("-----Execution Time of Job Based Baseline: %f-------\n"%(end_time-start_time))
    with open('jobbased_baseline.txt', 'a') as f:
        f.write("-----Job Step Based Baseline Finish. Final Time:%f----\n"%final_time)
        f.write("-----Execution Time of Job Based Baseline: %f-------\n"%(end_time-start_time))
        f.close()
    return final_placement


def final_placement_show_jobbased(final_placement, task_scheduler):
    """
    Input: list of several placements in several step
    Output: show the placement
    """
    f =  open('jobbased_baseline.txt', 'a')
    for i in range(len(final_placement)):
        f.write("Step%d:\n"%i)
        print("Step%d:"%i)
        placement = final_placement[i]
        task_set = task_scheduler.get_taskset_jobbased(i)
        for id in range(len(task_set)):
            
            task = task_set[id]
            job_id = int(ord(task.task_name[1]) - ord('A'))
            task_id = int(task.task_name[2]) - 1
            try:
                dc_id = np.where(placement[job_id][task_id]==1)[0] + 1
            except:
                dc_id = np.where(placement[job_id][task_id]==1)[0][0] + 1
            
            f.write(str(task) + 'place in DC' + str(dc_id)+'\n')
            
            print(task, 'place in DC', dc_id)
    f.close()


def final_placement_show_depthbased(final_placement, task_scheduler):
    """
    Input: list of several placements in several step
    Output: show the placement
    """
    f =  open('depthbased_baseline.txt', 'a')
    for i in range(task_scheduler.max_depth):
        f.write("Depth%d:\n"%i)
        print("Depth%d:"%i)
        placement = final_placement[i]
        task_set = task_scheduler.get_taskset(i)
        for id in range(len(task_set)):
            
            task = task_set[id]
            job_id = int(ord(task.task_name[1]) - ord('A'))
            task_id = int(task.task_name[2]) - 1
            try:
                dc_id = np.where(placement[job_id][task_id]==1)[0] + 1
            except:
                dc_id = np.where(placement[job_id][task_id]==1)[0][0] + 1

            f.write(str(task) + 'place in DC' + str(dc_id)+'\n')
            print(task, 'place in DC', dc_id)
    f.close()   

    


if __name__=='__main__':
    # print('----------------------------')
    #DepthBasedBaseline()
    # print('----------------------------')
    # final_placement = JobStepBasedBaseline(threshold=6)
    
    JobStepBasedBaseline(threshold=6)
    
    
    #DepthBasedBaseline()
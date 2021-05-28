from task_scheduler import TaskScheduler
from DAG_scheduler import DAGScheduler
from data_loader import DataLoader
import pulp as lp
import numpy as np
import math

class Solver:
    def __init__(self, file_path="../ToyData.xlsx"):
        self.task_scheduler = TaskScheduler(file_path)

        self.finishtime_matrix = None
        self.placement_matrix = None
        self.data_center_dict = None
        

    def formulate_LP(self, task_set_list, data_center_dict, slot_change=0):
        """
        TODO: need to change data center num into max id of data center?
        """
        global MAX_VALUE
        MAX_VALUE = 0
        data_center_num = 0
        for key in data_center_dict.keys():
            data_center_num += 1
        task_num_all = len(task_set_list)

        # M
        bigM = (data_center_num * task_num_all)/ (task_num_all)
        bigM = 5


        # divide task by job
        job_num_all = 0
        job_list = []
        for i in range(len(task_set_list)):
            task_name = task_set_list[i].task_name
            job = task_name[1]
            if job not in job_list:
                job_list.append(job)
                job_num_all += 1

        # get max num of task of one job
        task_num_max = 0
        job_dict_count = dict()
        for job in job_list:
            job_dict_count[job] = 0
        for job in job_list:
            for task in task_set_list:
                if task.task_name[1] == job:
                    job_dict_count[job] += 1
        for job in job_list:
            if job_dict_count[job] > task_num_max:
                task_num_max = job_dict_count[job]
        

        # get max job id
        max_job = 'A'
        for j in job_list:
            if j>max_job:
                max_job = j
        max_job_id = ord(max_job)-ord('A') + 1
        

        
        # constant: execution time
        max_id = 0
        for task in task_set_list:
            ex_time = task.execution_time
            corr_job = task.task_name[1]
            task_id = int(task.task_name[2])-1
            if task_id > max_id:
                max_id = task_id
        max_id = max_id+1# here we need to add one
               
        constant_extime =np.zeros((max_job_id, max_id, data_center_num))
        for task in task_set_list:
            ex_time = task.execution_time
            corr_job = task.task_name[1]
            job_id = ord(corr_job) - ord('A')
            task_id = int(task.task_name[2])-1
            if task_id > max_id:
                max_id = task_id
            
            constant_extime[job_id][task_id][:] += ex_time 
       

        # constant: b_sj, bandwidth, aj, slot num
        constant_slot = np.zeros(data_center_num)
        constant_bandwidth = np.zeros((data_center_num, data_center_num))
        keys = list(data_center_dict.keys())
        for i in range(len(keys)):
            key = keys[i]
            cur_data_center = data_center_dict[key]
            constant_slot[i] = cur_data_center.slot_num # add slot num here
            for link_to in cur_data_center.link_dict.keys():
                link_id = int(link_to[2])-1# should minus 1
                bandwidth = cur_data_center.link_dict[link_to]
                constant_bandwidth[i][link_id] = bandwidth # add bandwidth here
        

        # constant: required data d_k_i_s
        constant_reqdata = np.zeros((max_job_id, max_id, data_center_num))
        for task in task_set_list:
            # first, get required data
            cur_task_id = int(task.task_name[2]) - 1
            cur_job_id = ord(task.task_name[1]) - ord('A')
            required_data_dict = task.data_dict
            # then, search for every data's source
            for data_point in required_data_dict.keys():
                data_point_num = required_data_dict[data_point]
                tgt_dc_id = -1
                for dc in data_center_dict.keys():
                    if data_point in data_center_dict[dc].data_list:
                        tgt_dc_id = int(dc[2]) - 1
                        break
                if tgt_dc_id == -1:
                   
                    raise Exception("Error: can't find data(%s) in any data center"%(data_point))
                else:# update
                    constant_reqdata[cur_job_id][cur_task_id][tgt_dc_id] = data_point_num
        

        # constant: complete time, c = max(d / b)
        constant_completime = np.zeros((max_job_id, max_id, data_center_num))
        for k in range(max_job_id):
            for i in range(max_id):
                for j in range(data_center_num):
                    max_c = 0
                    for s in range(data_center_num):
                        if constant_bandwidth[s][j]==0 or constant_reqdata[k][i][s]==0:                      
                            continue
                        tmp_c = constant_reqdata[k][i][s]/constant_bandwidth[s][j]
                        if max_c < tmp_c:
                            max_c = tmp_c
                    constant_completime[k][i][j] = max_c
        
        
         # constant: M^(c+e)
        constant_exponetial = np.zeros((max_job_id, max_id, data_center_num))
        for k in range(max_job_id):
            for i in range(max_id):
                for j in range(data_center_num):
                    if constant_extime[k][i][j] == 0:
                        constant_exponetial[k][i][j] = 0
                        continue                   
                    constant_exponetial[k][i][j] = np.exp(constant_extime[k][i][j] + constant_completime[k][i][j])
        
        """
        init the result matrix: finish time matrix
        """
        self.finishtime_matrix = np.zeros((max_job_id, max_id, data_center_num))
        self.placement_matrix = np.zeros((max_job_id, max_id, data_center_num))
        
        """
        for now, we have several constants
        then we can solve LP problem
        """
        # define problem
        problem = lp.LpProblem(name='Max-Min-Fairness', sense=lp.LpMinimize)

        # variable name
        variable_name = ['x_kij', 'lambda_kij0', 'lambda_kij1']
        ## one way
        variable_x = [[[lp.LpVariable('x%d%d%d'%(k,i,j), cat='Binary') for j in range(data_center_num) ] for i in range(max_id) ]for k in range(max_job_id)]
        variable_lambda0 = [[[lp.LpVariable('lambda0%d%d%d'%(k,i,j), cat='Binary')for j in range(data_center_num) ] for i in range(max_id) ]for k in range(max_job_id)]
        variable_lambda1 = [[[lp.LpVariable('lambda1%d%d%d'%(k,i,j), cat='Binary') for j in range(data_center_num) ] for i in range(max_id) ]for k in range(max_job_id)]
        
        ## delete the varibale which is not needed
        for k in range(max_job_id):
            for i in range(max_id):
                for j in range(data_center_num):
                    if constant_completime[k][i][j] <= 0.: 
                        variable_lambda0[k][i][j] = 0
                        variable_lambda1[k][i][j] = 1
                        variable_x[k][i][j] = 0
                        constant_completime[k][i][j] = MAX_VALUE # change to a very large value
  

        ## another way
        # job_dim1 = np.zeros(max_job_id)
        # task_dim1 = np.zeros(max_id)
        # dc_dim1 = np.zeros(data_center_num)
        # job_dim2 = np.zeros(max_job_id)
        # task_dim2 = np.zeros(max_id)
        # dc_dim2 = np.zeros(data_center_num)
        # job_dim3 = np.zeros(max_job_id)
        # task_dim3 = np.zeros(max_id)
        # dc_dim3 = np.zeros(data_center_num)
        # variable_x = lp.LpVariable.dicts('variable_x', (job_dim1, task_dim1, dc_dim1), cat='Binary')
        # variable_lambda0 = lp.LpVariable.dicts('variable_lambda0', (job_dim2, task_dim2, dc_dim2), cat='Binary')
        # variable_lambda1 = lp.LpVariable.dicts('variable_lambda1', (job_dim3, task_dim3, dc_dim3), cat='Binary')

        # target equation
        
        objective = lp.lpSum([variable_lambda0[k][i][j] + variable_lambda1[k][i][j] * constant_exponetial[k][i][j] for k in range(max_job_id) for i in range(max_id) for j in range(data_center_num)])
        problem += objective

        # add constraint

        for k in range(max_job_id):
            for i in range(max_id):
                for j in range(data_center_num):
                    if constant_completime[k][i][j]<= 0.:
                        continue
                    constraints1 = variable_x[k][i][j] == variable_lambda1[k][i][j] 
                    constraints2 = (variable_lambda0[k][i][j] + variable_lambda1[k][i][j])==1
                     
                    problem += constraints1
                    problem += constraints2

        for j in range(data_center_num):
            
            constraints3 = lp.lpSum([variable_x[k][i][j] for k in range(max_job_id) for i in range(max_id)])<=constant_slot[j]   
            problem += constraints3

        for k in range(max_job_id):
            for i in range(max_id):
                if constant_completime[k][i].sum()<= 0.:
                    continue
                constraints4 = lp.lpSum([variable_x[k][i][j] for j in range(data_center_num)])==1
                problem += constraints4

        
        ## Enter the loop solution of LP
        while(job_num_all!=0):
            
            if job_num_all != 1:
                problem.solve(lp.PULP_CBC_CMD(msg =False))
            else:
                problem.solve(lp.PULP_CBC_CMD(msg =False))
           

            """
            We have solved LP, then move and into next LP
            """

            # get the argmax value of x
            pha_max = 0
            idx_k = 0
            idx_i = 0
            idx_j = 0
            for k in range(max_job_id):
                for i in range(max_id):
                    for j in range(data_center_num):
                        if isinstance(variable_x[k][i][j], np.float64) or isinstance(variable_x[k][i][j], int) or isinstance(variable_x[k][i][j], float):
                            continue
                        if variable_x[k][i][j].varValue !=0:
                            pha = variable_x[k][i][j].varValue * (constant_extime[k][i][j] + constant_completime[k][i][j])
                            if pha > pha_max:
                                pha_max = pha
                                idx_k = k
                                idx_i = i
                                idx_j = j

            fixed_job_id = idx_k
            # print("Have fixed job:", fixed_job_id)
            job_num_all -= 1 # minus 1

            # update the final result: two matrix
            for i in range(max_id):
                for j in range(data_center_num):
                    if isinstance(variable_x[fixed_job_id][i][j], int):
                        self.finishtime_matrix[idx_k][i][j] = 0
                    else:
                        self.finishtime_matrix[idx_k][i][j] = variable_x[fixed_job_id][i][j].varValue * (constant_extime[k][i][j] + constant_completime[k][i][j])

                    if isinstance(variable_x[fixed_job_id][i][j], int):
                        self.placement_matrix[idx_k][i][j] = 0
                    else:
                        self.placement_matrix[idx_k][i][j] = variable_x[fixed_job_id][i][j].varValue


            # fix and add new constraint
            
            for i in range(max_id):
                for j in range(data_center_num):
                    variable_x[fixed_job_id][i][j] = self.placement_matrix[fixed_job_id][i][j]
                    # new_constraint = (variable_x[fixed_job_id][i][j] == self.placement_matrix[fixed_job_id][i][j])
                    # problem += new_constraint

        print("Linear Programming Status:", lp.LpStatus[problem.status])    
                  
        

    def get_placement(self, task_set_list, data_center_dict):
        """
        Return: Placement Matrix, Finish Time Matrix
        """
        self.formulate_LP(task_set_list, data_center_dict)
        return self.placement_matrix, self.finishtime_matrix


    def update_datacenter(self, placement_matrix, task_set_list_new, task_set_list_old, data_center_dict, slot_change=0):
        """
        After one iteration, data center will remain some task in slot.
        Thus, we need to update the data center dict
        """
        # get which task needs to be remained
        require_tasks = []
        for task in task_set_list_new:
            require_datas = list(task.data_dict.keys())
            for data in require_datas:
                if 't' in data:
                    require_tasks.append(data)
                   

        # get the placement of these tasks
        require_tasks = list(set(require_tasks)) # delete the repeated !!!
        max_id = placement_matrix.shape[1]
      
        for task in require_tasks:
            job_id = ord(task[1]) - ord('A')
            task_id = int(task[2]) - 1
            
            slot_id = None
            for j in range(placement_matrix.shape[2]):
                if placement_matrix[job_id][task_id][j]==1:
                    slot_id = j
                    break
            if slot_id is None:
                continue
            DC = 'DC' + str(slot_id+1)
            data_center_dict[DC].data_list.append(task) 

        return data_center_dict

                   

   


if __name__=='__main__':
    task_scheduler = TaskScheduler()
    task_set = task_scheduler.get_taskset_jobbased(0)
    task_set_new = task_scheduler.get_taskset_jobbased(1)
    data_center = task_scheduler.get_datacenter()

    solver = Solver()
    placement, finish_time = solver.get_placement(task_set, data_center)
    new_dc_dict = solver.update_datacenter(placement, task_set_new, task_set, data_center)
    print(placement)
    placement, finish_time = solver.get_placement(task_set_new, new_dc_dict)
    
    task_set_new = task_scheduler.get_taskset()

    

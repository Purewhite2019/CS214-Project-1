from task_scheduler import TaskScheduler
from DAG_scheduler import DAGScheduler
from data_loader import DataLoader
import pulp as lp
import numpy as np

class Solver:
    def __init__(self, file_path="../ToyData.xlsx"):
       self.task_scheduler = TaskScheduler(file_path)
       

    def formulate_LP(self, task_set_list, data_center_dict):
        """
        TODO: need to change data center num into max id of data center?
        """
        data_center_num = 0
        for key in data_center_dict.keys():
            data_center_num += 1
        task_num_all = len(task_set_list)

        # M
        bigM = data_center_num * task_num_all


        # divide task by job
        job_num_all = 0
        job_list = []
        for i in range(len(task_set_list)):
            task_name = task_set_list[i].task_name
            job = task_name[1]
            if job not in job_list:
                job_list.append(job)
                job_num_all += 1

        # get max num of  task of one job
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
        # print(task_num_max)

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
                    raise "Error: can't find such data in any data center"
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
                        continue
                    constant_exponetial[k][i][j] = np.exp(constant_extime[k][i][j] + constant_completime[k][i][j])


        """
        for now, we have several constants
        then we can solve LP problem
        """

        # define problem
        problem = lp.LpProblem(name='Max-Min-Fairness', sense=lp.LpMinimize)

        # add variable
        variable_name = ['x_kij', 'lambda_kij0', 'lambda_kij1']
        ## one way
        variable_x = [[[lp.LpVariable('x%d%d%d'%(k,i,j), cat='Binary') for j in range(data_center_num) ] for i in range(max_id) ]for k in range(max_job_id)]
        variable_lambda0 = [[[lp.LpVariable('lambda0%d%d%d'%(k,i,j), cat='Binary')for j in range(data_center_num) ] for i in range(max_id) ]for k in range(max_job_id)]
        variable_lambda1 = [[[lp.LpVariable('lambda1%d%d%d'%(k,i,j), cat='Binary') for j in range(data_center_num) ] for i in range(max_id) ]for k in range(max_job_id)]
        print(len(variable_lambda1))
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
        print(variable_lambda0[0][0][0])
        objective = lp.lpSum([variable_lambda0[k][i][j] + variable_lambda1[k][i][j] * constant_exponetial[k][i][j] for k in range(max_job_id) for i in range(max_id) for j in range(data_center_num)])
        problem += objective

        # add constraint

        for k in range(max_job_id):
            for i in range(max_id):
                for j in range(data_center_num):
                    constraints1 = variable_x[k][i][j] == variable_lambda1[k][i][j] 
                    constraints2 = (variable_lambda0[k][i][j] + variable_lambda1[k][i][j])==1
                     
                    problem += constraints1
                    problem += constraints2

        for j in range(data_center_num):
            constraints3 = lp.lpSum([variable_x[k][i][j] for k in range(max_job_id) for i in range(max_id)])<=constant_slot[j]   
            problem += constraints3

        for k in range(max_job_id):
            for i in range(max_id):
                constraints4 = lp.lpSum([variable_x[k][i][j] for j in range(data_center_num)])==1
                problem += constraints4

        problem.solve()
        print("Status:", lp.LpStatus[problem.status])



if __name__=='__main__':
    task_scheduler = TaskScheduler()
    task_set = task_scheduler.get_taskset()
    data_center = task_scheduler.get_datacenter()

    solver = Solver()
    solver.formulate_LP(task_set, data_center)
       
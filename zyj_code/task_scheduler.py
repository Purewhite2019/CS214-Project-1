import numpy as np
from DAG_scheduler import DAGScheduler
from data_loader import DataLoader

class TaskScheduler:
    def __init__(self, file_path="../ToyData.xlsx", threshold=5):
        dag_scheduler = DAGScheduler(file_path)
        data_loader = DataLoader(file_path)
        # depth based task set
        self.task_set_dict = dag_scheduler.task_sets
        self.data_center_dict = data_loader.create_datacenter()
        self.data_center_dict_modified = self.data_center_dict
        self.threshold = threshold
        max_depth = 0
        for key in self.task_set_dict.keys():
            for i in range(len(self.task_set_dict[key])):
                self.task_set_dict[key][i].depth = key
            if key > max_depth:
                max_depth = key
        self.max_depth = max_depth

        # job based task set
        self.task_set_dict_jobbased = self.job_based_task(self.task_set_dict, \
                                            depth_based=True)
        self.task_set_dict_stepbased = self.jobbased_division(self.task_set_dict_jobbased, self.threshold)
        
    
    def job_based_task(self, task_set_dict, depth_based=True):
        """
        Construct a new task dict based on different job
        We can still add depth based tasks in job.
        """
        task_set_dict_jobbased = dict()

        for depth in task_set_dict.keys():
            task_list = task_set_dict[depth]
            for task in task_list:
                job_belong = task.task_name[1]
                if job_belong in task_set_dict_jobbased:
                    task_set_dict_jobbased[job_belong].append(task)
                else:
                    task_set_dict_jobbased[job_belong] = []
                    task_set_dict_jobbased[job_belong].append(task)
       
        if depth_based:
            for job_name in task_set_dict_jobbased.keys():
                task_list = task_set_dict_jobbased[job_name]
                task_set_dict_jobbased[job_name] = dict()
                for task in task_list:
                    depth = task.depth
                    
                    if depth in task_set_dict_jobbased[job_name]:
                        task_set_dict_jobbased[job_name][depth].append(task)
                    else:
                        task_set_dict_jobbased[job_name][depth] = []
                        task_set_dict_jobbased[job_name][depth].append(task)
        
        return task_set_dict_jobbased


    def get_taskset(self, depth=0, threshold=5):
        """
        Temporaliy use different depth set
        """
        if depth > self.max_depth:
            raise Exception("Error: Depth Beyond.")
        if len(self.task_set_dict[depth]) <= threshold:
            return self.task_set_dict[depth]
        else:
            return self.task_set_dict[depth]
    
    def jobbased_division(self, job_based_task_dict, threshold=5):
        task_division_dict = dict()
        job_num = len(job_based_task_dict.keys())
        step_all = np.zeros(job_num, dtype=np.int)
        cur_id = 0
        count = 0
        
        finish = np.zeros(job_num)
        while(finish.sum()!=job_num):
            for j in range(job_num):
                job_name = chr(ord('A')+j)
                job_step = int(step_all[j])
                if job_step >= len(job_based_task_dict[job_name].keys()):
                    finish[j] = 1
                    
                    continue
                task_list = job_based_task_dict[job_name][job_step]
                if count + len(task_list) < threshold:
                    if cur_id in task_division_dict:
                        task_division_dict[cur_id].extend(task_list)
                        count += len(task_list)
                        step_all[j] += 1
                    else:
                        task_division_dict[cur_id] = []
                        task_division_dict[cur_id].extend(task_list)
                        count += len(task_list)
                        step_all[j] += 1
                else:# reach threshold, into next state
                    count = 0
                    cur_id += 1
                    break
                if j==job_num-1:# not reach threshold, but reach end, into next state
                    count = 0
                    cur_id += 1
                    break 

        self.max_step = cur_id-1
        
        return task_division_dict


    def get_taskset_jobbased(self, step=0):
        """
        Return one step's task set
        """
        return self.task_set_dict_stepbased[step]
        


    def get_datacenter(self):
        return self.data_center_dict_modified
    
    def update_datacenter(self, placement_matrix, task_set_list):
        """
        update data center, after one iteration
        """
        for task in task_set_list:
            print(task)
        



    
    
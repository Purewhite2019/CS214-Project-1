import numpy as np
import pandas as pd
class TASK:
    """
    Include: task name, data dict
            data dict is like: {'A1':100, 'A2':50}
    Note: You can simply call print to display them
    Author: Yanjie Ze
    """
    def __init__(self, task_name, data_dict=None):
        self.task_name = task_name
        self.execution_time = None
        if data_dict is not None:
            self.data_dict = data_dict
        else:
            self.data_dict = dict()
    
    def add_data(self, new_data_name, new_data_num):
        self.data_dict[new_data_name] = new_data_num

    def add_execution_time(self, execution_time):
            self.execution_time = execution_time
    
    def __str__(self):
        names = []
        for name in self.data_dict.keys():
            names.append(name)
        return "Task %s, Execution Time %u, need data: %s"%(self.task_name, self.execution_time, names)


class JOB:
    """
    Job, include: dict of task
    Author: Yanjie Ze
    """
    def __init__(self, job_name, task_dict=None):
        self.job_name = job_name
        if task_dict is not None:
            self.task_dict = task_dict
        else:
            self.task_dict = dict()
    
    def add_task(self, new_task_name, new_task):
        self.task_dict[new_task_name] = new_task

    def __str__(self):
        task_name = self.task_dict.keys()
        names = []
        for name in task_name:
            names.append(name)
        return "Job %s, with tasks: %s"%(self.job_name, names)



class DataLoader:
    """
    Load Toy Data. 
    Note that this only works for Toy Data.

    Author: Yanjie Ze
    """
    def __init__(self, file_path="../ToyData.xlsx"):
        self.file_path = file_path
        self.job_name_list = ['A', 'B', 'C','D','E','F']
        self.data_name_list = ['A1','A2','B1','B2','tB1','C1','C2','tC1','tC2','D1','D2','D3','tD1','tD2', 'tD3', 'E1',\
         'E2','E3','E4','tE1','tE2','tE3','tE5','F1','F2','F3','F4','F5','tF1','tF2','tF3','tF4','tF5','tF6','tF7','tF8']
        self.task_name_list = ['tA1','tA2','tB1','tB2','tC1','tC2','tC3','tD1','tD2','tD3',\
            'tD4','tD5','tE1','tE2','tE3','tE4','tE5','tE6','tF1','tF2','tF3','tF4','tF5','tF6','tF7','tF8','tF9']
    
    def read_data_all(self):
        """
        read data from excel
        """
        self.data_bandwidth = pd.read_excel(self.file_path, sheet_name='Inter-Datacenter Links')
        self.data_joblist = pd.read_excel(self.file_path, sheet_name='Job List')
        self.data_datacenter = pd.read_excel(self.file_path, sheet_name='Data Center Details')

    def create_job_dict(self):
        """
        Return: job dict, task dict
        """
        data_joblist = pd.read_excel(self.file_path, sheet_name='Job List')
        task_num = data_joblist.shape[0]

        # create job dict
        job_dict = dict()
        for job_name in self.job_name_list:
            job_dict[job_name]= JOB(job_name=job_name)
        

        # create task dict
        task_dict = dict()
        for task_name in self.task_name_list:
            task_dict[task_name] = TASK(task_name=task_name)


        # add execution time into task
        for i in range(len(self.task_name_list)):
            task_name = self.task_name_list[i]
            task_dict[task_name].add_execution_time(data_joblist['Execution Time (s)'][i])

        # get data into task dict    
        for i in range(len(self.data_name_list)):
            data_name = self.data_name_list[i] # Column Name
            for j in range(len(self.task_name_list)): 
                task_name = self.task_name_list[j] # Row Name
                data_num = data_joblist[data_name][j]
                if pd.isnull(data_num) is not True: # exclude "nan"
                    task_dict[task_name].add_data(new_data_name=data_name,\
                                                    new_data_num=data_num)

        # get task into job dict                
        for task_name in task_dict.keys():
            job_name_belong_to = task_name[1]
            job_dict[job_name_belong_to].add_task(task_name, task_dict[task_name])

        print("Create_job_dict() finish, return job dict and task dict.")
        return job_dict, task_dict


if __name__=='__main__':
    data_loader = DataLoader()
    job_dict, task_dict = data_loader.create_job_dict()


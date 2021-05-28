"""
File Function: Interpret Toy Data
Author: Yanjie Ze
Date: May 20, 2021
"""
import numpy as np
import pandas as pd

class TASK:
    """
    Include: task name, data dict
            data dict is like: {'A1':100, 'A2':50}
    Note: You can simply call print to display
    """
    def __init__(self, task_name, data_dict=None):
        self.task_name = task_name
        self.execution_time = None
        if data_dict is not None:
            self.data_dict = data_dict
        else:
            self.data_dict = dict()
        self.precedence = None
        self.depth = None
    
    def add_data(self, new_data_name, new_data_num):
        self.data_dict[new_data_name] = new_data_num

    def add_execution_time(self, execution_time):
        self.execution_time = execution_time
    
    def add_precedence(self, pre_task):
        self.precedence = pre_task

    def __str__(self):
        names = []
        for name in self.data_dict.keys():
            names.append(name)
        return "Task %s, Execution Time %u, need data: %s"%(self.task_name, self.execution_time, names)


class JOB:
    """
    Job, include: dict of task
    Note: You can simply call print to display
     
    """
    def __init__(self, job_name, task_dict=None):
        self.job_name = job_name
        if task_dict is not None:
            self.task_dict = task_dict
        else:
            self.task_dict = dict()
        self.DAG = None
        self.graph_matrix = None
        self.task_num = None
        self.depth_vector = None

    def add_task(self, new_task_name, new_task):
        self.task_dict[new_task_name] = new_task

    def __str__(self):
        task_name = self.task_dict.keys()
        names = []
        for name in task_name:
            names.append(name)
        return "Job %s, with tasks: %s, with DAG: %s"%(self.job_name, names, self.DAG)

    def add_DAG(self, DAG):
        self.DAG = DAG
    
    def update_tasknum(self):
        self.task_num = len(self.task_dict.keys())
    
    def create_graphmatrix(self):
        self.graph_matrix = np.zeros((self.task_num, self.task_num),dtype=np.int)
        self.depth_vector = np.ones(self.task_num, dtype=np.int)*(-1)

class DataCenter:
    """
    Include: Num of slots, Data, bandwidth
     
    """
    def __init__(self, dc_name, slot_num):
        self.dc_name = dc_name
        self.slot_num = slot_num
        self.data_list = []
        self.link_dict = dict()
    
    def __str__(self):
        links = []
        for i in self.link_dict.keys():
            links.append(i)
        return "Data Center %s, slot num=%u, has data:%s, has link to:%s"%(self.dc_name, self.slot_num, self.data_list ,links)

    def add_data(self, data_name):
        self.data_list.append(data_name)
    
    def add_link(self, destination, bandwidth):
        self.link_dict[destination] = bandwidth

class DataLoader:
    """
    Load Toy Data. 
    Note: this only works for Toy Data.
     
    """
    def __init__(self, file_path="../ToyData.xlsx"):
        self.file_path = file_path
        self.job_name_list = ['A', 'B', 'C','D','E','F']
        
        self.data_name_list = ['A1','A2','B1','B2','tB1','C1','C2','tC1','tC2','D1','D2','D3','tD1','tD2', 'tD3', 'E1',\
        'E2','E3','E4','tE1','tE2','tE3','tE5','F1','F2','F3','F4','F5','tF1','tF2','tF3','tF4','tF5','tF6','tF7','tF8']
        self.task_name_list = ['tA1','tA2','tB1','tB2','tC1','tC2','tC3','tD1','tD2','tD3',\
            'tD4','tD5','tE1','tE2','tE3','tE4','tE5','tE6','tF1','tF2','tF3','tF4','tF5','tF6','tF7','tF8','tF9']
        # elif file_path=='../GeneratedData.xlsx' or file_path=='GeneratedData.xlsx':
        #     self.data_name_list = ['A1','A2','B1','B2','tB1','C1','C2','tC1','tC2','D1','D2','D3','tD1','tD2', 'tD3', 'E1',\
        #     'E2','E3','E4','tE1','tE2','tE3','tE5','F1','F2','F3','F4','F5','tF1','tF2','tF3','tF4','tF5','tF6','tF7','tF8']
        #     self.task_name_list = ['tA1','tA2','tB1','tB2','tC1','tC2','tC3','tD1','tD2','tD3',\
        #         'tD4','tD5','tE1','tE2','tE3','tE4','tE5','tE6','tF1','tF2','tF3','tF4','tF5','tF6',\
        #         'tF7','tF8','tF9', 'tG1','tG2', 'tG3','tG4','tG5','tG6', 'tG7','tG8', 'tG9']
   
    def read_data_all(self):
        """
        read data from excel
        (Demo)
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

        # add DAG relation
        job_dict = self.create_DAG(job_dict)

        return job_dict, task_dict

    def create_datacenter(self):
        """
        return data center dict
        """

        data_datacenter = pd.read_excel(self.file_path, sheet_name='Data Center Details')

        # create data center dict, add slot num
        data_center_dict = dict()
        for i in range(len(data_datacenter['DC'])):
            dc = data_datacenter['DC'][i]
            slot_num = data_datacenter['Num of Slots'][i]
            if pd.isnull(dc):
                continue
            data_center_dict[dc] = DataCenter(dc_name=dc, slot_num=slot_num)
    

        # add data of each data center
        for i in range(len(data_datacenter['Data Partition'])):
            data_name = data_datacenter['Data Partition'][i]
            location = data_datacenter['Location'][i]
            data_center_dict[location].add_data(data_name)

        # read file
        data_bandwidth = pd.read_excel(self.file_path, sheet_name='Inter-Datacenter Links')
        
        # add bandwidth
        center_num = 0
        for dc in data_bandwidth['Bandwidth/MBps']:
            if pd.isnull(dc):
                continue
            center_num += 1

        for i in range(len(data_bandwidth['Bandwidth/MBps'])):
            dc = data_bandwidth['Bandwidth/MBps'][i]
            if pd.isnull(dc):
                continue
            for j in range(center_num):
                bandwidth = data_bandwidth.loc[i][j+1]
                dest = data_bandwidth.loc[j][0]
                if bandwidth != '-':
                    data_center_dict[dc].add_link(destination=dest, bandwidth=bandwidth)
        
        
        return data_center_dict


    def create_DAG(self, job_dict):
        """
        Add DAG relation into job dict
        """

        data_joblist = pd.read_excel(self.file_path, sheet_name='Job List')
        for i in range(len(data_joblist['Precedence Constraint'])):
            relation = data_joblist['Precedence Constraint'][i]
            correspond_job = data_joblist['Job / Required Data amount (MB)'][i]
            if pd.isnull(relation) is True:
                continue
            job_dict[correspond_job].add_DAG(relation)
        
        return job_dict

if __name__=='__main__':
    data_loader = DataLoader()
    # # demo 1
    # job_dict, task_dict = data_loader.create_job_dict()

    # # demo 2
    # data_center_dict = data_loader.create_datacenter()

    # demo 3
    job_dict, task_dict = data_loader.create_job_dict()
    print(job_dict['B'])



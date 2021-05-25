import numpy as np
from DAG_scheduler import DAGScheduler
from data_loader import DataLoader

class TaskScheduler:
    def __init__(self, file_path="../ToyData.xlsx"):
        dag_scheduler = DAGScheduler(file_path)
        data_loader = DataLoader(file_path)
        self.task_set_dict = dag_scheduler.task_sets
        self.data_center_dict = data_loader.create_datacenter()
    
    def task_assignment(self, threshold):
        pass

    def data_center_update(self):
        pass

    def get_taskset(self, depth=0):
        """
        Temporaliy use different depth set
        """
        return self.task_set_dict[depth]

    def get_datacenter(self):
        return self.data_center_dict

    
    
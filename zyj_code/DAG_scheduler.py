from data_loader import DataLoader

class DAGScheduler:
    """
    DAG Scheduler
    """
    def __init__(self, file_path="../ToyData.xlsx"):
        data_loader = DataLoader(file_path)
        self.job_dict, self.task_dict= data_loader.create_job_dict()

    def task_allocation(self):
        pass


    
    
       
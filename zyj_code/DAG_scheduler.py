from data_loader import DataLoader
import numpy as np



class DAGScheduler:
    """
    DAG Scheduler
    """
    def __init__(self, file_path="../ToyData.xlsx"):
        data_loader = DataLoader(file_path)
        self.job_dict, self.task_dict= data_loader.create_job_dict()

        for key in self.job_dict.keys():
            self.job_dict[key].update_tasknum()
            self.job_dict[key].create_graphmatrix()
            #print(self.job_dict[key].graph_matrix)

        # get adj matrix
        self.update_DAG()

        # get Depth for each task
        for key in self.job_dict.keys():
            self.BFS_mark(key)

        self.task_sets = self.taskset_collection()

    def update_DAG(self):
        """
        Parse DAG, using adjacent matrix
        """
        for job_name in self.job_dict.keys():
            job = self.job_dict[job_name]
            DAG = job.DAG.split('(')
            DAG.pop(0)
            if len(DAG)<=0:
                continue
            for i in range(len(DAG)):
                relation = DAG[i].split(',')
                start = int(relation[0][2])
                end = int(relation[1][2])
                job.graph_matrix[start-1][end-1] = 1
           

    def BFS_mark(self, job_name):
        """
        Use BFS to mark the tasks in job, give depth to each task
        """
        gmatrix = self.job_dict[job_name].graph_matrix
    
        cur_depth = 0
        for i in range(gmatrix.shape[0]):
            # get current node's depth, or update it from -1 to 0
            if(self.job_dict[job_name].depth_vector[i]==-1):
                self.job_dict[job_name].depth_vector[i] = cur_depth
            else:
                cur_depth = self.job_dict[job_name].depth_vector[i]
            # update others
            for j in range(gmatrix.shape[1]):
                if gmatrix[i][j]==1:
                    if self.job_dict[job_name].depth_vector[j] < cur_depth + 1:
                        self.job_dict[job_name].depth_vector[j] = cur_depth + 1
    
        
    def taskset_collection(self):
        """
        Divide all tasks by set
        """
        task_sets = dict()
        depth_init = np.zeros(20)
        for key in self.job_dict.keys():
            cur_job = self.job_dict[key]
            for task_name in cur_job.task_dict.keys():
                cur_task = cur_job.task_dict[task_name]
                task_id = int(task_name[2])-1
                task_depth = cur_job.depth_vector[task_id]
                if depth_init[task_depth]==1:
                    task_sets[task_depth].append(cur_task)
                else:
                    task_sets[task_depth] = []
                    depth_init[task_depth] = 1
                    task_sets[task_depth].append(cur_task) 
             
        return task_sets
    
    def get_taskname(self, job_name, task_id):
        pass
        
        

        

if __name__=='__main__':
    scheduler = DAGScheduler()
    
    
    
       
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from matplotlib.collections import LineCollection


def get_data(file1='jobbased_baseline.txt', file2='depthbased_baseline.txt'):
    f1 = open(file1, 'r')
    f2 = open(file2, 'r')

    jobbased_x = np.zeros(8)
    jobbased_y = np.zeros(8)
    for i in range(8):
        line = f1.readline()
        line = line.split(' ')
        cost_time = float(line[len(line)-1].split('\n')[0])
        jobbased_x[i] = i
        jobbased_y[i] = cost_time
        if i==7:
            jobbased_finish_y = np.array(cost_time)
            jobbased_finish_x = np.array(7)
    
    depthbased_x = np.zeros(5)
    depthbased_y = np.zeros(5)
    for i in range(5):
        line = f2.readline()
        line = line.split(' ')
        cost_time = float(line[len(line)-1].split('\n')[0])
        depthbased_x[i] = i
        depthbased_y[i] = cost_time
        if i==4:
            depthbased_finish_y = np.array(cost_time)
            depthbased_finish_x = np.array(4)
    f1.close()
    f2.close()

        
        

def draw_completion_time(file1='jobbased_baseline.txt', file2='depthbased_baseline.txt', y_high=15.5, figure_name='./comparison.png'):
    """
    Draw graph: Completion Time of Each Collection
    """
    global jobbased_finish_x
    global jobbased_finish_y
    global jobbased_x
    global jobbased_y
    global depthbased_finish_x
    global depthbased_finish_y
    global depthbased_y
    global depthbased_x

    # # baseline
    # jobbased_x = np.array([0,1,2,3,4,5,6,7])
    # jobbased_y = np.array([4.5, 10, 3.53, 4.25, 3.08, 1.575, 2.75, 3.667])
    # jobbased_finish_x = np.array(7)
    # jobbased_finish_y = np.array(3.667)
    # # SGD
    # depthbased_x = np.array([0,1,2,3,4])
    # depthbased_y = np.array([5.0, 5.0, 6.0, 2.75, 3.667])
    # depthbased_finish_x = np.array(4)
    # depthbased_finish_y = np.array(3.667)
    # def get_data():
    f1 = open(file1, 'r')
    f2 = open(file2, 'r')

    jobbased_x = np.zeros(8)
    jobbased_y = np.zeros(8)
    for i in range(8):
        line = f1.readline()
        line = line.split(' ')
        cost_time = float(line[len(line)-1].split('\n')[0])
        jobbased_x[i] = i
        jobbased_y[i] = cost_time
        if i==7:
            jobbased_finish_y = np.array(cost_time)
            jobbased_finish_x = np.array(7)
        
    depthbased_x = np.zeros(5)
    depthbased_y = np.zeros(5)
    for i in range(5):
        line = f2.readline()
        line = line.split(' ')
        cost_time = float(line[len(line)-1].split('\n')[0])
        depthbased_x[i] = i
        depthbased_y[i] = cost_time
        if i==4:
            depthbased_finish_y = np.array(cost_time)
            depthbased_finish_x = np.array(4)
    f1.close()
    f2.close()

   
    plt.plot(jobbased_x, jobbased_y, lw=2, color='red', alpha=0.7, label='Baseline')
    plt.plot(depthbased_x, depthbased_y, lw=2, color='blue', alpha=0.7, label='SGD')
    plt.xlabel('Depth or Step')
    plt.grid()
    plt.xlim([0,7])
    plt.ylim([0,y_high])
    plt.ylabel('Time Cost/s')
    plt.scatter(depthbased_finish_x, depthbased_finish_y, c='blue', marker='*', s=30)
    plt.text(depthbased_finish_x-0.5, depthbased_finish_y+0.2, 'finish point', c='blue')
    
    plt.scatter(jobbased_finish_x, jobbased_finish_y, c='red', marker='*', s=30)
    plt.text(jobbased_finish_x-0.5, jobbased_finish_y+0.2, 'finish point', c='red')
    
    plt.fill_between(jobbased_x, jobbased_y, facecolor='red', alpha=0.3)
    plt.fill_between(depthbased_x, depthbased_y, facecolor='blue', alpha=0.3)
    plt.legend()
    plt.title('Completion Time of Each Collection')
    plt.savefig(figure_name)
    plt.show()


def draw_extime():
    x = np.array([1.5,1.5,2.5,1,4,1,2,2,2,1.5,1,1,4,2,3,2,1,3,4,2,1,3,1,1.5,2.5,2,3.5])
    mean = np.mean(x)
    variance = np.var(x)
    plt.grid()
    map_vir = cm.get_cmap(name='viridis')
    color = map_vir(x)
    plt.hist(x, color='purple', alpha=0.6, label='Execution Time')
    plt.legend()
    plt.title('Occurrence of Different Execution Time')
    plt.ylabel('Occurrence')
    plt.xlabel('Execution Time/s')
    plt.savefig('./extime.png')
    plt.show()
    

if __name__=='__main__':

    # draw_completion_time()
    # draw_extime()
   
    draw_completion_time(figure_name='./comparison9.png')

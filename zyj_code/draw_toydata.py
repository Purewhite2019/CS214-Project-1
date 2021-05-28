import matplotlib.pyplot as plt
import numpy as np
# baseline
jobbased_x = np.array([0,1,2,3,4,5,6,7])
jobbased_y = np.array([4.5, 10, 3.53, 4.25, 3.08, 1.575, 2.75, 3.667])
jobbased_finish_x = np.array(7)
jobbased_finish_y = np.array(3.667)
# SGD
depthbased_x = np.array([0,1,2,3,4])
depthbased_y = np.array([5.0, 5.0, 6.0, 2.75, 3.667])

def draw_completion_time():
    plt.plot(jobbased_x, jobbased_y, lw=2, color='red', alpha=0.7, label='Baseline')
    plt.plot(depthbased_x, depthbased_y, lw=2, color='blue', alpha=0.7, label='SGD')
    plt.xlabel('Depth or Step')
    plt.grid()
    plt.xlim([0,7])
    plt.ylim([0,10.5])
    plt.ylabel('Time Cost/s')
    plt.scatter(4, 3.667, c='blue', marker='*', s=30)
    plt.text(4-0.5, 3.667+0.2, 'finish point', c='blue')
    
    plt.scatter(jobbased_finish_x, jobbased_finish_y, c='red', marker='*', s=30)
    plt.text(jobbased_finish_x-0.5, jobbased_finish_y+0.2, 'finish point', c='red')
    
    plt.fill_between(jobbased_x, jobbased_y, facecolor='red', alpha=0.3)
    plt.fill_between(depthbased_x, depthbased_y, facecolor='blue', alpha=0.3)
    plt.legend()
    plt.title('Completion Time of Each Collection')
    plt.savefig('./comparison.png')
    plt.show()
    
    

if __name__=='__main__':
    draw_completion_time()

import random

def execution_time_generator(num=27, low=0.1, high=15, mean=10, variance=6):
    """
    Gaussian Generation
    """
    i = 0
    f = open('random_extime.txt', 'w')
    while(i<num):     
        number = random.uniform(mean, variance)
        if number<low or number>high:
            
            continue
        i += 1
        number = str(number)
        f.write(number+'\n')
        print(number)
    f.close()

if __name__=='__main__':
    execution_time_generator()

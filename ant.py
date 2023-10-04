import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt
import time

def win_condition(coord,problem=1):
    global lost_ant
    x = coord[0]
    y = coord[1]
    if problem == 1:
        if abs(x) == 2 or abs(y) == 2:
            return True
    elif problem == 2:
        if x+y == 1:
            return True
        elif x+y < -100:
            lost_ant += 1
            return True
    else:
        if ((x-0.25)/3)**2 + ((y-0.25)/4)**2 >= 1:
            return True
    return False

def optiver_ds_ant_prob(prob_num=1, trial_num=100000):
    global lost_ant
    lost_ant=0
    start_time = time.time()
    print()
    print('Problem {}:'.format(prob_num))
    axes = ['X','Y']
    directions = [1,-1]
    pathlengths = []
    final_coord = []
    lost_ant=0
    trials = trial_num

    for i in range(trials):
        cur_coordinates = [0,0]
        path = []
        count = 0
        while True:
            axis = axes[np.random.randint(0,2)]
            if axis == 'X':
                direction = directions[np.random.randint(0,2)]
                cur_coordinates[0] += direction
                #print(cur_coordinates)
                count += 1
                if win_condition(cur_coordinates, prob_num):
                    break
            else:
                direction = directions[np.random.randint(0,2)]
                cur_coordinates[1] += direction
                #print(cur_coordinates)
                count += 1
                if win_condition(cur_coordinates, prob_num):
                    break
        #print(count)
        pathlengths.append(count)
        final_coord.append(cur_coordinates)

    print('Average Steps:',np.mean(pathlengths))
    if prob_num == 2:
        print('Lost Ant Rate:', lost_ant/trials)

    coord_counts = defaultdict(int)
    for coord in final_coord:
        coord_tuple = tuple(coord)
        coord_counts[coord_tuple] += 1
    coord_counts = list(coord_counts.items())
    coord_counts = sorted(coord_counts, key=lambda x: (-x[1], x[0][0], x[0][1]))
    other_results = 0
    other_counts = 0
    # Print the counts
    for coord_count in coord_counts:
        coord, count = coord_count
        if count > trial_num/1000:
            print(f"{coord}: {count} times")
        else:
            other_results += 1
            other_counts += count
    if other_results != 0:
        print('...and {} more ({}% of cases)'.format(other_results,round(100*other_counts/trial_num,3)))

    plt.hist(pathlengths, bins=np.arange(0, 52, 1), edgecolor='black')
    plt.xlabel('Number of Steps')
    plt.ylabel('Absolute Frequency')
    plt.title('Number of Steps Before Honey')
    plt.xlim(0, 50)
    current_ticks = plt.gca().get_yticks()
    new_ticks = [tick / trials for tick in current_ticks]
    plt.gca().set_yticks(current_ticks)
    plt.gca().set_yticklabels(new_ticks)
    plt.show()
    end_time = time.time()
    execution_time = end_time - start_time
    return execution_time

t1 = optiver_ds_ant_prob(1)
t2 = optiver_ds_ant_prob(2)
t3 = optiver_ds_ant_prob(3)
print()
print('Q1:',t1, 'seconds')
print('Q2:',t2, 'seconds')
print('Q3:',t3, 'seconds')
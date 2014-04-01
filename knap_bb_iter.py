import sys
import cProfile
from collections import namedtuple
Item = namedtuple("Item", ['index', 'value', 'weight'])

best = 0
best_conf = []
full_capacity = 0
item_weights = []

def solve_it(input_data):
    # Modify this code to run your optimization algorithm
    global item_weights
    global best_conf

    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    orig_items = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        orig_items.append(Item(i-1, int(parts[0]), int(parts[1])))

    items = sorted(orig_items, key = lambda x: float(x.value)/float(x.weight), reverse = True)

    # a trivial greedy algorithm for filling the knapsack
    # it takes items in-order until the knapsack is full
    value = 0
    weight = 0


    #cur_val = 0
    item_weights = map(lambda x: x.weight, items)
    #decide(items, taken, skipped, 0, capacity, cur_val, prev_oe)

    # prepare the solution in the specified output format
    result_presorted = best_conf
    result = [x for (y, x) in sorted(zip(map(lambda x: x.index, items), result_presorted))]
    print best == current_val(items, best_conf)
    output_data = str(best) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, result))
    return output_data

def bb_iter(items, capacity):
    taken = []
    skipped = []
    lev = 0
    cap_left = capacity
    while lev < len(items):
        if cap_left - items[lev].weight >= 0:
            taken.append(items[lev])
            cap_left -= items[lev].weight
        else:
            skipped.append(items[lev])
        lev += 1


def decide(items, taken, skipped, i, capacity, cur_val, prev_oe):
    global best
    global best_conf
    global full_capacity
    global item_weights
    #cval = current_val(items, taken)
    cval = cur_val
    if i == len(items):
        if cval > best:
            best_conf = list(taken)
        best = cval if cval > best else best

        return

    min_remaining_weight = min(item_weights[i:])
    if capacity < min_remaining_weight and cval < best:
        return

    new_capacity = capacity - items[i].weight

    # if new_capacity < min_remaining_weight:
    #     return

    if new_capacity >= 0:
        taken[i] = 1
        #oe = optimistic_estimation(items, skipped, full_capacity, prev_oe, i)
        if best < prev_oe:
            cur_val += items[i].value
            decide(items, taken, skipped, i+1, new_capacity, cur_val, prev_oe)
            cur_val -= items[i].value
        # else prune

    taken[i] = 0
    skipped[i] = 1
    oe = optimistic_estimation(items, skipped, full_capacity)
    if best < oe:
        decide(items, taken, skipped, i+1, capacity, cur_val, oe)
    skipped[i] = 0
        # else prune
    # else:
    #     best = cval if cval > best else best
    #     return



def optimistic_estimation(items, skipped, capacity):
    value = 0
    weight = 0
    for i in xrange(0, len(items)):
        if skipped[i] == 0:
            if weight + items[i].weight < capacity:
                value += items[i].value
                weight += items[i].weight
            else:
                remainder = capacity - weight
                weight += remainder
                value += float(remainder) / items[i].weight * items[i].value
    # for idx, item in enumerate(items):
    #     if skipped[idx] == 0:
    #         if weight + item.weight < capacity:
    #             value += item.value
    #             weight += item.weight
    #         else:
    #             remainder = capacity - weight
    #             weight += remainder
    #             value += float(remainder) / item.weight * item.value
    return value

def current_val(items, taken):
    value = 0
    for idx, item in enumerate(items):
        if taken[idx] == 1:
            value += item.value
    return value


with open('./data/ks_4_0', 'r') as f:
    input_data = ''.join(f.readlines())
    print cProfile.run('solve_it(input_data)')
    #print solve_it(input_data)

# if __name__ == '__main__':
#     if len(sys.argv) > 1:
#         file_location = sys.argv[1].strip()
#         input_data_file = open(file_location, 'r')
#         input_data = ''.join(input_data_file.readlines())
#         input_data_file.close()
#         print solve_it(input_data)
#     else:
#         print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)'
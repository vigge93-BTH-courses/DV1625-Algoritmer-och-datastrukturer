# Shahryar Eivazzadeh, December 2020, sei@bth.se
import sys
from time import time
if (sys.version < "3.7"):
    print("Your Python version is old. It is "+sys.version+" . Upgrade to at least 3.7")
    exit()
import numpy as np
import math as math
import pandas as pd
import matplotlib.pyplot as plt
import os
import logging
import timeit
from statistics import mean, median, stdev

# some config
SPEED_FACTOR = 1
LOG_LEVEL = 'INFO'  # Also DEBUG, INFO, WARNING, ...
BASE_LIST_SIZE = 20000//SPEED_FACTOR
REMOVE_LIST_SIZE = BASE_LIST_SIZE//5
INSERTREMOVE_LIST_SIZE = BASE_LIST_SIZE + REMOVE_LIST_SIZE
LOWER_VALUE = INSERTREMOVE_LIST_SIZE*-2
HIGHER_VALUE = INSERTREMOVE_LIST_SIZE*2
BENCH_LIST_SIZE = BASE_LIST_SIZE * 100
BENCH_LOWER_VALUE = BENCH_LIST_SIZE*-2
BENCH_HIGHER_VALUE = BENCH_LIST_SIZE*2
POLLUTION_FACTOR = 10
INSERT_FLAG = 0
REMOVE_FLAG = 1
POLLUTION_FLAG = -1
# if BASE_LIST_SIZE > HIGHER_VALUE - LOWER_VALUE:
#     print('Wrong BASE_LIST_SIZE')
#     exit()
TEST_TIMES = 500//SPEED_FACTOR
GROW_STEP_SIZE = 30
newline = '\n'
tab = '\t'


directory = os.path.dirname(os.path.abspath(__file__))
log = logging.getLogger(__name__)
logging.basicConfig(filename=directory+'/test.log',  level=os.environ.get("LOGLEVEL", LOG_LEVEL), filemode='w', format='\n%(levelname)-4s [L:%(lineno)d] %(message)s', datefmt='%Y-%m-%d:%H:%M:%S')


def wrapper(func, *args, **kwargs):

    def wrapped():
        return func(*args, **kwargs)
    return wrapped


def check_functions(the_rbt):

    FUNC_LIST = ['insert', 'remove', 'search', 'path', 'min', 'max', 'bfs']

    log.info(f"{newline}Testing if the class has the required methods. ({FUNC_LIST})")
    print(f"{newline}Testing if the class has the required methods. ({FUNC_LIST})")

    for func in FUNC_LIST:
        if not hasattr(the_rbt, func):
            print(f"The class does not have {func}() function.")
            exit()

    log.info("The class has the required functions.")
    print("The class has the required functions.")
    return True


def create_base_and_remove_lists():  # they both should have none repetitive items (across both lists)

    original_list = np.random.choice(np.arange(LOWER_VALUE, HIGHER_VALUE), BASE_LIST_SIZE + REMOVE_LIST_SIZE, replace=False)
    log.info(f'Original list (size={BASE_LIST_SIZE + REMOVE_LIST_SIZE},{original_list.size}):')
    log.debug(original_list)

    base_list = original_list[:BASE_LIST_SIZE]
    log.info(f'Base list: (size={BASE_LIST_SIZE},{base_list.size}):')
    log.debug(base_list)

    remove_list = original_list[BASE_LIST_SIZE:]
    log.info(f'Remove list: (size={REMOVE_LIST_SIZE},{remove_list.size}):')
    log.debug(remove_list)

    return [base_list, remove_list]


def create_insertremove_cplist_01(base_list, remove_list):

    base_cplist = [list(item) for item in zip(base_list, [INSERT_FLAG]*BASE_LIST_SIZE)]
    log.info('base insertremove list')
    log.debug(base_cplist)

    insert_for_remove_cplist = [list(item) for item in zip(remove_list, [INSERT_FLAG]*REMOVE_LIST_SIZE)]
    remove_cplist = [list(item) for item in zip(remove_list, [REMOVE_FLAG]*REMOVE_LIST_SIZE)]
    log.info('remove insertremove list')
    log.debug(remove_cplist)

    mixed_cplist = np.random.permutation(np.concatenate((base_cplist, insert_for_remove_cplist), axis=0))
    log.info('mixed_cplist list')
    log.debug(mixed_cplist)

    insertremove_cplist = np.concatenate((mixed_cplist, np.random.permutation(remove_cplist)), axis=0)
    log.info('insertremove list')
    log.debug(insertremove_cplist)

    return insertremove_cplist


def create_insertremove_cplist(base_list, remove_list):
    return create_insertremove_cplist_01(base_list, remove_list)


def test_insertremove(the_rbt, base_list, remove_list):

    log.info(f"{newline}Testing if the class can insert and remove correctly")
    print(f"{newline}Testing if the class can insert and remove correctly")

    insert_remove_cplist = create_insertremove_cplist(base_list, remove_list)

    log.info('Insert and remove several items.')
    print('Inserting and removing several items.')
    try:
        for item in insert_remove_cplist:
            log.debug(f'For: {item}')
            if item[1] == 0:
                log.debug(f'Inserting : {item[0]}')
                the_rbt.insert(item[0])
            elif item[1] == 1:
                log.debug(f'Removing : {item[0]}')
                the_rbt.remove(item[0])
            else:
                log.error(f'ERROR : {item[0]}')
                pass
    except:
        log.error('Error in inserting or removing')
        print("Error in inserting or removing")
        exit()

    log.info('Test for existing items.')
    print('Test for existing items.')
    try:
        for item in base_list:
            log.debug(item)
            if the_rbt.search(item):
                log.debug(f'Correctly contains : {item}')
            else:
                log.error(f'ERROR does not contain: {item}')
                print(f'ERROR does not contain: {item}')
                exit()
    except:
        log.error("Error: the tree does not find the item that should be there.")
        print("Error: the tree does not find the item that should be there.")
        exit()

    log.info('Correct insertion, removal and search.')
    print('Correct insertion, removal and search.')


def test_path(the_rbt, base_list):

    log.info(f'Function test_path, (BASE_LIST_SIZE={BASE_LIST_SIZE}, actual size={len(base_list)})')
    print(f'{newline}Test paths implementation and length')

    path_lengths = []
    try:
        for i in range(BASE_LIST_SIZE):
            log.debug(f'Trying to find the path for {base_list[i]} (i={i})')
            path = the_rbt.path(base_list[i])
            if path[-1] != base_list[i]:
                log.error(f'Could not find the item in the path function ({path[-1]}!={base_list[i]}).')
                print(f'Could not find the item in the path function ({path[-1]}!={base_list[i]}).')
                exit()
            path_lengths.append(len(path)-1)
            log.info(f'length={len(path)-1} path={path}')
    except:
        log.error(f'Error in test_path, while checking finding pathes')
        print(f'Problem finding path for some item(s)')
        exit()

    log.info(f'Could find all paths')
    print(f'Could find all paths')

    path_length_min = min(path_lengths)
    path_length_max = max(path_lengths)
    log.info(f'Min path length = {path_length_min}, Max path length = {path_length_max}')
    print(f'Min path length = {path_length_min}, Max path length = {path_length_max}')
    if (2*math.log2(BASE_LIST_SIZE)<=path_length_max):
        log.error(f'Error: Max = {path_length_max} > {2*math.log2(BASE_LIST_SIZE)}')
        print(f'Error: Max = {path_length_max} > {2*math.log2(BASE_LIST_SIZE)}')
    else:
        log.info(f'Max = {path_length_max} <= {2*math.log2(BASE_LIST_SIZE)}')
        theoretical_max = math.ceil(2*math.log2(BASE_LIST_SIZE))
        print(f'Max = {path_length_max}  <= Max by theory = {theoretical_max}')

    return(path_lengths)


def create_path_length_hist(path_lengths):

    log.info(f'{newline}Creating  histogram for the path lengths')
    print(f'{newline}Creating  histogram for the path lengths')

    min_length = min(path_lengths)
    max_length = max(path_lengths)
    avg_length = mean(path_lengths)
    med_length = median(path_lengths)
    sd_length = stdev(path_lengths)
    stat_sentence = \
        f'min= {min_length} (root)' + \
        '\naverage= {:00.3}'.format(avg_length) + \
        '\nmedian= {:.0f}'.format(med_length) + \
        f'{newline}max= {max_length}' + \
        '\ntheoretical max= {:00.3}'.format(2*math.log2(BASE_LIST_SIZE)) + \
        '\nSD= {:0.3}'.format(sd_length)
    print(f'{stat_sentence} ')

    hist_plot = pd.Series(path_lengths).hist(
        grid=False,
        # bins=int(BASE_LIST_SIZE/10),
        )
    hist_plot.spines['right'].set_visible(False)
    hist_plot.spines['top'].set_visible(False)
    hist_plot.spines['left'].set_visible(False)
    hist_plot.set_title(f"Red Black Tree Path Length for {BASE_LIST_SIZE} Items")
    hist_plot.annotate(f'{stat_sentence}', xy=(1, 1),
                       xytext=(1, 1.5), xycoords=('axes fraction', 'axes fraction'), textcoords='offset points',
                       horizontalalignment='left', verticalalignment='top', fontsize='x-small', annotation_clip=False
                    )
    hist_plot.set_xlabel("Path Length (Including None Leaf Nodes)", size=12)
    hist_plot.set_ylabel("Frequency", size=12)

    plt.axvline(avg_length, color='red', linewidth=1)
    plt.annotate(f'avg: {avg_length}', xy=(avg_length, 0.7), xytext=(5, 15),
                xycoords=('data', 'axes fraction'), textcoords='offset points',
                horizontalalignment='left', verticalalignment='center', rotation='horizontal', fontsize='xx-small',
                arrowprops=dict(arrowstyle='-|>', fc='black', shrinkA=0, shrinkB=0,
                                connectionstyle='angle,angleA=0,angleB=90,rad=10'),
                )
    plt.axvline(med_length, color='red', linewidth=1)
    plt.annotate('\nmedian= {:.0f}'.format(med_length), xy=(med_length, 0.8), xytext=(5, 15),
                xycoords=('data', 'axes fraction'), textcoords='offset points',
                horizontalalignment='left', verticalalignment='center', rotation='horizontal', fontsize='xx-small',
                arrowprops=dict(arrowstyle='-|>', fc='black', shrinkA=0, shrinkB=0,
                                connectionstyle='angle,angleA=0,angleB=90,rad=10'),
        )
    plt.axvline(min_length, color='red', linewidth=1)
    plt.annotate(f'min: {min_length} (root)', xy=(min_length, 0.6), xytext=(5, 15),
                xycoords=('data', 'axes fraction'), textcoords='offset points',
                horizontalalignment='left', verticalalignment='center', rotation='horizontal', fontsize='xx-small',
                arrowprops=dict(arrowstyle='-|>', fc='black', shrinkA=0, shrinkB=0,
                                connectionstyle='angle,angleA=0,angleB=90,rad=10'),
                )
    plt.axvline(max_length, color='red', linewidth=1)
    plt.annotate(f'max: {max_length}', xy=(max_length, 0.5), xytext=(5, 15),
                xycoords=('data', 'axes fraction'), textcoords='offset points',
                horizontalalignment='left', verticalalignment='center',rotation='horizontal', fontsize='xx-small',
                arrowprops=dict(arrowstyle='-|>', fc='black', shrinkA=0, shrinkB=0,
                                connectionstyle='angle,angleA=0,angleB=90,rad=10'),
                )
    plt.tight_layout()
    plt.savefig(directory+'/histogram_path_length.pdf')


def test_min_max(the_rbt, base_list):

    log.info(f'{newline}Testing min,max')
    print(f'{newline}Testing min,max')

    try:

        the_min = the_rbt.min()
        if  the_min == min(base_list):
            log.info(f'Correct min ({the_min})')
            print(f'Correct min ({the_min})')
        else:
            log.error(f'Error: Calculated Min is {the_min}, while it should be {min(base_list)}')
            print(f'Error: Calculated Min is {the_min}, while it should be {min(base_list)}')
            exit()
    except:
            log.exception(f'Error: in calculating min value')
            print(f'Error: in calculating min value')
            exit()

    try:
        the_max = the_rbt.max()
        if  the_max == max(base_list):
            log.info(f'Correct max ({the_max})')
            print(f'Correct max ({the_max})')
        else:
            log.error(f'Error: Calculated Max is {the_max}, while it should be {max(base_list)}')
            print(f'Error: Calculated Max is {the_max}, while it should be {max(base_list)}')
            exit()
    except:
        log.exception(f'Error: in calculating max value')
        print(f'Error: in calculating max value')
        exit()

    return [the_min,the_max]


def test_bfs(the_rbt, base_list):

    log.info(f'{newline}Testing BFS')
    print(f'{newline}Testing BFS')

    bfs_list = the_rbt.bfs()
    bfs_list_length = len(bfs_list)
    log.info(f'BFS: length {bfs_list_length} vs base_list {len(base_list)}')
    log.debug(f'BASE_LIST: {base_list}')
    log.debug(f'BFS: {bfs_list}')
    for i in range(bfs_list_length-1):
        if bfs_list[i] > bfs_list[i+1]:
            if i+2 < bfs_list_length and bfs_list[i+1] > bfs_list[i+2]:
                log.error(f'Wrong BFS, check items {bfs_list[i]},{bfs_list[i+1]},{bfs_list[i+2]}')
                print(f'Wrong BFS, check items {bfs_list[i]},{bfs_list[i+1]},{bfs_list[i+2]}')
                exit()

    log.info(f'Passed the first BFS validity test.')
    print(f'Passed the first BFS validity test.')


def create_graph(new_rbt, new_bfs, filename):

    log.debug(f'-{tab}Drawing tree diagram ({filename}), based on the provided BFS.')
    print(f'-{tab}Drawing tree diagram ({filename}), based on the provided BFS.')

    BIG_NUMBER = 100000
    THE_VALUE = 0
    THE_COLOR = 1
    LEFT_VALUE = 2
    RIGHT_VALUE = 3

    def gname(input):
        return(f'n{input+BIG_NUMBER if input >= 0 else abs(input)+2*BIG_NUMBER}')

    graph = f'digraph RBTREE {{\ngraph [class="{int(time())}"];'
    for i, item in enumerate(new_bfs):

        graph = f'{graph}{newline}{gname(item[THE_VALUE])} [label = "{item[THE_VALUE]}", style=filled, fontcolor = white, fillcolor = {item[THE_COLOR]}];'

        if not (item[LEFT_VALUE] is None):
            graph = f'{graph}{newline}{gname(item[THE_VALUE])} -> {gname(item[LEFT_VALUE])};'

        if not (item[RIGHT_VALUE] is None):
            graph = f'{graph}{newline}{gname(item[THE_VALUE])} -> {gname(item[RIGHT_VALUE])};'

    graph = graph + '\n}'
    log.debug(f'Graph:{newline}{graph}')
    f = open(f'{directory}/{filename}.gv', 'w')
    f.write(graph)
    f.close()

    log.debug(f'-{tab}Created tree diagram ({filename}), based on the provided BFS.')
    print(f'-{tab}Created tree diagram ({filename}), based on the provided BFS.')


def test_redblack_constraints(new_rbt, new_bfs, filename):

    THE_VALUE = 0
    THE_COLOR = 1
    LEFT_VALUE = 2
    RIGHT_VALUE = 3
    THE_INDEX = 4

    def find_child(value, start=0):

        if start > len(new_bfs)-2:
            return None

        for i, item in enumerate(new_bfs[start:len(new_bfs)-2]):
            if item[THE_VALUE] == value:
                log.debug(f'find_child returning {[new_bfs[i][THE_VALUE], new_bfs[i][THE_COLOR], new_bfs[i][LEFT_VALUE], new_bfs[i][RIGHT_VALUE], i+start]}')
                return [new_bfs[i+start][THE_VALUE], new_bfs[i+start][THE_COLOR], new_bfs[i+start][LEFT_VALUE], new_bfs[i+start][RIGHT_VALUE], i+start]

        return None

    def test_black_count(index):
        if index >= len(new_bfs):
            return 0

        left_node = find_child(new_bfs[index][LEFT_VALUE], index+1)
        right_node = find_child(new_bfs[index][RIGHT_VALUE], index+2)

        left_black_count = 0
        if not (left_node is None):
            if (str(left_node[THE_COLOR]).upper() == 'BLACK'):
                left_black_count += 1
            left_black_count += test_black_count(left_node[THE_INDEX])

        right_black_count = 0
        if not (right_node is None):
            if (str(right_node[THE_COLOR]).upper() == 'BLACK'):
                right_black_count += 1
            right_black_count += test_black_count(right_node[THE_INDEX])

        if right_black_count != left_black_count:
            log.error(f'Error: For the node {new_bfs[index][THE_VALUE]}, the number of black nodes in each path in the right branch ({right_black_count}) is not the same as its left branch ({left_black_count}).')
            print(f'Error: For the node {new_bfs[index][THE_VALUE]}, the number of black nodes in each path in in the right branch ({right_black_count}) is not the same as its left branch ({left_black_count}).')
            exit()
        else:
            log.info(f'For the node {new_bfs[index][THE_VALUE]}, the number of black nodes in in each path in the right branch ({right_black_count}) is the same as of each path in its left branch ({left_black_count}).')

        return left_black_count

    def test_black_count_constraint():

        log.info(f'-{tab}Testing black count constraint')
        print(f'-{tab}Testing black count constraint')

        test_black_count(0)

        log.info(f'-{tab}Passed testing black count constraint')
        print(f'-{tab}Passed testing black count constraint')

    def test_red_parent_constraint():

        log.info(f'-{tab}Testing red parent constraint')
        print(f'-{tab}Testing red parent constraint')

        for i, item in enumerate(new_bfs):

            if str(item[THE_COLOR]).upper() == 'RED':

                left_node = find_child(item[LEFT_VALUE], i+1)
                right_node = find_child(item[RIGHT_VALUE], i+1)

                if (not (left_node is None)) and str(left_node[THE_COLOR]).upper() == 'RED':
                    log.error(f'ERROR: In {filename}, a red left child ({left_node[THE_VALUE]}  for a red parent ({item[THE_VALUE]}) violates Red-Black Trees constraints.')
                    print(f'ERROR: In {filename}, a red left child ({left_node[THE_VALUE]}  for a red parent ({item[THE_VALUE]}) violates Red-Black Trees constraints.')
                    exit()

                if (not (right_node is None)) and str(right_node[THE_COLOR]).upper() == 'RED':
                    log.error(f'ERROR: In {filename}, a red right child ({right_node[THE_VALUE]}  for a red parent ({item[THE_VALUE]}) violates Red-Black Trees constraints.')
                    print(f'ERROR: In {filename}, a red right child ({right_node[THE_VALUE]}  for a red parent ({item[THE_VALUE]}) violates Red-Black Trees constraints.')
                    exit()

        log.info(f'-{tab}Passed testing red parent constraint')
        print(f'-{tab}Passed testing red parent constraint')


    test_red_parent_constraint()
    test_black_count_constraint()


def test_structure ():

    SAMPLE_SIZE = 300

    log.debug(f'{newline}Testing tree structure (based on the provided BFS).')
    print(f'{newline}Testing tree structure (based on the provided BFS).')

    example_base_list = [-146,195,-440,247,-205,-470,-129,251,350,29,111,-144,32,-154,374,-93,-351,23,297,307,-314,450,203,-10,283,142,252,76,119,153,-191,458,465,-301,-478,312,40,-265,-302,381,-68,-120,-404,64,-226,-3,148,75,82,-27,-462,363,-266,424,94,-454,-348,-245,-382,205,427,50,464,-444,-23,-455,-204,-474,-26,-151,-373,432,463,-187,-40,-229,-184,-46,-456,-386,-73,164,-400,-293,302,159,118,104,-87,-6,170,-222,-88,-329,-337,-164,174,-425,196,-30,-280,340,33,453,-346,-398,15,-72,-447,-98,-45,-64,-295,349,-284,377,58,-459,-476,273,-426,-148,-322,-288,135,110,-186,-55,-111,185,352,367,376,189,-160,96,-480,81,-344,171,54,344,-209,-378,68,-308,-70,-358,-417,-457,65,-14,-52,-12,-240,-392,183,172,-336,-321,86,403,0,462,-464,-97,235,-393,8,-216,457,198,249,-217,-225,-374,-359,175,433,446,166,320,-112,71,288,-407,216,-449,27,-41,91,-367,217,77,-379,-206,423,10,139,-200]
    sample_base_list = np.random.choice(np.arange(-1000, 1000), SAMPLE_SIZE, replace=False)

    case = 1
    for input_list in [example_base_list,sample_base_list]:

        #Create graph
        new_rbt = rbt.RedBlackTree()    
        for key in input_list:
            new_rbt.insert(key)

        new_bfs = new_rbt.bfs()
        log.debug(f'New BFS: {new_bfs}')

        create_graph(new_rbt, new_bfs, f'sample_rbtree_{case}')

        test_redblack_constraints(new_rbt, new_bfs, f'sample_rbtree_{case}')


        case+=1



def test_dfs(the_rbt):

    log.info(f'DFS {the_rbt.dfs()}')
    
# def create_graph(the_rbt):

#     if len(the_rbt) > 100:
#         print('\nThe graph is too large (>100). I will not draw it.')
#         return

#     dfs = the_rbt.dfs()
#     graph ='''
#     graph ""
#     {
#     '''

#     for node in dfs:
#         graph = graph + f'n{node[0]} [label="{node[0]}"] {newline}'

#     graph = graph + "}"


def bench_insertremove(the_rbt, base_list, remove_list):
    # BENCH_LIST_SIZE    
    insert_remove_cplist = create_insertremove_cplist(base_list, remove_list)

    log.info('Insert and remove several items.')            
    print('Inserting and removing several items.')            
    try:
        for item in insert_remove_cplist:
            log.info(f'For: {item}')
            if item[1] == 0:
                log.info(f'Inserting : {item[0]}')
                the_rbt.insert(item[0])
            elif item[1] == 1:
                log.info(f'Removing : {item[0]}')
                the_rbt.remove(item[0])
            else:
                log.info(f'ERROR : {item[0]}')
                pass
    except:
        log.exception('Error in inserting or removing')
        print("Error in inserting or removing")
        exit()
            
    log.info('Test for existing items.')            
    print('Test for existing items')            
    try:
        for item in base_list:
            log.info(item)                
            if the_rbt.search(item):
                log.info(f'Correctly contains : {item}')
            else:
                log.error(f'ERROR does not contain: {item}')
                print(f'ERROR does not contain: {item}')
                exit()
    except:
        log.exception("Error: the tree does not find the item that should be there.")
        print("Error: the tree does not find the item that should be there.")
        exit()
    log.info('Correct insertion, removal and search.')            
    print('Correct insertion, removal and search.')            



def test_redblacktree(the_rbt):

    # Test if it has the required functions
    check_functions(the_rbt)


    base_list, remove_list = create_base_and_remove_lists()
    log.debug(f'Base List{base_list}')
    log.debug(f'Remove List{remove_list}')


    # insert_remove_cplist=create_insertremove_cplist(base_list, remove_list)
    test_insertremove(the_rbt, base_list, remove_list)



    #test path
    path_lengths = test_path(the_rbt, base_list)

    #Create path length histogram
    create_path_length_hist(path_lengths)


    #Testing min,max
    the_min, the_max = test_min_max(the_rbt, base_list)


    #Testing BFS
    test_bfs(the_rbt, base_list)


    #esting Structure (based on BFS)
    test_structure()

    # print('Testing DFS')
    # test_dfs(the_rbt)


    # test_insertremove(the_rbt, action_cplist)

    # Test polluted list
    # test_insertremove(the_rbt, polluted_list)


if __name__ == "__main__":

    import red_black_tree as rbt        
    the_rbt = rbt.RedBlackTree()
    test_redblacktree(the_rbt)





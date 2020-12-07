# Shahryar Eivazzadeh, December 2020, sei@bth.se
import sys
if (sys.version < "3.7"):
    print("Your Python version is old. It is " +
          sys.version+" . Upgrade to at least 3.7")
    exit()

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import timeit
from statistics import mean, median, stdev


# some config
SPEED_FACTOR = 1
LIST_SIZE = 5000//SPEED_FACTOR
TEST_TIMES = 500//SPEED_FACTOR
GROW_STEP_SIZE = 30
newline = '\n'


def wrapper(func, *args, **kwargs):
    def wrapped():
        return func(*args, **kwargs)
    return wrapped


def python_sort(input):
    return(sorted(input))


def check_sorting(sortfunc):

    input_list = np.random.randint(-1000, 1000, size=100).tolist()
    sorted_list = sortfunc(input_list)
    for i in range(0, len(sorted_list)-1):
        if sorted_list[i] > sorted_list[i+1]:
            return False

    return True


def fixed_sorting(sortfunc):

    bench_result = []
    rand_low, rand_high, rand_list_size = -1000, 1000, LIST_SIZE
    for i in range(0, TEST_TIMES):
        rand_list = np.random.randint(
            rand_low, rand_high, size=rand_list_size).tolist()
        wrapped_sort_func = wrapper(sortfunc, rand_list)
        the_time = timeit.timeit(wrapped_sort_func, number=1)
        bench_result.append(the_time)
    return(bench_result)


def variable_sorting(sortfunc):

    bench_result = []
    rand_low, rand_high = -1000, 1000
    for i in range(0, LIST_SIZE, GROW_STEP_SIZE):  # 1
        rand_list = np.random.randint(rand_low, rand_high, size=i).tolist()
        wrapped_sort_func = wrapper(sortfunc, rand_list)
        the_time = timeit.timeit(wrapped_sort_func, number=1)
        bench_result.append(the_time)

    expanded_result = np.repeat(bench_result, GROW_STEP_SIZE)[:LIST_SIZE]
    return(expanded_result[:].tolist())


def create_report(sortfunc_list):

    # setup
    directory = os.path.dirname(os.path.abspath(__file__))
    test_fixed_funcwrap_list = []
    sortfunc_names = []
    for func in sortfunc_list:
        test_fixed_funcwrap_list.append(wrapper(fixed_sorting, func))
        sortfunc_names.append(func.__name__)

    # check correctness
    for i, func in enumerate(sortfunc_list):
        if check_sorting(func):
            print("Correct sorting: " + sortfunc_names[i])
        else:
            print("Failed sorting: " + sortfunc_names[i])
            exit()

    # bench fixed-size and growing size
    bench_dataframe = pd.DataFrame()
    variable_dataframe = pd.DataFrame()
    for k, sortfunc in enumerate(sortfunc_list):
        print(f'{newline}Testing {sortfunc_names[k]} for growing list size, 1 to {LIST_SIZE}')
        variable_dataframe.insert(0, sortfunc_names[k], variable_sorting(sortfunc))
        print(f'{newline}Testing: {sortfunc_names[k]} for fixed list size ({LIST_SIZE})')
        bench_dataframe.insert(0, sortfunc_names[k], fixed_sorting(sortfunc))

    variable_dataframe.insert(0, 'Input Size', list(range(1, LIST_SIZE+1)))

    # Creating individual histogram for sorting algorithms
    print('Creating individual histogram for sorting algorithms')
    for j, sortfunc in enumerate(sortfunc_names):

        min_time = min(bench_dataframe.loc[j])
        max_time = max(bench_dataframe.loc[j])
        avg_time = mean(bench_dataframe.loc[j])
        med_time = median(bench_dataframe.loc[j])
        sd_time = stdev(bench_dataframe.loc[j])
        stat_sentence = \
            f'{newline}min=' + '{:0.3e}'.format(min_time) + \
            f'{newline}average=' + '{:0.3e}'.format(avg_time) + \
            f'{newline}median=' + '{:0.3e}'.format(med_time) + \
            f'{newline}max=' + '{:0.3e}'.format(max_time) + \
            f'{newline}SD=' + '{:0.3e}'.format(sd_time)
        print(
            f'{newline}For {sortfunc_names[j]}:{newline} {stat_sentence} {newline}')

        hist_plot = bench_dataframe.hist(
            grid=False,
            column=sortfunc_names[j],
            bins=int(LIST_SIZE/10),
        )
        hist_plot = hist_plot[0]
        for x in hist_plot:
            x.spines['right'].set_visible(False)
            x.spines['top'].set_visible(False)
            x.spines['left'].set_visible(False)
            x.set_title(
                f"Time duration for {sortfunc_names[j]}{newline}{stat_sentence}")
            x.set_xlabel("Time Duration (Seconds)", size=12)
            x.set_ylabel("Frequency", size=12)

        plt.tight_layout()
        plt.savefig(directory+'/histogram_'+sortfunc_names[j]+'.pdf')

    # mixed grow plot
    print("Mixed grow plot is being created.")
    grow_melted = variable_dataframe.melt('Input Size')
    sns.set_theme(style="white")
    sns.set(style="ticks")  # ,rc={'figure.figsize':(16,8.27)}
    g = sns.lmplot(x='Input Size', y='value', data=grow_melted, hue='variable', legend=False, fit_reg=True,
                   scatter_kws={"s": 10, "alpha": .5}, line_kws={"lw": 2, "alpha": 0.5})  # legend=False,
    plt.legend(bbox_to_anchor=(0.65, 1), loc='upper left', borderaxespad=0.)
    plt.title("Time Duration By Growing Input Size", size=16)
    g.set_axis_labels("Input Size", "Time Duration (Seconds)")
    fig = plt.gcf()
    fig.set_size_inches(18.5, 10.5)
    plt.tight_layout()
    plt.savefig(directory+'/grow_mixed.pdf')

    # mixed KDE plot
    print("Mixed density (KDE) plot is being created.")
    mixed_plot = bench_dataframe.plot.kde(
        title='Mixed Density (KDE) Plot'
    )
    mixed_plot.set_xlabel('Time Duration (Seconds)')
    mixed_plot.get_figure().savefig(directory+'/density_mixed.pdf')

    # mixed boxplot
    print("Mixed boxplot is being created.")
    boxplot_plot = bench_dataframe.plot.box(
        title='Mixed BoxPlot (no outlier)',
        showfliers=False,
    )
    boxplot_plot.set_ylabel('Time Duration (Seconds)')
    boxplot_plot.get_figure().savefig(directory+'/boxplot_mixed.pdf')


if __name__ == "__main__":
    from quicksort_inplace import quicksort_inplace
    from quicksort_notinplace import quicksort_notinplace
    from mergesort_inplace import mergesort_inplace
    from mergesort_notinplace import mergesort_notinplace
    from heapsort_inplace import heapsort_inplace
    from heapsort_notinplace import heapsort_notinplace

    sortfunc_list = [python_sort, quicksort_inplace, quicksort_notinplace,
                     mergesort_inplace, mergesort_notinplace, heapsort_inplace, heapsort_notinplace]
    create_report(sortfunc_list)

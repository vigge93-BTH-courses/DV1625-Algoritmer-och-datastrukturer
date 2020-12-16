# Shahryar Eivazzadeh, December 2020, sei@bth.se
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import os
import timeit
from statistics import mean, median, stdev
if (sys.version < "3.7"):
    print("Your Python version is old. It is " +
          sys.version+" . Upgrade to at least 3.7")
    exit()
sns.reset_orig()
matplotlib.rc_file_defaults()

# some config
SPEED_FACTOR = 1
LIST_SIZE = 100000//SPEED_FACTOR
TEST_TIMES = 500//SPEED_FACTOR
GROW_STEP_SIZE = 5000*SPEED_FACTOR
GROW_MAX_SIZE = 1000000//SPEED_FACTOR
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
        print(i)
        rand_list = np.random.randint(
            rand_low, rand_high, size=rand_list_size).tolist()
        wrapped_sort_func = wrapper(sortfunc, rand_list)
        the_time = timeit.timeit(wrapped_sort_func, number=1)
        bench_result.append(the_time)
    return(bench_result)


def variable_sorting(sortfunc):

    bench_result = []
    rand_low, rand_high = -1000, 1000
    for i in range(0, GROW_MAX_SIZE, GROW_STEP_SIZE):  # 1
        print(i)
        rand_list = np.random.randint(rand_low, rand_high, size=i).tolist()
        wrapped_sort_func = wrapper(sortfunc, rand_list)
        the_time = timeit.timeit(wrapped_sort_func, number=1)
        bench_result.append(the_time)

    expanded_result = np.repeat(bench_result, GROW_STEP_SIZE)[:GROW_MAX_SIZE]
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
        print(f'{newline}Testing {sortfunc_names[k]} for growing list size, 1 to {GROW_MAX_SIZE}')
        variable_dataframe.insert(0, sortfunc_names[k], variable_sorting(sortfunc))
        print(f'{newline}Testing: {sortfunc_names[k]} for fixed list size ({LIST_SIZE})')
        bench_dataframe.insert(0, sortfunc_names[k], fixed_sorting(sortfunc))

    variable_dataframe.insert(0, 'Input Size', list(range(1, GROW_MAX_SIZE+1)))

    # Creating individual histogram for sorting algorithms
    print('Creating individual histogram for sorting algorithms')
    for j, sortfunc in enumerate(sortfunc_names):

        min_time = min(bench_dataframe[sortfunc])
        max_time = max(bench_dataframe[sortfunc])
        avg_time = mean(bench_dataframe[sortfunc])
        med_time = median(bench_dataframe[sortfunc])
        sd_time = stdev(bench_dataframe[sortfunc])
        stat_sentence = \
            f'{newline}min=' + '{:0.3e}'.format(min_time) + \
            f'{newline}average=' + '{:0.3e}'.format(avg_time) + \
            f'{newline}median=' + '{:0.3e}'.format(med_time) + \
            f'{newline}max=' + '{:0.3e}'.format(max_time) + \
            f'{newline}SD=' + '{:0.3e}'.format(sd_time)
        print(
            f'{newline}For {sortfunc}:{newline} {stat_sentence} {newline}')

        hist_plot = bench_dataframe.hist(
            grid=False,
            column=sortfunc,
            bins=int(LIST_SIZE/10),
            histtype='step'
        )
        hist_plot = hist_plot[0]
        for x in hist_plot:
            x.spines['right'].set_visible(False)
            x.spines['top'].set_visible(False)
            x.spines['left'].set_visible(False)
            x.set_title(f"Time duration for {sortfunc}")
            x.annotate(f'{stat_sentence}', xy=(1, 1),
                       xytext=(1, 1.5), xycoords=('axes fraction', 'axes fraction'), textcoords='offset points',
                       horizontalalignment='left', verticalalignment='top', fontsize='x-small', annotation_clip=False
                       )
            x.set_xlabel("Time Duration (Seconds)", size=12)
            x.set_ylabel("Frequency", size=12)
        
        plt.axvline(avg_time, color='red', linewidth=1)
        plt.annotate('avg: {:0.3e}'.format(avg_time), xy=(avg_time, 0.7), xytext=(5, 15),
                     xycoords=('data', 'axes fraction'), textcoords='offset points',
                     horizontalalignment='left', verticalalignment='center', rotation='horizontal', fontsize='xx-small',
                     arrowprops=dict(arrowstyle='-|>', fc='black', shrinkA=0, shrinkB=0,
                                     connectionstyle='angle,angleA=0,angleB=90,rad=10'),
                     )
        plt.axvline(med_time, color='red', linewidth=1)
        plt.annotate('median: {:0.3e}'.format(med_time), xy=(med_time, 0.8), xytext=(5, 15),
                     xycoords=('data', 'axes fraction'), textcoords='offset points',
                     horizontalalignment='left', verticalalignment='center', rotation='horizontal', fontsize='xx-small',
                     arrowprops=dict(arrowstyle='-|>', fc='black', shrinkA=0, shrinkB=0,
                                     connectionstyle='angle,angleA=0,angleB=90,rad=10'),
                     )
        plt.axvline(min_time, color='red', linewidth=1)
        plt.annotate('min: {:0.3e}'.format(min_time), xy=(min_time, 0.6), xytext=(5, 15),
                     xycoords=('data', 'axes fraction'), textcoords='offset points',
                     horizontalalignment='left', verticalalignment='center', rotation='horizontal', fontsize='xx-small',
                     arrowprops=dict(arrowstyle='-|>', fc='black', shrinkA=0, shrinkB=0,
                                     connectionstyle='angle,angleA=0,angleB=90,rad=10'),
                     )
        plt.axvline(max_time, color='red', linewidth=1)
        plt.annotate('max: {:0.3e}'.format(max_time), xy=(max_time, 0.5), xytext=(5, 15),
                     xycoords=('data', 'axes fraction'), textcoords='offset points',
                     horizontalalignment='left', verticalalignment='center', rotation='horizontal', fontsize='xx-small',
                     arrowprops=dict(arrowstyle='-|>', fc='black', shrinkA=0, shrinkB=0,
                                     connectionstyle='angle,angleA=0,angleB=90,rad=10'),
                     )
        plt.tight_layout()
        plt.savefig(directory+'/histogram_'+sortfunc+'.pdf')

    # mixed grow plot
    print("Mixed grow plot is being created.")
    grow_melted = variable_dataframe.melt('Input Size')
    sns.set_theme(style="white")
    sns.set(style="ticks")  # ,rc={'figure.figsize':(16,8.27)}
    g = sns.lmplot(x='Input Size', y='value', data=grow_melted, hue='variable', legend=False, fit_reg=True,
                   scatter_kws={"s": 10, "alpha": .5}, line_kws={"lw": 2, "alpha": 0.5}, ci=None)  # legend=False,
    plt.legend(bbox_to_anchor=(0.65, 1), loc='upper left', borderaxespad=0.)
    plt.title("Time Duration By Growing Input Size", size=16)
    g.set_axis_labels("Input Size", "Time Duration (Seconds)")
    fig = plt.gcf()
    fig.set_size_inches(28.5, 10.5)
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
    plt.xticks(fontsize='xx-small', rotation=90)
    boxplot_plot.set_ylabel('Time Duration (Seconds)')
    plt.tight_layout()
    boxplot_plot.get_figure().savefig(directory+'/boxplot_mixed.pdf')

    # mixed KDE plot without python_sort
    print("Mixed density (KDE) plot is being created.")
    bench_dataframe = bench_dataframe.drop(columns='python_sort')
    mixed_plot = bench_dataframe.plot.kde(
        title='Mixed Density (KDE) Plot'
    )
    mixed_plot.set_xlabel('Time Duration (Seconds)')
    mixed_plot.get_figure().savefig(directory+'/density_mixed_2.pdf')


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

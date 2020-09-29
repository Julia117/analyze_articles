from statsmodels.tsa.seasonal import seasonal_decompose
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates


def make_plot(similar_vk, similar_vm, similar_mk):
    """
    Draw 3 subplots with number of pairs of similar articles
    between each pair of newspapers

    Parameters
    ----------
    similar_vk, similar_mk, similar_vm : similar_x is a dictionary
                in format {date : [similar_articles]} where similar_articles
                are pairs with vector similarity > 0.92. V stands for vedomosti,
                k stands for kommersant and m stands for meduza.

    Returns
    -------
    Draws 3 subplots with dates on shared x-axis and number of similar pairs
    between two newspapers on y-axis.

    """

    fig, axs = plt.subplots(3, 1, sharex=True)

    axs[0].plot(list(similar_mk.keys()), list(len(x) for x in similar_mk.values()))
    axs[0].set_title("meduza~kommersant")
    axs[1].plot(list(similar_vk.keys()), list(len(x) for x in similar_vk.values()))
    axs[1].set_title("vedomosti~kommersant")
    axs[2].plot(list(similar_vm.keys()), list(len(x) for x in similar_vm.values()))
    axs[2].set_title("vedomosti~meduza")

    # Filter all the redundant labels
    plt.xticks(list(similar_vk.keys())[::7])

    # And finally, we place the labels back
    plt.tick_params(labelbottom=True)
    plt.xticks(rotation=30, fontsize=8)
    plt.tick_params(labelbottom=True)

    # TODO
    # plt.axvline(x='2020/08/09', color='r', linewidth=0.5)
    # plt.axvline(x='2020/07/07', color='r', linewidth=0.5)


def make_plot_trend(similar_vk, similar_vm, similar_mk):
    """
    Draw 3 subplots with trend of number of pairs of similar articles
    between each pair of newspapers

    Parameters
    ----------
    similar_vk, similar_mk, similar_vm : similar_x is a dictionary
                in format {date : [similar_articles]} where similar_articles
                are pairs with vector similarity > 0.92. V stands for vedomosti,
                k stands for kommersant and m stands for meduza.

    Returns
    -------
    Draws 3 subplots with dates on shared x-axis and trend of number of similar pairs
    between two newspapers on y-axis.

    Notes
    -----
    Trends are calculated via convolution using backward displaced moving
    weighted average.

    """

    fig, axs = plt.subplots(3, 1, sharex=True)

    decomposition_mk = seasonal_decompose(list(len(x) for x in similar_mk.values()), two_sided=False, period=7)
    decomposition_vk = seasonal_decompose(list(len(x) for x in similar_vk.values()), two_sided=False, period=7)
    decomposition_vm = seasonal_decompose(list(len(x) for x in similar_vm.values()), two_sided=False, period=7)

    axs[0].plot(list(similar_mk.keys()),decomposition_mk.trend)
    axs[0].set_title("meduza~kommersant")
    axs[1].plot(list(similar_vk.keys()),decomposition_vk.trend)
    axs[1].set_title("vedomosti~kommersant")
    axs[2].plot(list(similar_vm.keys()),decomposition_vm.trend)
    axs[2].set_title("vedomosti~meduza")

    # Filter all the redundant labels
    plt.xticks(list(similar_vk.keys())[::7])

    # And finally, we place the labels back
    plt.tick_params(labelbottom=True)
    plt.xticks(rotation=30, fontsize=8)
    plt.tick_params(labelbottom=True)

def draw_regression_line_trend(similar_articles, plot):
    """
    Draws a plot with the number of pairs of similar articles
    and the regression line.

    Parameters
    ----------
    similar_articles: a dictionary in format {date : [similar_articles]}
                where similar_articles are pairs with vector similarity > 0.92.

    Returns
    -------
    Draws a plot with number of pairs of similar articles
    and the regression line to see the trend.

    """
    decomposition = seasonal_decompose(list(len(x) for x in similar_articles.values()), two_sided=False, period=7)

    x = list(similar_articles.keys())
    dates = mdates.datestr2num(list(similar_articles.keys()))
    # dates = dates - min(dates)
    # y = list(len(x) for x in similar_articles.values())

    plot.plot(x, decomposition.trend)

    # as we use one-sided moving average the fist 5 elements are Null, so we omit them
    m, b = np.polyfit(dates[6:], decomposition.trend[6:], 1)
    # m = slope, b = intercept

    reg_line, = plot.plot(x, m * dates + b, label="slope = " + "{:.3f}".format(m))
    plot.legend(handles=[reg_line], loc='upper right')


def draw_regression_line_scatter(similar_articles, plot):
    """
    Draws a plot with the number of pairs of similar articles
    and the regression line.

    Parameters
    ----------
    similar_articles: a dictionary in format {date : [similar_articles]}
                where similar_articles are pairs with vector similarity > 0.92.

    Returns
    -------
    Draws a plot with number of pairs of similar articles
    and the regression line to see the trend.

    """
    x = list(similar_articles.keys())
    dates = mdates.datestr2num(list(similar_articles.keys()))
    dates = dates - min(dates)
    y = list(len(x) for x in similar_articles.values())

    plot.plot(x, y, 'o')

    m, b = np.polyfit(dates, y, 1)
    # m = slope, b = intercept

    reg_line, = plot.plot(x, m * dates + b, label="slope = " + "{:.3f}".format(m))
    plot.legend(handles=[reg_line], loc='upper right')


def make_plot_regression(similar_vk, similar_vm, similar_mk):
    """
    Draw 3 subplots with number of pairs of similar articles
    between each pair of newspapers and regression line

    Parameters
    ----------
    similar_vk, similar_mk, similar_vm : similar_x is a dictionary
                in format {date : [similar_articles]} where similar_articles
                are pairs with vector similarity > 0.92. V stands for vedomosti,
                k stands for kommersant and m stands for meduza.

    Returns
    -------
    Draws 3 subplots with dates on shared x-axis, number of similar pairs
    between two newspapers on y-axis and a regression line. Regression slope is
    written in the legend.

    """

    fig, axs = plt.subplots(3, 1, sharex=True)

    draw_regression_line_trend(similar_mk, axs[0])
    # axs[0].plot(list(similar_mk.keys()), list(len(x) for x in similar_mk.values()))
    axs[0].set_title("meduza~kommersant")
    # axs[1].plot(list(similar_vk.keys()), list(len(x) for x in similar_vk.values()))
    draw_regression_line_trend(similar_vk, axs[1])
    axs[1].set_title("vedomosti~kommersant")
    # axs[2].plot(list(similar_vm.keys()), list(len(x) for x in similar_vm.values()))
    draw_regression_line_trend(similar_vm, axs[2])
    axs[2].set_title("vedomosti~meduza")

    # Filter all the redundant labels
    plt.xticks(list(similar_vk.keys())[::7])

    # And finally, we place the labels back
    plt.tick_params(labelbottom=True)
    plt.xticks(rotation=30, fontsize=8)
    plt.tick_params(labelbottom=True)

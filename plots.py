from statsmodels.tsa.seasonal import seasonal_decompose
import matplotlib.pyplot as plt


def make_plot(similar_vk, similar_vm, similar_mk):
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

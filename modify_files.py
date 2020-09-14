from analyze_articles import text_processing
from analyze_articles import file_handling
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import math


def get_result_vector(tagged_article, w2v_model):
    result = []
    for word in tagged_article:
        try:
            result.append(w2v_model.get_vector(word))
        except:
            pass

    return np.array([x / len(sum(result)) for x in sum(result)]).tolist()


def vectors_similarity(v1, v2):
    return np.sum(np.asarray(v1) * np.asarray(v2)) / (np.linalg.norm(np.asarray(v1)) * np.linalg.norm(np.asarray(v2)))

def compare_pairs(paper1, paper2):
    similar_articles = {}
    for date in paper1:
        if date in paper1 and date in paper2:
            i = 0
            for vec1 in paper1[date]:
                j = 0
                for vec2 in paper2[date]:
                    similar_articles.setdefault(date, [])
                    if vectors_similarity(vec1, vec2) > 0.92:
                        similar_articles[date].append([i, j])
                    j += 1
                i += 1
    return similar_articles


def add_tags_to_articles(articles, file, dates):
    tagged_articles = {}
    try:
        for date in articles:
            if datetime.strptime(date, "%Y/%m/%d").date() in dates:
                print(date)
                tagged_articles[date] = [text_processing.add_tags(text=text) for text in articles[date]]
    finally:
        file_handling.add_to_file(file, tagged_articles)
    return tagged_articles


def artice_to_vector(tagged_articles, w2v_model, dates, file):
    vectors = {}
    try:
        for date in tagged_articles:
            if datetime.strptime(date, "%Y/%m/%d").date() in dates:
                print(date)
                vectors[date] = [get_result_vector(article, w2v_model) for article in tagged_articles[date]]
    finally:
        file_handling.add_to_file(file, vectors)
    return vectors


def similar_pairs_percentage(pairs, vectors1, vectors2):
    num_of_pairs = []
    for day in pairs:
        if(len(vectors1[day]) == 0 or (len(vectors2[day])) == 0):
            num_of_pairs.append(0)
        else:
            num_of_pairs.append(len(pairs[day]) / (len(vectors1[day])*len(vectors2[day])))
    return num_of_pairs

def make_plot(similar_vk, similar_vm, similar_mk):
    fig, axs = plt.subplots(3, 1, sharex=True)

    # There are a lot of overlapping labels that slow down the rendering
    # So, first we get rid of the labels
    # plt.tick_params(labelbottom=False) 
    # Then we plot the graph
    # plt.plot(list(result.keys()), list(result.values()))
    # similar_vm = compare_pairs(vectors_v, vectors_m)
    # similar_vk = compare_pairs(vectors_v, vectors_k)
    # similar_mk = compare_pairs(vectors_m, vectors_k)

    # axs[0].plot(list(similar_mk.keys()), similar_pairs_percentage(similar_mk, vectors_m, vectors_k))
    # axs[1].plot(list(similar_vk.keys()), similar_pairs_percentage(similar_vk, vectors_v, vectors_k))
    # axs[2].plot(list(similar_vm.keys()), similar_pairs_percentage(similar_vm, vectors_v, vectors_m))

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

    # plt.close()

def replace_0(dict):
    for day in dict:
        if  dict[day] == []:
            dict[day] = [-1,-1]
    return dict

# plt.close()
def make_plot_log(similar_vm, similar_vk, similar_mk):
    fig, axs = plt.subplots(3, 1, sharex=True)

    # similar_vm = replace_0(similar_vm)
    # similar_vk = replace_0(similar_vk)
    # similar_mk = replace_0(similar_mk)

    axs[0].plot(list(similar_mk.keys()), list(math.log(len(x),1.1) for x in similar_mk.values()))
    axs[0].set_title("meduza~kommersant")
    axs[1].plot(list(similar_vk.keys()), list(math.log(len(x),1.1)  for x in similar_vk.values()))
    axs[1].set_title("vedomosti~kommersant")
    axs[2].plot(list(similar_vm.keys()), list(math.log(len(x),1.1)  for x in similar_vm.values()))
    axs[2].set_title("vedomosti~meduza")

    # Filter all the redundant labels
    plt.xticks(list(similar_vk.keys())[::7])

    # And finally, we place the labels back
    plt.tick_params(labelbottom=True)
    plt.xticks(rotation=30, fontsize=8)
    plt.tick_params(labelbottom=True)

def make_plot_on_one(similar_vm, similar_vk, similar_mk):
    # fig, axs = plt.subplots(3, 1, sharex=True)

    # similar_vm = replace_0(similar_vm)
    # similar_vk = replace_0(similar_vk)
    # similar_mk = replace_0(similar_mk)

    plt.plot(list(similar_mk.keys()), list(len(x) for x in similar_mk.values()))
    # set_title("meduza~kommersant")
    plt.plot(list(similar_vk.keys()), list(len(x)  for x in similar_vk.values()))
    # axs[1].set_title("vedomosti~kommersant")
    plt.plot(list(similar_vm.keys()), list(len(x) for x in similar_vm.values()))
    # axs[2].set_title("vedomosti~meduza")

    # Filter all the redundant labels
    plt.xticks(list(similar_vk.keys())[::7])
    plt.yscale('log')
    # And finally, we place the labels back
    plt.tick_params(labelbottom=True)
    plt.xticks(rotation=30, fontsize=8)
    plt.tick_params(labelbottom=True)

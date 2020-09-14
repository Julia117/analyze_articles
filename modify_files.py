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



tagged_m = add_tags_to_articles(articles_m, TAGGED_MEDUZA)
tagged_v = add_tags_to_articles(articles_v, TAGGED_VEDOMOSTI)
tagged_k2 = add_tags_to_articles(articles_k, TAGGED_KOMMERSANT)



with open("analyze_articles/tagged_meduza.txt", "w") as outfile:
    json.dump(tagged_m, outfile)

with open("analyze_articles/tagged_vedomosti.txt") as json_file:
    tagged_v = json.load(json_file)
with open("analyze_articles/tagged_kommersant_full.txt") as json_file:
    tagged_k = json.load(json_file)
with open("analyze_articles/tagged_meduza.txt") as json_file:
    tagged_m = json.load(json_file)


vectors_m = artice_to_vector(tagged_m, w2v_model)
vectors_v = artice_to_vector(tagged_v, w2v_model)
vectors_k = artice_to_vector(tagged_k, w2v_model)


write_to_file(VECTORS_MEDUZA, vectors_m)
write_to_file(VECTORS_VEDOMOSTI, vectors_v)
write_to_file(VECTORS_KOMMERSANT, vectors_k)


with open(VECTORS_MEDUZA) as json_file:
    vectors_m = json.load(json_file)
with open(VECTORS_VEDOMOSTI) as json_file:
    vectors_v = json.load(json_file)
with open(VECTORS_KOMMERSANT) as json_file:
    vectors_k = json.load(json_file)

similar_vm = compare_pairs(vectors_v, vectors_m)
similar_vk = compare_pairs(vectors_v, vectors_k)
similar_mk = compare_pairs(vectors_m, vectors_k)


import matplotlib.pyplot as plt

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

plt.close()
# result_vm = {}
# for date in similar_vm:
#     result_vm[date] = len(similar_vm[date])
#
# from datetime import timedelta
# # date_list = [datetime.strptime(list(result_vm.keys())[0],'%Y/%m/%d') - datetime.timedelta(days=x) for x in range(10)]
#
# # datelist = pd.date_range(pd.datetime(2017, 1, 1).strftime('%Y-%m-%d'), periods=42).tolist()
#
# # newdate = pd.date_range(result_vm.keys().strftime('%Y/%m/%d'), periods=10).tolist()
# import matplotlib.pyplot as plt
#
# # There are a lot of overlapping labels that slow down the rendering
# # So, first we get rid of the labels
# plt.tick_params(labelbottom=False)
#
# # Then we plot the graph
# plt.plot(list(result_vm.keys()), list(result_vm.values()))
#
# # Filter all the redundant labels
# plt.xticks(list(result_vm.keys())[::7])
#
# # And finally, we place the labels back
# plt.tick_params(labelbottom=True)
# plt.xticks(rotation=30, fontsize=8)
# plt.tick_params(labelbottom=True)
#
# # TODO
# plt.axvline(x = '2020/08/09', color='r', linewidth=0.5)
# plt.axvline(x = '2020/07/07', color='r', linewidth=0.5)
#
# plt.close()

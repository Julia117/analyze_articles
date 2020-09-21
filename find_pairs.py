import numpy as np


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

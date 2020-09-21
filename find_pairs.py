import numpy as np


def vectors_similarity(v1, v2):
    """
    Get cosine similarity of two vectors

    Parameters
    ----------
    v1, v2 : vectors to compare

    Returns
    -------
    A float number from 0 to 1

    Notes
    -----
    To calculate vectors similarity for texts we calculate cosine
    between two vectors. For more information check
    https://www.quora.com/Why-do-we-use-cosine-similarity-on-Word2Vec-instead-of-Euclidean-distance

    """
    return np.sum(np.asarray(v1) * np.asarray(v2)) / (np.linalg.norm(np.asarray(v1)) * np.linalg.norm(np.asarray(v2)))


def compare_pairs(paper1, paper2):
    """
    Make pairwise comparison between articles from two papers

    Parameters
    ----------
    paper1, paper2 : papers to compare

    Returns
    -------
    similar_articles
            A dictionary in format {date : [similar_articles]} where similar
            articles are pairs with vector similarity > 0.92

    """
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

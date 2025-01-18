def sort_verses_by_relevance(verses, query):
    def relevance_score(verse):
        score = 0
        for term in query.split():
            score += verse.lower().count(term.lower())
        return score

    sorted_verses = sorted(verses, key=relevance_score, reverse=True)
    return sorted_verses

def filter_verses(verses, query, min_score=1):
    def relevance_score(verse):
        score = 0
        for term in query.split():
            score += verse.lower().count(term.lower())
        return score

    return [verse for verse in verses if relevance_score(verse) >= min_score]
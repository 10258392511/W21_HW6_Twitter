from HW_6_Twitter_Starter_Code import *


def make_request_with_local_cache(baseurl, hashtag, count, cache):
    """
    A revised version using a local cache.

    Check the cache for a saved result for this baseurl+params:values
    combo. If the result is found, return it. Otherwise send a new
    request, save it, then return it.


    Parameters
    ----------
    baseurl: string
        The URL for the API endpoint
    hashtag: string
        The hashtag to search
    count: integer
        The number of tweets to retrieve
    cache: dict
        A local cache.

    Returns
    -------
    dict
        the results of the query as a dictionary loaded from cache
        JSON
    """
    # TODO Implement function
    CACHE_DICT = cache
    params = {"q": hashtag.lower(), "count": count}
    unique_key = construct_unique_key(baseurl, params)
    if unique_key in CACHE_DICT:
        print("fetching cached data")
        return CACHE_DICT[unique_key]
    else:
        print("making new requests")
        results = make_request(baseurl, params)
        CACHE_DICT[unique_key] = results
        save_cache(CACHE_DICT)
        return results


def find_top_hashtags(tweets: dict, hasgtag_ignore: str, num_top: int = 3) -> list:
    """
    Find the top 3 co-occurring hashtags.

    Parameters
    ----------
    tweets: dict
        Namely the value of "statuses" of a raw api response.
    hashtag_ignore: str
        Excluding the original hashtag used to make the query.
    num_top: int
        How many co-occurring hashtags need to be collected.

    Returns
    -------
    list of tuples
        [(hashtag, frequency)]
    """
    counter = Counter()
    for tweet in tweets:
        tags = tweet["entities"]["hashtags"]
        for tag in tags:
            if tag["text"].lower() == hasgtag_ignore[1:].lower():
                continue
            counter[f"#{tag['text']}"] += 1

    return counter.most_common(num_top)


def find_top_words(tweets: dict, stop_words: list, num_top: int = 10) -> list:
    """
    Find the top 10 co-occurring words, case-insensitive. We only count strings with letters and numbers as valid words.

    Parameters
    ----------
    tweets: dict
        Namely the value of "statuses" of a raw api response.
    stop_words: list
        List of stop words read from a file.
    num_top: int
        How many co-occurring hashtags need to be collected.

    Returns
    -------
    list of tuples
        [(word, frequency)]
    """
    counter = Counter()
    for tweet in tweets:
        text = tweet["text"].split(" ")
        for word in text:
            word = word.lower()
            if (word) != "rt" and (word not in stop_words) and word.isalnum():
                counter[word] += 1

    return counter.most_common(num_top)


if __name__ == '__main__':
    base_url = "https://api.twitter.com/1.1/search/tweets.json"
    count = 100

    stop_words = []
    with open("./stop-word-list.txt", "r") as rf:
        line = rf.readline().strip()
        while len(line) > 0:
            stop_words.append(line)
            line = rf.readline().strip()

    # for word in stop_words:
    #     print(word)

    # # a test for a nonsensical hashtag
    # hash_tag = "#ascoinasco"
    # params = {"q": hash_tag, "count": count}
    # results = make_request(base_url, params)
    # print(results)

    CACHE_DICT = open_cache()
    # for key in CACHE_DICT:
    #     print(key)

    # interactive prompt
    while True:
        hash_tag = input("Please enter a hashtag to make a query, beginning with '#' or 'exit' to quit: ").strip()
        if hash_tag == "exit":
            break

        if hash_tag[0] != "#":
            print("Invalid hashtag. ", end="")
            continue

        results = make_request_with_local_cache(base_url, hash_tag, count, CACHE_DICT)  # dict
        tweets = results["statuses"]

        if len(tweets) == 0:
            print("Sorry, no result is found.")
            continue

        # ec1: 3 top hashtags
        top_tags = find_top_hashtags(tweets, hash_tag)
        print(f"3 most commonly co-occurring hashtags are ", end="")
        for i, tag in enumerate(top_tags):
            if i == len(top_tags) - 1:
                print(tag[0])
            else:
                print(tag[0], end=", ")

        # ec2: 10 top words
        top_words = find_top_words(tweets, stop_words)
        print(f"10 top words are ", end="")
        for i, top_word in enumerate(top_words):
            if i == len(top_words) - 1:
                print(f"({top_word[0]}, {top_word[1]} time(s))")
            else:
                print(f"({top_word[0]}, {top_word[1]} time(s))", end=", ")

    print("Bye!")

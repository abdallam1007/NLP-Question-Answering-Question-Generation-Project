
def most_freq_pronoun(article):
    prns = {"he": 0, "she": 0, "they": 0, "it": 0}
    text = open(article)
    title = text.readline()

    title_tok = title.split(" ")
    if "(" in title_tok[-1]:
        title_tok.pop()

    title = " ".join(title_tok)

    toks = text.read().split(" ")
    total_prns = 0

    for word in toks:
        if word in ["He", "he"]:
            prns["he"] += 1
            total_prns += 1
        elif word in ["She", "she"]:
            prns["she"] += 1
            total_prns += 1
        elif word in ["It", "it"]:
            prns["it"] += 1
            total_prns += 1
        elif word in ["They", "they"]:
            prns["they"] += 1
            total_prns += 1

    max = 0
    prn = ""
    for key in prns:
        if prns[key] > max:
            max = prns[key]
            prn = key

    if float(prns["it"]) / total_prns * 100 >= 22:
        return (prns, "it", title)

    return (prns, prn, title)


def get_it_prop_avg_people_set():
    proportion_people = [0, 0, 0, 0]
    min_prop_it = 200
    max_prop_it = 0
    for i in range(1, 10):
        all_prns = 0
        prop_he = 0
        prop_she = 0
        prop_they = 0
        prop_it = 0

        file = "data/set1/a" + str(i) + ".txt"
        (prns, prn, title) = most_freq_pronoun(file)

        for key in prns:
            all_prns += prns[key]

        # he she they it
        prop_he = float(prns["he"]) / all_prns * 100
        prop_she = float(prns["she"]) / all_prns * 100
        prop_they = float(prns["they"]) / all_prns * 100
        prop_it = float(prns["it"]) / all_prns * 100

        proportion_people[0] += prop_he
        proportion_people[1] += prop_she
        proportion_people[2] += prop_they
        proportion_people[3] += prop_it

        if prop_it < min_prop_it:
            min_prop_it = prop_it
        if prop_it > max_prop_it:
            max_prop_it = prop_it

    proportion_people[0] = proportion_people[0] / 9
    proportion_people[1] = proportion_people[1] / 9
    proportion_people[2] = proportion_people[2] / 9
    proportion_people[3] = proportion_people[3] / 9

    print("PEOPLE SET:")
    print("Average proportion of \"he\":", proportion_people[0])
    print("Average proportion of \"she\":", proportion_people[1])
    print("Average proportion of \"they\":", proportion_people[2])
    print("Average proportion of \"it\":", proportion_people[3])
    print("-----------------------------------------------")

    print("Minimum proportion of \"it\":", min_prop_it)
    print("Maximum proportion of \"it\":", max_prop_it)
    print("\n\n")


def get_it_prop_avg_not_people_sets():
    proportion_not_people = [0, 0, 0, 0]
    min_prop_it = 200
    max_prop_it = 0
    for i in range(2, 5):
        for j in range(1, 10):
            all_prns = 0
            prop_he = 0
            prop_she = 0
            prop_they = 0
            prop_it = 0

            file = "data/set" + str(i) + "/a" + str(j) + ".txt"
            # print(file)
            (prns, prn, title) = most_freq_pronoun(file)

            for key in prns:
                all_prns += prns[key]

            # he she they it
            prop_he = float(prns["he"]) / all_prns * 100
            prop_she = float(prns["she"]) / all_prns * 100
            prop_they = float(prns["they"]) / all_prns * 100
            prop_it = float(prns["it"]) / all_prns * 100

            proportion_not_people[0] += prop_he
            proportion_not_people[1] += prop_she
            proportion_not_people[2] += prop_they
            proportion_not_people[3] += prop_it

            if prop_it < min_prop_it:
                min_prop_it = prop_it
            if prop_it > max_prop_it:
                max_prop_it = prop_it

    proportion_not_people[0] = proportion_not_people[0] / 27
    proportion_not_people[1] = proportion_not_people[1] / 27
    proportion_not_people[2] = proportion_not_people[2] / 27
    proportion_not_people[3] = proportion_not_people[3] / 27

    # print(proportion_not_people)
    print("NON-PEOPLE SETS:")
    print("Average proportion of \"he\":", proportion_not_people[0])
    print("Average proportion of \"she\":", proportion_not_people[1])
    print("Average proportion of \"they\":", proportion_not_people[2])
    print("Average proportion of \"it\":", proportion_not_people[3])
    print("-----------------------------------------------")

    print("Minimum proportion of \"it\":", min_prop_it)
    print("Maximum proportion of \"it\":", max_prop_it)

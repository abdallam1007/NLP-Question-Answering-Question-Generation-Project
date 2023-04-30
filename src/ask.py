import sys
import random
from pattern.en import *
from nltk.parse import stanford
from nltk.corpus import wordnet as wn
from nltk import pos_tag, word_tokenize, sent_tokenize

# Define the path to the Stanford Parser jar file
stanford_parser_jar = 'libs/stanford-corenlp-4.5.4/stanford-corenlp-4.5.4.jar'

# Define the path to the Stanford Parser models jar file
stanford_parser_models_jar = 'libs/stanford-corenlp-4.5.4/stanford-corenlp-4.5.4-models.jar'

# Create a Stanford Parser object
parser = stanford.StanfordParser(
    path_to_jar=stanford_parser_jar,
    path_to_models_jar=stanford_parser_models_jar
)

# list of auxiliary verb
aux = ["have", "do", "be", "can", "could", "will", "would", "shall", "should", "may", "might", "must"]

# list of location words
location_words = ["in", "at", "from", "to", "through", "above", "under", "on"]

# list of time words
time_words = ["at", "in", "on", "until", "starting", "by", "for", "beginning", "ending", "lasting", "since"]

# pattern.en functions raise error the first time they're called
def safe_lemma(s):
    try:
        lemma(s)
    except:
        pass
    return lemma(s)

def safe_tenses(s):
    try:
        tenses(s)
    except:
        pass
    return tenses(s)

def safe_conj(v, tns, prs, nmb, mod, asp, ng = False, par = True):
    try:
        conjugate(v, tense=tns, person=prs, number=nmb, mood=mod,
                  aspect=asp, negated=ng, parse=par)
    except:
        pass
    return conjugate(v, tense=tns, person=prs, number=nmb, mood=mod,
                     aspect=asp, negated=ng, parse=par)

# keep ONE of each valid form of "do", can't start question with "done"/"doing"
def remove_dup_pp(l):
    l = list(dict.fromkeys(l))
    if "done" in l:
        l.remove("done")
    if "doing" in l:
        l.remove("doing")
    return l

# gets the wordnet synset of the word to get the supersense
def get_supersense(word):
    synsets = wn.synsets(word)
    if synsets:
        synset = synsets[0]
        supersense = synset.lexname()
        return supersense
    else:
        return None

# returns the string the tree represents
def tree_to_str(t):
    t_flat = t.flatten()
    t_str = ""
    for i in range(len(t_flat)):
        t_str += t_flat[i] + " "
    return t_str[:-1]

# returns the tree as a pos tagged list of words
def pos_tag_a_tree(t):
    t_str = tree_to_str(t)
    tok = word_tokenize(t_str)
    pos = pos_tag(tok)
    return pos

# returns true is there is a noun in this sentence that refers to a person
def is_person(pos_tags):
    for (s, pos) in pos_tags:
        if pos in ["NN", "NNS", "NNP"]:
            ss = get_supersense(s)
            if ss == None or ss.split(".")[1] == "person":
                return True
    return False

# returns the first noun that occurs after the index provided
def find_next_noun(pos_tags, ind):
    for i in range(ind, len(pos_tags)):
        if pos_tags[i][1] in ["NN", "NNS", "NNP"]:
            return pos_tags[i][0]
    return None

# find a prepositional phrase that refers to a location and returns the
# sentence up until that phrase
def find_loc_pp(t):
    t_lst = pos_tag_a_tree(t)
    i = 0
    found = 0
    while(i < len(t_lst) and not found):
        if t_lst[i][0] in location_words:
            noun = find_next_noun(t_lst, i)
            if not noun:
                return None
            ss = get_supersense(noun)
            if ss:
                ss = ss.split(".")[1]
            else:
                return None

            if ss == "location":
                return t_lst[1 : i]

        i += 1

    return None

# find a prepositional phrase that refers to a time and returns the
# sentence up until that phrase
def find_time_pp(t):
    t_lst = pos_tag_a_tree(t)
    i = 0
    found = 0
    while(i < len(t_lst) and not found):
        if t_lst[i][0] in time_words:
            noun = find_next_noun(t_lst, i)
            if not noun:
                return None
            ss = get_supersense(noun)
            if ss:
                ss = ss.split(".")[1]
            else:
                return None

            if ss == "time":
                return t_lst[1 : i]

        elif t_lst[i][0] == "during":
            return t_lst[1 : i]

        i += 1
    return None


# create Yes/No questions
def make_bin_question(np_lst, vp_lst, verb):
    # converting np and vp to string for final question
    np_str = ""
    for i in range(len(np_lst)):
        if i < len(np_lst) - 1 and not np_lst[i + 1].isalnum() :
            add = ""
        else:
            add = " "

        np_str = np_str + np_lst[i] + add
    pos = pos_tag(word_tokenize(np_str))

    vp_str = ""
    for i in range(1, len(vp_lst)):
        if i < len(vp_lst) - 1 and not vp_lst[i + 1].isalnum() :
            add = ""
        elif i < len(vp_lst) - 1:
            add = " "
        else:
            add = "?"

        vp_str = vp_str + vp_lst[i] + add

    # chech if the root verb of the sentence is an auxiliary verb
    verb_lemma = safe_lemma(verb)

    if (verb_lemma in aux) or verb == "could":
        q = verb.capitalize() + " " + np_str[0].lower() + np_str[1:] + vp_str

    else:
        # if not auxiliary conjugating "do" is necessary
        verb_tenses = safe_tenses(verb)
        to_do = []

        for (tns, prs, nmb, mod, asp) in verb_tenses:
            conj_do = safe_conj("do", tns, prs, nmb, mod, asp)
            to_do.append(conj_do)

        to_do = remove_dup_pp(to_do)

        if to_do == []:
            return None

        q = to_do[0].capitalize() + " " + np_str[0].lower() + np_str[1:] + verb_lemma + " " + vp_str

    return q

def make_who_question(vp_str, verb):
    verb_lemma = safe_lemma(verb)
    q = "Who " + verb + " " + vp_str
    return q

def make_where_question(np_str, pp, verb):
    vp_str = ""
    for (s, t) in pp:
        vp_str += s + " "

    verb_lemma = safe_lemma(verb)

    verb_tenses = safe_tenses(verb)
    to_do = []

    for (tns, prs, nmb, mod, asp) in verb_tenses:
        conj_do = safe_conj("do", tns, prs, nmb, mod, asp)
        to_do.append(conj_do)

    to_do = remove_dup_pp(to_do)

    if to_do != []:
        q = "Where " + to_do[0] + " " + np_str.lower() + " " + verb_lemma + " " +  vp_str[:-1] + "?"
        return q

    return None

def make_when_question(np_str, pp, verb):
    vp_str = ""
    for (s, t) in pp:
        vp_str += s + " "

    verb_lemma = safe_lemma(verb)

    verb_tenses = safe_tenses(verb)
    to_do = []

    for (tns, prs, nmb, mod, asp) in verb_tenses:
        conj_do = safe_conj("do", tns, prs, nmb, mod, asp)
        to_do.append(conj_do)

    to_do = remove_dup_pp(to_do)

    if to_do != []:
        q = "When " + to_do[0] + " " + np_str.lower() + " " + verb_lemma + " " +  vp_str[:-1] + "?"
        return q

    return None

def make_what_question(np_str, vp_str, verb):
    verb_lemma = safe_lemma(verb)

    verb_tenses = safe_tenses(verb)
    to_do = []

    for (tns, prs, nmb, mod, asp) in verb_tenses:
        conj_do = safe_conj("do", tns, prs, nmb, mod, asp)
        to_do.append(conj_do)

    to_do = remove_dup_pp(to_do)

    if to_do != []:
        q = "What " + to_do[0] + " " + np_str.lower() + " " + verb_lemma + "?"
        return q

    return None

def make_questions(t):
    questions = {"bin": [], "who": [], "where": [], "when": [], "what": []}
    # restrict the type of sentences we work on to (NP, VP, .) sentences =
    # simple predicate sentences
    if len(t[0]) != 3:
        return (False, None)

    np = t[0][0]
    vp = t[0][1]
    pd = t[0][2]

    if np.label() != "NP" or vp.label() != "VP" or pd.label() != ".":
        return (False, None)

    np_flat = np.flatten()
    vp_flat = vp.flatten()
    verb = vp_flat[0]

    np_str = ""
    for i in range(len(np_flat)):
        if i < len(np_flat) - 1 and not np_flat[i + 1].isalnum() :
            add = ""
        elif i == len(np_flat) - 1:
            add = ""
        else:
            add = " "

        np_str = np_str + np_flat[i] + add

    vp_str = ""
    for i in range(1, len(vp_flat)):
        if i < len(vp_flat) - 1 and not vp_flat[i + 1].isalnum() :
            add = ""
        elif i < len(vp_flat) - 1:
            add = " "
        else:
            add = "?"

        vp_str = vp_str + vp_flat[i] + add

    q = make_bin_question(np_flat, vp_flat, verb)
    if q:
        questions["bin"].append(q)

    prep_phr_l = find_loc_pp(vp)
    prep_phr_t = find_time_pp(vp)

    added = 0
    np_pos = pos_tag_a_tree(np)
    if np_pos[0][1] == "PRP" or is_person(np_pos):
        q = make_who_question(vp_str, verb)
        if q:
            questions["who"].append(q)
            added += 1
    if prep_phr_l:
        q = make_where_question(np_str, prep_phr_l, verb)
        if q:
            questions["where"].append(q)
            added += 1
    if prep_phr_t:
        q = make_when_question(np_str, prep_phr_t, verb)
        if q:
            questions["when"].append(q)
            added += 1
    if added == 0:
        q = make_what_question(np_str, vp_str, verb)
        if q:
            questions["what"].append(q)

    return questions

def update_questions(questions, new_questions):
    for key in questions.keys():
        if key in new_questions:
            questions[key].extend(new_questions[key])
    return questions

def choose_questions(questions, n, percentages):
    result = []
    remaining = n
    for key, percentage in percentages.items():
        num = int(percentage * n)
        if num > len(questions[key]):
            num = len(questions[key])
        result += random.sample(questions[key], num)
        remaining -= num
    if remaining > 0:
        all_questions = [q for qs in questions.values() for q in qs]
        result += random.sample(all_questions, remaining)
    return result


def print_questions(questions):
    for i, question in enumerate(questions):
        print(f"{i+1}. {question}")

def questionGeneration(article, n):
    percentages = {"bin": 0.3, "who": 0.2, "where": 0.2, "when": 0.2, "what": 0.1}
    questions = {"bin": [], "who": [], "where": [], "when": [], "what": []}

    # Read the file
    with open(article, 'r') as file:
        article = file.read()

    # Tokenize the article into sentences
    sentences = sent_tokenize(article)

    # Parse the sentences to generate the questions
    for sentence in sentences:
        # Parse the sentence and get the parse tree
        for tree in parser.raw_parse(sentence):
            new_questions = make_questions(tree)
            update_questions(questions, new_questions)

    chosen_questions = choose_questions(questions, n, percentages)
    print_questions(chosen_questions)


questionGeneration(sys.argv[1], int(sys.argv[2]))

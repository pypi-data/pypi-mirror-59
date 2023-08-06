""" Attempt to associate a country with text (possibly) containing placenames 

Main entry points:

load_name_map(filename)

Load a prepared geonames map from filename. The parse-geonames.py script prepares the map from the GeoNames
allCountries.txt file.

load_stop_list(filename)

Load a list of phrases to ignore, one per line.

code(text, length=0)

Geocode all word sequences in the text up to length words. 
If length==0, geocode the entire text as a single blob.
Returns a (possibly-empty) list of matching ISO3 country codes.

Python usage:

    from ggeocode.coder import load_name_map, code

    load_name_map("name-map.lines.json")
    load_stoplist("stoplist.txt")

    result = code("Ottawa") # ['CAN']
    result = code("Ottawa KS") # ['USA']
    result = code("Belleville") # ['CAN', 'FRA', 'USA']

Command-line usage:

    $ python -m ggeocode.coder name-map.lines.json "Ottawa" "Ottawa KS" "LAX"

Started 2019-09 by David Megginson
This code is in the Public Domain.

"""

import argparse, json, logging, re, readline, sys


#
# Module variables
#

logger = logging.getLogger("geocode")
""" Logger for errors and messages. """

WS_PATTERN = re.compile('[\W\d_]+')
""" Precompiled regular expression for non-word characters. """

name_map = {}
""" Compiled map from GeoNames data """

stoplist = set()
""" List of normalised phrases to ignore """


#
# Utility functions
#

def normalise (s):
    """ Generate a normalised version of a string.
    @param s: the string to normalise
    @returns: the normalise string
    """
    return WS_PATTERN.sub(' ', s).lower().strip()


def merge_weight_map(main_map, merge_map, num_words):
    """ Merge a new weight map into an existing one.
    If the same key exists in both maps, add the values.
    @param main_map: the existing weight map (may be None)
    @param merge_map: the new weight map to merge (may be None)
    @param num_words: the number of words in the phrase (more words == higher)
    @returns: the union of the two maps, with values added.
    """

    # weighting formula for multi-word phrases
    factor = 1 + ((num_words - 1) * 2)
    logger.debug("%d words, factor %f", num_words, factor)
    
    if main_map is None:
        main_map = dict()

    for key in merge_map:
        if key in main_map:
            main_map[key] += merge_map[key] * factor
        else:
            main_map[key] = merge_map[key] * factor

    return main_map


def make_result (text, weight_map):
    """ Extract the (possibly-empty) list of country codes with the highest weight.
    Order is not significant.
    @param text: the original text
    @param weight_map: a weight map (country codes as keys, weights as values)
    @returns: a list of country codes (may be empty)
    """
    max_keys = []
    max_score = 0
    if weight_map:
        for key in weight_map:
            if weight_map[key] > max_score:
                max_keys = [key]
                max_score = weight_map[key]
            elif weight_map[key] == max_score:
                max_keys.append(key)
    return {
        "text": text,
        "status": True if max_score > 0 else False,
        "score": max_score,
        "countries": max_keys,
    }
        
#
# External entry points
#

def load_name_map (filename):
    """ Load the pre-compiled GeoNames map.
    The map is line-oriented JSON. Each line contains a JSON array with a normalised name as
    the first element, and a weight map as the second element. Use the parse-geonames.py
    script to create the file from the GeoNames allCountries.txt file.
    Will load the values into the module-global name_map dictionary.
    @param filename: the filename containing the line-oriented JSON.
    @see name_map
    """
    if not name_map:
        loaded_count = 0
        with open(filename) as input:
            logger.info("Loading database...")
            for line in input:
                entry = json.loads(line)
                name_map[entry[0]] = entry[1]
                loaded_count += 1
                if (loaded_count % 1000000) == 0:
                    logger.info("Read %d entries", loaded_count)

def load_stoplist(filename):
    """ Load a stoplist of words and phrases, one per line.
    Any phrase in this list will not be geocoded.
    @param filename: the filename containing the stop phrases
    @see stoplist
    """
    with open(filename) as input:
        logger.info("Loading stoplist...")
        for line in input:
            line = re.sub('#.*$', '', line)
            line = normalise(line)
            if line:
                stoplist.add(line)


def code (text, max_words=0):
    """ Return the most-likely list of country codes for a text string.
    You must call load_name_map() before invoking this function.
    Will normalise the text, then attempt to geocode multi-word phrases up to
    max_words words. If max_words is 0, then try to geocode all of the text as a 
    single string.
    For example, if max_words is 3 and the text string is "In Los Angeles, California"
    this function will try to geocode the following strings:
    "in los angeles"
    "los angeles california"
    "in los"
    "los angeles"
    "angeles california"
    "in"
    "los"
    "angeles"
    "california"
    @param text: the text string to geocode
    @param max_words: the maximum number of words in each phrase
    @returns: a (possibly-empty) list of country codes with the highest weight
    @see load_name_map
    """
    if not name_map:
        raise Exception("No name map loaded. You must call load_name_map(filename) first")

    # simplify the text (remove extra spaces and punctuation, and make lower case)
    text_norm = normalise(text)

    if max_words == 0:
        # 0 means just try to geocode the whole thing as a single string
        weight_map = name_map.get(text_norm)
    else:
        # an integer >0 means try variable-length phrases
        weight_map = None # map that will hold the merged results

        words = text_norm.split(" ") # make an array of words

        # test all phrases >= max_words words long
        for i in range(max_words, 0, -1):
            for j in range(0, len(words) - i + 1):
                # rejoin the phrase as a string
                key = " ".join(words[j:j+i])

                # skip single letters or phrases in the stoplist
                if len(key) == 1 or key in stoplist:
                    continue

                logger.debug("Trying %s...", key)
                result = name_map.get(key)
                if result:
                    logger.debug("Match: %s", result)
                    # merge into the combined weight map
                    weight_map = merge_weight_map(weight_map, result, i)
                    logger.debug("Current weight map: %s", str(weight_map))

    # return a (possibly-empty) list of the country codes with the highest weight
    return make_result(text, weight_map)


#
# Command-line script entry point: try to geocode all the arguments, or read strings from the console.
#

if __name__ == "__main__":

    # process args
    arg_parser = argparse.ArgumentParser(description="Geocode text (by country)")
    arg_parser.add_argument("-m", "--name-map", required=True, help="File containing pre-compiled name map.")
    arg_parser.add_argument("-w", "--max-words", type=int, default=3, help="Maximum phrase length to geocode (0 means do the whole string).")
    arg_parser.add_argument("-s", "--stoplist", help="File containing phrases to ignore (one per line).")
    arg_parser.add_argument(
        "-l", "--log-level",
        default="info",
        choices={"debug", "info", "warning", "error"},
        help="Level for logging messages (default: info)."
    )
    arg_parser.add_argument("strings", nargs="*", help="Text to geocode (if non supplied, read strings from command-line.")
    args = arg_parser.parse_args();

    # set up logging
    logging.basicConfig(level=args.log_level.upper())

    # load the pre-compiled map
    load_name_map(args.name_map)

    # load stoplist
    if args.stoplist:
        load_stoplist(args.stoplist)

    # geocode
    if len(args.strings) > 0:
        # We have strings to geocode on the command line
        for s in args.strings:
            print(json.dumps(code(s, max_words=args.max_words)))
    else:
        # We'll read input interactively from the console
        def read_input ():
            try:
                s = input("ggeocode> ")
                return s.strip().lower()
            except EOFError:
                print("Quitting...")
                sys.exit(0)

        while True:
            # Endless console loop
            s = read_input()
            if s == "exit":
                sys.exit(0)
            elif s in ("?", "h", "help"):
                print("Type a string you'd like to geocode (\"exit\" or Ctrl-D to exit)")
            else:
                print(json.dumps(code(s, max_words=args.max_words)))

# end

import json
from tqdm import tqdm


def load_alana_dataset(filename, lazy=False):
    """
    Loads the Alana dataset dump file either as an object or as a generator
    :param filename: the json file
    :param lazy: (optional) If set to True, this method becomes a generator yielding a line at a time.
    Use for larger datasets. Default = False
    :return: either a list of json objects (each is a session), or a generator or sessions
    """
    data = []
    # probably unnecessary and slow on large datasets
    with open(filename) as f:
        num_lines = sum(1 for line in f)

    if lazy == False:
        for line in tqdm(open(filename), total=num_lines, desc="Reading file..."):
            data.append(json.loads(line))
        return data
#    else:
#        for line in tqdm(open(filename), total=num_lines, desc="Reading file..."):
#            yield json.loads(line)


def get_user_system_pairs(filter_bots=None, data=None, preprocessed=False):
    """
    Extract user/system pairs from the Alana JSON dump dataset
    :param filter_bots: (optional) get only responses produced by a list of bot names
    :param data: the dataset input (list of raw Alana entries)
    :return: a json object with structure {session_id: [{user:..., system:...}, {...}]}
    """
    if not data:
        raise Exception("No dataset was given.")

    dataset = {}
    if isinstance(data, list):
        for item in tqdm(data, desc="Extracting u/s pairs..."):
            h = []
            for s in item['states']:
                try:
                    if filter_bots:
                        if list(s['state']['response'].keys())[0] in filter_bots:
                            h.append(
                                {'user': (s['state']['input']['text'] if not preprocessed else s['state']['nlu']['annotations']['processed_text']), 'system': list(s['state']['response'].values())[0]})
                    else:
                        h.append({'user': (s['state']['input']['text'] if not preprocessed else s['state']['nlu']['annotations']['processed_text']), 'system': list(s['state']['response'].values())[0]})
                except Exception as ex:
                    continue
            dataset[item['session_id']] = h
    return dataset

#    if isinstance(data, dict):
#        h = []
#        for s in data['states']:
#            try:
#                if filter_bots:
#                    if list(s['state']['response'].keys())[0] in filter_bots:
#                        h.append(
#                            {'user': s['state']['input']['text'], 'system': list(s['state']['response'].values())[0]})
#                else:
#                    h.append({'user': s['state']['input']['text'], 'system': list(s['state']['response'].values())[0]})
#            except:
#                continue
#        yield {data['session_id']: h}


def get_asr_filtered(min_asr=0, data=None):
    if not data:
        raise Exception("No dataset was given.")
    raise NotImplementedError


def get_rating_filtered(min_rating=0, data=None, operator='eq'):
    VALID_OPR = {'eq', 'gt', 'lt'}
    if operator not in VALID_OPR:
        raise ValueError(f"Operator must be one of {VALID_OPR}")

    if not data:
        raise Exception("No dataset was given.")

    dataset = []
    if isinstance(data, list):
        if operator == 'gt':
            dataset = [x for x in tqdm(data, desc="Filtered dialogues: ") if x.get('rating') and x['rating'] >= str(min_rating)]
            return dataset
        elif operator == 'eq':
            dataset = [x for x in tqdm(data, desc="Filtered dialogues: ") if x.get('rating') and x['rating'] == str(min_rating)]
            return dataset
        elif operator == 'lq':
            dataset = [x for x in tqdm(data, desc="Filtered dialogues: ") if ix.get('rating') and x['rating'] <= str(min_rating)]
            return dataset

    if isinstance(data, dict):
        raise Exception(f"Input given was {type(data)}")

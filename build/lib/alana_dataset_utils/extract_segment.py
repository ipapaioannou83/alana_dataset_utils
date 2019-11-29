import json
from tqdm import tqdm


def load_alana_dataset(filename):
    data = []
    # probably unnecessary and slow on slow datasets
    num_lines = sum(1 for line in open(filename))
    for line in tqdm(open(filename), total=num_lines):
        data.append(json.loads(line))
    return data


def get_user_system_pairs(filter_bots=None, data=None):
    """
    Extract user/system pairs from the Alana JSON dump dataset
    :param filter_bots: (optional) get only responses produced by a list of bot names
    :param data: the dataset input (list of raw Alana entries)
    :return: a json object with structure {session_id: [{user:..., system:...}, {...}]}
    """
    if not data:
        raise Exception("No dataset was given.")

    dataset = {}
    for item in tqdm(data):
        h = []
        for s in item['states']:
            try:
                if filter_bots:
                    if list(s['state']['response'].keys())[0] in filter_bots:
                        h.append(
                            {'user': s['state']['input']['text'], 'system': list(s['state']['response'].values())[0]})
                else:
                    h.append({'user': s['state']['input']['text'], 'system': list(s['state']['response'].values())[0]})
            except:
                continue
        dataset[item['session_id']] = h

    return dataset


def get_asr_filtered(min_asr=0, data=None):
    if not data:
        raise Exception("No dataset was given.")
    raise NotImplementedError

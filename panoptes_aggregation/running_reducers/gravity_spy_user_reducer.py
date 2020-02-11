'''
Gravity Spy User Reducer
------------------------
This module provides functions to calculate user weights for the Gravity Spy
project. Extracts are from caesar's `PluckFieldExtractor`.
'''
from .running_reducer_wrapper import running_reducer_wrapper

DEFAULTS = {
    'first_level': {'default': 'level_1', 'type': str},
    'level_config': {'default': None, 'type': dict}
}


@running_reducer_wrapper(defaults_data=DEFAULTS)
def gravity_spy_user_reducer(data, **kwargs):
    '''Calculate Gravity Spy user weights based on a confusion matrix
    from gold standard data.

    Parameters
    ----------
    data : list
        A list with one item containing the extract with the user's choice
        and the gold standard label.
    first_level : str
        A string containing the key for the first level in the `level_config` object
    level_config : dict
        This dictionary holds information about each level in the project.  The key must be
        strings and the values are a dict with up to three keys:
        * `workflow_id`: the workflow ID for the level
        * `new_categories`: the categories added in this level (not included for the final level)
        * `threshold`: the min value of `alpha` these categories need to trigger a level up
            (not included for the final level)
        * `next_level`: the key for the next level (not included for the final level)
        example:
            level_config = {
                'level_1': {
                    'workflow_id': 1,
                    'new_categories': [
                        'BLIP',
                        'WHISTLE'
                    ],
                    'threshold': 0.7,
                    'next_level': 'level_2'
                },
                'level_2': {
                    'workflow_id': 2
                }
            }

    store : keyword, dict
        A dictionary with two keys:

        * `confusion_matrix`: The confusion matrix for the user (stored as nested dict).
            The first key is the choice given by the user, the second key is the gold
            standard label.
        * `column_normalization`: The sum of each of the columns (used for normalization).
            i.e. The total number of time the user has vote for each choice.
        * `max_level`: The maximum workflow level of the user

    Returns
    -------
    reduction : dict
        A dictionary with four keys:

        * `alpha`: A dictionary of values indicating how well the user classifies each
            category they have seen gold standard images for (diagonal of the normalized
            confusion matrix).
        * `level_up`: Bool indicating if the user should level up (used to trigger effect)
        * `max_workflow_id`: The workflow ID for the user's highest unlocked level
        * `max_level`: The maximum workflow level of the user
        * `alpha_length`: The number of values in the `alpha` dict, used to make sure the
            user has seen every gold standard class of a level before being promoted
        * `normalized_confusion_matrix`: The column normalized confusion matrix for the user
        * `_store`: The updated store (see above)
    '''
    first_level_key = kwargs.pop('first_level')
    level_config = kwargs.pop('level_config')
    store = kwargs.pop('store')
    cm = store.get('confusion_matrix', {})
    n = store.get('column_normalization', {})
    level = store.get('max_level', first_level_key)
    user_label = data[0]['user_label']
    gold_label = data[0]['gold_label']
    cm.setdefault(user_label, {}).setdefault(gold_label, 0)
    cm[user_label][gold_label] += 1
    n.setdefault(user_label, 0)
    n[user_label] += 1
    normalized_confusion_matrix = {
        column_key: {
            row_key: row_value / n[column_key] for row_key, row_value in column_value.items()
        } for column_key, column_value in cm.items()
    }
    alpha = {key: value[key] for key, value in normalized_confusion_matrix.items() if key in value}
    level_up = False
    max_workflow_id = None
    if (level_config is not None) and (level in level_config):
        if {'workflow_id', 'new_categories', 'threshold', 'next_level'} <= level_config[level].keys():
            level_up = True
            for key in level_config[level]['new_categories']:
                level_up &= (alpha.get(key, 0) >= level_config[level]['threshold'])
            if level_up:
                level = level_config[level]['next_level']
            max_workflow_id = level_config[level]['workflow_id']
    return {
        'alpha': alpha,
        'level_up': level_up,
        'max_workflow_id': max_workflow_id,
        'max_level': level,
        'normalized_confusion_matrix': normalized_confusion_matrix,
        '_store': {
            'confusion_matrix': cm,
            'column_normalization': n,
            'max_level': level
        }
    }

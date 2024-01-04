import random
from typing import Any

class MoodAspect():
    '''
        MoodAspect: a class to capture different aspects of the mood of the person at the current moment
    '''
    @staticmethod
    def CreateMoodAspectUpdate(value, context, delta=True) ->list:
        return {'value':value, 'context': context, 'delta': delta}
    
    @property
    def name(self)->str:
        return self._name
    
    @property
    def description(self)->str:
        return self._description
    
    @property
    def range(self)->tuple:
        return (self._min, self._max)
    
    @property
    def value(self)->int:
        return self._value
    
    @value.setter
    def value(self, new_val)->None:
        if not isinstance(new_val, int):
            raise TypeError(f'Error setting mood value not int, actually a {type(new_val)}')
        self._value = max(min(new_val, self._max_val),self._min_val)
    
    def __getitem__(self, index)->Any:
        return self._context[index]

    def __setitem__(self, index, value)->None:
        self._context[index] = value

    def __len__(self)->int:
        return len(self._context)

    def __iter__(self)->Any:
        return iter(self._context)
    
    def append(self, value):
        if len(self._context) == self._context_len:
            lim = 1 - self._context_len
            self._context = self._context[lim:]
        self._context.append(value)


    def __init__(self, name, description, context_len=10, max_val=255, min_val=0, initial_value=-1)->None:
        #check all the input, trust no one!
        self.logger = logging.getLogger('logger.'+__name__)
        if not isinstance(name, str):
            raise TypeError(f'Name is not a string - type {type(name)}')
        if not isinstance(description, str):
            raise TypeError(f'Description is not a string - type {type(description)}')
        if not isinstance(max_val, int) or not isinstance(min_val, int) or not isinstance(initial_value, int):
            raise TypeError(f'Mood values are not ints max={type(max_val)}, min={type(min_val)}, init={type(initial_value)}')
        if max_val < min_val:
            raise Exception(f'max({max_val}) is not more than min({min_val})')
        if not isinstance(context_len, int) or context_len < 1:
            raise Exception(f'Context Length is not good - val:{context_len}, type:{type(context_len)}')
        #Now set all the values
        self._name = name
        self._description = description
        self._context = []
        self._max_val = max_val
        self._min_val = min_val
        self._value = initial_value
        if self._value == -1:
            self._value = random.randint(min_val, max_val)
        self._value = max(min(self._value, self._max_val),self._min_val)
        self._context_len = context_len

    def update_aspect(self, new_value, context=None, is_delta=True):
        if is_delta:
            self.value = self.value + new_value
        else:
            self.value = new_value

        if context:
            self.append(context)


class Mood:
    # Inspired by SIMS emotions (https://sims.fandom.com/wiki/Emotion).
    # Some have been removed (e.g. dazed) because they are irrelevant.

    @property
    def mood_aspect_count(self) -> int:
        return len(self._mood_aspects)
    
    @property
    def current_mood(self) -> tuple:
        ma_max = 0
        cm_list = []
        for key, ma in self._mood_aspects.items():
            if ma_max < ma.value:
                ma_max = ma.value
                cm_list=[ma.name]
            elif ma_max == ma.value:
                cm_list.append(ma.name)

        return (ma_max, tuple(cm_list))

        
    def __init__(self, mood_aspect_list):
        self.logger = logging.getLogger('logger.'+__name__)
        if not isinstance(mood_aspect_list, dict):
            raise TypeError(f'mood_aspect_list is not a dict - type:{type(mood_aspect_list)}')
        
        self._mood_aspects = {}

        for key, description in mood_aspect_list.items():
            if not isinstance(description, str):
                raise TypeError(f'description for mood aspect(key) is not a string - type:{type(description)}')

            self._mood_aspects[str(key)] = MoodAspect(str(key), description, initial_value=10)

    def update_mood_aspect(self, mood_aspect_name, value, context=None, delta=True)->None:
        if not mood_aspect_name in self._mood_aspects:
            raise KeyError(f'Mood Aspect {mood_aspect_name} not found in the list of mood aspects')
        if not isinstance(value, int):
            raise TypeError(f'New Mood value is not int, actual type:{type(value)}')
        self._mood_aspects[mood_aspect_name].update_aspect(value, context, delta) 

    def update_mood_aspects(self, update_dict)->None:
        ignore_err = True
        if not isinstance(update_dict, dict):
            raise TypeError(f'update dictionary is not type dict, actually type{type(update_dict)}')
        for key, update in update_dict.items():
            update_ok = True
            if not key in self._mood_aspects:
                if not ignore_err:
                    raise KeyError(f'Mood Aspect {key} not found in the list of mood aspects')
                update_ok = False
            elif not isinstance(update, dict):
                if not ignore_err:
                    raise TypeError(f'New Mood update is not dict, actual type:{type(update)}')
                update_ok = False
            elif not set(['value','context','delta']).issubset(set(update.keys())):
                if not ignore_err:
                    raise Exception(f'update does not have the right structure, keys are{update.keys()}')
                update_ok = False
            if update_ok:
                self.update_mood_aspect(key, update['value'], update['context'], update['delta'])
   

import random
from typing import Any

class MoodAspect():
    '''
        MoodAspect: a class to capture different aspects of the mood of the person at the current moment
    '''
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
    def __init__(self):
        self.current_mood = "Fine"  # Default to "Fine" (Neutral)

    # Inspired by SIMS emotions (https://sims.fandom.com/wiki/Emotion).
    # Some have been removed (e.g. dazed) because they are irrelevant.

    MOODS = [
        "Angry",
        "Energized",
        "Happy",
        "Bored",
        "Fine",
        "Focused",
        "Confident",
        "Inspired",
        "Uncomfortable"
    ]

    def update_mood(self, new_mood):
        if new_mood in Mood.MOODS:
            self.current_mood = new_mood
        else:
            print("Invalid mood.")

    def get_mood(self):
        return self.current_mood

    def randomize_mood(self):
        self.current_mood = random.choice(Mood.MOODS)

if __name__ == "__main__":

    agent = Mood()
    agent.randomize_mood()  # Randomly set the mood
    task = "Writing"
    print(f"{agent} is performing {task} task. Their current mood is {agent.get_mood()}.")

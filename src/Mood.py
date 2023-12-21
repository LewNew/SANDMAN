import random

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


agent = Mood()
agent.randomize_mood()  # Randomly set the mood
task = "Writing"
print(f"{agent} is performing {task} task. Their current mood is {agent.get_mood()}.")

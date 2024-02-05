tasks = [
    {"Break": "A short period of rest or relaxation"},
    {"Email": "Reading and responding to electronic messages"},
    {"Work": "Focused time on primary tasks or projects"},
    {"Lunch": "Designated time for eating a meal"},
    {"Meeting": "A scheduled discussion with others"},
    {"Call": "A conversation with someone over the phone"},
]

task_names = {list(task.keys())[0] for task in tasks}

# Naming: Why is call named call and not phone call?
# Compare with Gen Agents tasks for consistency
# English dictionary definitions for consistency
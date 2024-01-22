# Experiments

The scripts within this branch are used to perform experiments to evaluate the performance of LLMs with a simple 
question-and-answering (Q&A) task. The experiments are performed within the context of SANDMAN, therefore the task 
is centred around creating a daily plan in machine-readable form. For our current implementation, we have opted for 
a JSON format. This is a similar approach taken within related work.

## Prompts

This outlines the various prompts that we are currently working with. Commonalities that we anticipate will be 
present within all prompts are the following:

- They will always be explicit in their instructions (i.e., "Create me a daily plan ...")
- They will always pass in a list of available Tasks to choose from.
- They will always specify a given output format (i.e., JSON) and the structure of this output.

### Bootstrap Prompt

The Bootstrap Prompt is the 'baseline prompt'. It is the most bare-bones prompt that we use. It instructs the 
desired model to create a daily plan with no added context besides a list of tasks to choose from. It requests the 
output to be in JSON format, and provides the structure for this.

        user_msg = ("Create me a daily routine. The tasks are selected from \n"
                    f"the following list:\n{task_descriptions}\n"
                    "The output must be in JSON format: {'schedule': [{"
                    "'time': time, 'task': task}]}")

### Persona Prompt

The Persona Prompt is built upon the Bootstrap Prompt, but is more sophisticated because it passes in a persona. The 
persona is currently a simplistic description of the user that the model is instructed to create a daily plan for. 
The persona is described by three variables: 'organisation', 'role', and 'trait'.

        user_msg = (
            f"Create a daily routine for an individual who works in {org} as a {role} and is {trait}. "
            f"The tasks are selected from the following list:\n{task_descriptions}\n"
            "The output must be in the following JSON format with double "
            "quotes for keys: " '{"schedule": [{"time": time, "task": task}]}'
        )

- Organisation: The organisation the user works for. We currently have: Bank, University, Post Office
- Role: The role the user has within the organisation. Each organisation has 3 unique roles.
- Trait: The trait of the user. We currently have 10 traits. For each positive trait, there is a negative trait. For 
  instance, we have **ambitious** and **lazy**.
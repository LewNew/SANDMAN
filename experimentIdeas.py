job_role = "PhD"
description = "Your job role description here"
organisation = "Lancaster Uni"
traits = {"trait1": "Trait description here"}

formatted_string = f"job_role: {job_role}, job_role_description: {description}, organisation: {organisation}, organisation_description: {description}, traits: {traits}"

print(formatted_string)

"""
prompt1:
Create me a daily routeing from 9-5 in 5 minute intervals. The tasks are selected from

BreakTask
LunchTask
NothingTask
EmailTask
WebTask
WriteDocumentSpreadsheetTask
WriteDocumentPresentationTask
WriteCodeTask
WriteDocumentTask
ResearchTask
DataAnalysisTask

Their must be a logical selection of tasks and each task must also have a description to provide more context. The output must be in JASON format




prompt2:
Create me a daily routeing. The tasks are selected from

BreakTask: Takeing a break
LunchTask: Haveing lunch
NothingTask: Doing nothing
EmailTask: Work involving Reading and sending Emails
WebTask: Work involving browseing the internet
WriteDocumentSpreadsheetTask: Work involving Writeing Speadsheets
WriteDocumentPresentationTask: Work involving Writeing Presentation
WriteCodeTask: Work involving Writeing Code
WriteDocumentTask: Work involving Writeing Document
ResearchTask: Work involving Researching
DataAnalysisTask: Work involving Analysing Data

The output must be in JASON format: {"schedule": [{"time": time, "task": task}]}




#roles:
Bank:
1. Trader
2. Risk manager
3. Investment analyst
4. Financial advisor
5. Sales consultant
6. manager
7.advisor
 
University:
1. Resaercher
2. Professor
3. Student
 
post office:
1. manager
2. clerk
3. administrator
 
corporation
1.accountant
2.manager
3.researcher

#code
organisation = {
    'Bank': ['Trader', 'Risk manager', 'Investment analyst', 'Financial advisor', 'Sales consultant', 'Manager', 'Advisor'],
    'University': ['Researcher', 'Professor', 'Student'],
    'Post Office': ['Manager', 'Clerk', 'Administrator'],
    'Corporation': ['Accountant', 'Manager', 'Researcher']
}



Traits form sims:
Ambitious
Cheerful
Childish
Clumsy
Creative
erratic
self-Assured
Rude
Stubborn

other traits:
...

"""
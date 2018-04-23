def teacherPosts():
    teacherposts = [
        {
            "id": 1,
            "title": "Template Post",
            "body": "On the last quiz set date: dd/mm/yyyy, these are the things that everyone struggled with, these are tips most of you can benefit from.",
            "author": "Mr Smith",
            "create_date": "dd/mm/yyyy"
        },
        {
            "id": 2,
            "title": "Template Post2",
            "body": "On the last quiz set date: dd+1/mm/yyyy, these are the things that everyone struggled with, these are tips most of you can benefit from.",
            "author": "Mr Smith",
            "create_date": "dd+1/mm/yyyy"
        }
    ]
    return teacherposts

def quizzes():
    quizzes = [
        {
            "quizid":1,
            "Topic": "Data Representation",
            "Topicid": 1,
            "question1":2,
            "question2":3,
            "question3":4
        },
        {
            "quizid":2,
            "Topic": "Hardware",
            "Topicid": 2
        }
    ]
    return quizzes
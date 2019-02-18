from flask import Flask, url_for, request, render_template;
from app import app;
import redis;

# Connect to redis data store
r = redis.StrictRedis(host='localhost', port=6379, db=0, charset="utf-8", decode_responses=True);

#server/
@app.route('/')
def hello():

    #alternate ways to connect to redis, each command is equivalent
    #r = redis.StrictRedis();
    #r = redis.StrictRedis('localhost', 6379, 0);
    '''Renders a sample page.'''
    createLink = "<a href ='" + url_for('create') + "'>Create a question</a>";
    return """<html>
              <head>
                <title> Hello, world</title>
              </head>
              <body>
                """ + createLink + """
              </body>
           </html>""";

#server/create
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        #send the user the form
        return render_template('CreateQuestion.html');
    elif request.method == 'POST':
        #read form data and save it
        title = request.form['title'];
        question = request.form['question'];
        answer = request.form['answer'];

        # Store data in data store
        # Key name will be whatever title they typed in: Question
        # e.g. Music: question countries: question
        # e.g. music: answer countries: answer

        r.set(title + ':question', question)
        r.set(title + ':answer', answer)

        return render_template('CreatedQuestion.html', question = question);
    else:
        return "<h2>Invalid method</h2>"


#server/question/<title>
@app.route('/question/<title>', methods=['GET', 'POST'])
def question(title):
    if request.method == 'GET':
        # send the user the form
        #Read question from data store
        #Code here
        question = r.get(title+':question')

        return render_template('AnswerQuestion.html', question = question)
    elif request.method == 'POST':
        # User has attempeted answer. Check if they're correct
        submittedAnswer = request.form['submittedAnswer'];

        # Read answer from data Store
        # Code here

        answer = r.get(title+':answer')

        if submittedAnswer == answer:
            return "Correct!"
            #return render_template('Correct.html');
        else:
            return render_template('Incorrect.html', submittedAnswer = submittedAnswer, answer = answer);
    else:
        return "<h2>Invalid request<h2>";

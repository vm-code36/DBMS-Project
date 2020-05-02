# server.py
from flask import Flask, render_template, url_for, redirect, flash
from flask import jsonify
from flask import request
import mysql.connector
import errorCodes
import json
import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
import email_validator

from forms import AddStudentForm, BookIssueForm, BookReturnForm


app = Flask(__name__)
app.config['SECRET_KEY'] = '6fa405d4c8a116dfd32a28f5ca6d886d'

cnx = mysql.connector.connect(user='root', password='root@3636',database='library',charset='utf8')
cursor = cnx.cursor(prepared=True)



@app.route("/addstudent",methods=['GET', 'POST'])
def addstudent():
    form = AddStudentForm()
    query = "select count(student_id) + 1 from students;"
    prefix = 'ID'
    cursor.execute(query)
    row = cursor.fetchone()
    temp = str(row[0])
    student_id_temp = ''
    for i in range(len(temp),6):
        student_id_temp = student_id_temp + '0'
    student_id = prefix+student_id_temp+temp
    query = "INSERT into STUDENTS(student_id,first_name,last_name,email) values(%s,%s,%s,%s)"
    try:
        cursor.execute(query,(student_id,form.firstname.data,form.lastname.data,form.email.data))
        cnx.commit()
        flash(f'Student {student_id} Added','success')
        return redirect(url_for('searchBook'))
    except mysql.connector.Error as err:
        if(err.errno in errorCodes.errorCodeMessage):
            flash(errorCodes.errorCodeMessage[err.errno],'error')
        else:
            flash ('STUDENT Creation failed','error')
    return render_template("register.html", title='Register', form=form)

@app.route('/')
@app.route("/searchBook",methods=['GET', 'POST'])
def searchBook():
    query1 = 'select books.isbn, books.title, authors.name, books.status from books left outer join book_authors on books.isbn = book_authors.isbn left outer join authors on book_authors.author_id = authors.author_id'
    
    cursor.execute(query1)

    books = cursor.fetchall()

    return render_template('library.html', books=books)


@app.route("/issuebook/<isbn>",methods=['GET', 'POST'])
def issueBook(isbn):
    form = BookIssueForm()
    student_id = form.student_id.data
    try:
        query = 'select 1 from STUDENTS where student_id = %s'
        cursor.execute(query,(student_id,))
        isSTUDENT = 0
        for row in cursor:
            isSTUDENT = row[0]
        if(isSTUDENT):
            query = 'select status from BOOKS where isbn = %s'
            checkout_status = 1
            cursor.execute(query,(isbn,))
            for row in cursor:
                checkout_status = row[0]
            query = 'select count(*) >= 3 from BOOK_ISSUED where student_id = %s and date_return is null'
            isCountExceeded = 1
            cursor.execute(query,(student_id,))
            for row in cursor:
                isCountExceeded = row[0]
            if(checkout_status):
                flash(f'{isbn} already checked out', 'error')
            elif(isCountExceeded):
                flash(f'Maximum limit of 3 reached. {student_id} cannot checkout','error')
            else:
                query1 = 'Insert into BOOK_ISSUED values(0,%s,%s,%s,%s,null)'
                query2 = 'update BOOKS set status = True where isbn = %s'
                dateOut = datetime.date.today()
                dueDate = dateOut + datetime.timedelta(days=14)
                cursor.execute(query1,(isbn,student_id,dateOut,dueDate))
                cursor.execute(query2,(isbn,))
                cnx.commit()
                flash(f'{isbn} Checked Out','success')
                return redirect(url_for('searchBook'))
        else:
            flash(f'{student_id} is Invalid', 'error')
    except mysql.connector.Error as err:
        if(err.errno in errorCodes.errorCodeMessage):
            flash(errorCodes.errorCodeMessage[err.errno], 'error')
        else:
            flash('book issue is failed','error')

    return render_template('issuebook.html', isbn=isbn, form=form)


@app.route("/checkinBook",methods=['GET', 'POST'])
def checkinBook():
    form = BookReturnForm()
    isbn = form.isbn.data
    issue_id = 0
    query = 'SELECT issue_id FROM LIBRARY.BOOK_ISSUED where date_return is null and isbn = (%s)'
    try:
        cursor.execute(query,(isbn,))
        for row in cursor:
            issue_id = row[0]
        if(issue_id):
            query1 = 'update BOOK_ISSUED set date_return = curdate() where issue_id = (%s)'
            query2 = 'update BOOKS set status = False where isbn = (select isbn from BOOK_ISSUED where issue_id = (%s))'
            cursor.execute(query1,(issue_id,))
            cursor.execute(query2,(issue_id,))
            cnx.commit()
            flash(f'{isbn} is Checked In', 'success')
            return redirect(url_for('searchBook'))
        else:
            flash(f"{isbn} is already checked in", 'error')
    except mysql.connector.Error as err:
        if(err.errno in errorCodes.errorCodeMessage):
            flash(errorCodes.errorCodeMessage[err.errno], 'error')
        else:
            flash(f'{isbn} Check In fail', 'error')
    return render_template('return.html', form=form)


if __name__ == "__main__":
    app.run()

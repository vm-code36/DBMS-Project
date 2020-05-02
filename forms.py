from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
import email_validator


#CREATE TABLE STUDENTS(student_id VARCHAR(10) primary key ,first_name VARCHAR(100) NOT NULL,last_name VARCHAR(100) NOT NULL,email VARCHAR(1000) NOT NULL);
class AddStudentForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    lastname = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Add')

    def validate_email(self, email):
        query = "select * from STUDENT where email = email"
        student = cursor.execute(query)
        if student:
            raise ValidationError('That email is taken. Please choose a different one.')


class BookIssueForm(FlaskForm):
    isbn = StringField('ISBN')
    student_id = StringField('StudentId', validators=[DataRequired(), Length(min=0, max=10)])
    submit = SubmitField('Request')

class BookReturnForm(FlaskForm):
    isbn = StringField('ISBN')
    submit = SubmitField('Return')

class Surveyplatform():
    email = EmailField('Email address', [validators.InputRequired(), validators.Email()])
    password = PasswordField('Password', [
            validators.InputRequired(),
            validators.Length(min=4, max=80)
        ])
    confirm = PasswordField('Re-type Password', [
            validators.EqualTo('password', message='Passwords must match'),
    ])

# Cyber Security Base: Project I

The project is implemented with Django and Python. It can be run with the command “python manage.py runserver” while being in the project folder. The initial base for the project was done with the help of the Django tutorial that was linked in the course material. I did the base for the Poll app, but added users so that they can register accounts, log in, log out and only make polls and vote on them if they are logged in. 

## FLAW 1: OWASP A01:2021 – Broken Access Control
The flaw can be found at users/views.py (https://github.com/jennavahtera/cybersecurityproject1/blob/main/project/users/views.py) starting at line 37 until line 56. The login view generates a message to the person trying to login and the message shows too much information to the unauthorised user. This is an example of one of the mapped CWEs in Broken Access Control, the CWE-200: Exposure of Sensitive Information to an Unauthorized Actor. If there doesn’t exist such username that the person is trying for, the message is “Invalid username.”. If there exists the specific username, but the password is not correct for that user, the message is “Invalid password.” The problem is fixed if lines 41-56 are deleted and lines 58-73 are commented out. In the fix, Django’s own form validation is used (line 59) and also the error messages (lines 68 & 73) don’t specify whether the username or the password is incorrect. 

## FLAW 2: OWASP A03:2021 - Injection
The flaw can be found at polls/views.py at create_question method (https://github.com/jennavahtera/cybersecurityproject1/blob/main/project/polls/views.py) starting at line 65. When a user is creating a new poll, the poll question can be whatever, it isn’t validated at all. It can be so long, that only one poll fills up the whole page and other user has to scroll to even see any other polls. Even in the poll page the voting options are under the question, and they aren’t seen by the user, This is an example of one of the mapped CWEs in Injection, the CWE-20: Improper Input Validation. This can be fixed by giving some kind of restrictions for the poll question. If code lines 74-79 are commented out, then the poll questions can only be under 200 characters. If it’s more than that, then the user gets a message that says to shorten the question to under 200 characters. At this point, I think limiting the length of the question is the most important validation needed, but later on more validations can be added, like for example not allowing offensive words in the question etc.

## FLAW 3: OWASP A05:2021 – Security Misconfiguration (and also A04:2021 – Insecure Design)
This flaw can be found at settings.py (https://github.com/jennavahtera/cybersecurityproject1/blob/main/project/mysite/settings.py) at line 30. When the DEBUG setting is left to True, it leaves the app in a vulnerable state. It should be set to True only in the development phase, never in production. This is at it’s core a Security Misconfiguration concern, but I noticed that this can lead to other security flaws in other OWASP categories as well. I also have a flaw that the homepage of the polls app isn’t included in the urls.py (https://github.com/jennavahtera/cybersecurityproject1/blob/main/project/mysite/urls.py) line 26. When the DEBUG is set to true and the user tries to go to that address, it shows an error message 404 that shows the whole url composition of the site. This is an example of one of the mapped CWEs of OWASP A04:2021 - Insecure Design, specifically CWE-209 Generation of Error Message Containing Sensitive Information. This can be fixed mainly by changing the DEBUG to False (at settings.py, the line 30 should be commented and 31 commented out). Then the homepage should be included in urls (commenting out line 26 in urls.py).

## FLAW 4: OWASP A07:2021 – Identification and Authentication Failures
This flaw can be found at settings.py (https://github.com/jennavahtera/cybersecurityproject1/blob/main/project/mysite/settings.py) starting at line 96 until line 116 (most lines are comments). In this project, the passwords aren’t validated at all. They can be however long, have whatever characters, like only numbers for example. The passwords can also be the same as the username or they can be common and too vulnerable passwords, like “admin” for example. This is an example of one of the mapped CWEs in Identification and Authentication Failures, the CWE-521 Weak Password Requirements. This can be fixed with commenting out the lines 104-115, since Django already offers these tools for password validation.

## FLAW 5: OWASP A09:2021 – Security Logging and Monitoring Failures
This flaw can be found at users/views.py (https://github.com/jennavahtera/cybersecurityproject1/blob/main/project/users/views.py). The flaw is basically the whole page since it is that there isn’t logging at all, which is an example of one the mapped CWEs in Security Logging and Monitoring Failures, the CWE-778 Insufficient Logging. This can be fixed by adding some kind of logging. The fixes are commented out. First, the loggers are imported and added (lines 12-13). The fixes to this problem are included in the commented fix to flaw 1, but they aren’t needed to fix flaw 1. I just wanted to add them to the code where flaw 1 is also already fixed. Logging information can be gotten by commenting out lines 69 and 72. This logs messages whenever someone tries to login with wrong credentials. Furthermore, it gives the username of the user that is trying to log in. I think more logging could always be added, but I think in my app for now, the most important things to log are people trying to get in with more credentials, and to see the username of the account that someone tries to get in. 

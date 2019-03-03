# Exam Application
**Caution!** This code was created to be a attachment for a job application. It is not suitable for commercial purposes. If you find something interesting in it, please do not hesitate to reuse.


#### Table of Contents

1. Instalation
2. Introduction
3. Application stack overview
4. Api documentation

### 1. Instalation
The repository contains all the data required to run the application.
Please ensure that you have available ports: 80 and 8000.
To start application just run listed below commands.
```
git clone git@github.com:Michael-Wisniewski/rest-api.git
cd rest-api
docker-compose -f docker-compose.yml -f docker-compose.production.yml up
```
Test coverage
```
url: http://localhost:80/tests
```
Schoolboy's account app.
```
url: http://localhost:8000
login: schoolboy
password: schoolboy
```
Teacher's account app.
```
url: http://panel.localhost:8000
login: teacher
password: teacher
```
Users accounts
```
url: http://localhost:80/admin
login: headmaster
password: headmaster
```
### 2. Introduction
**"Exam App"** is a web application which allows students and teacher to create and exchange exam tests.
It was created in accordance with the RESTful application program interface rules.

<p align="center">
    <img src="./doc/use_case.svg">
</p>

    Application features:

    Schoolboy
        - authenticate account
        - viewing the available exams (include information about author and difficulty)
        - taking exam
        - getting exam result

    Teacher
        - authenticate account
        - viewing exam sheets (include information about exam's pass rate)
        - creating and managing of exams sheets

    Headmaster
        - managing of user accounts

    Other assumptions
        - exams are single choice tests
        - question has assigned score from 1 to 5 points
        - 60% score passes the exam
        - exam sheet can only be archived, not deleted
        - exams are single choice tests
        - exam sheets are versioned so exam result can not be saved
          if during the filling process, teacher makes any changes to it

### 3. Application stack overview

General

| Type        | Technologies           |
| ------------- |:-------------:|
| Version control system  | Git, Git Flow |
| Virtual enviromnent | Docker, Docker-Compose |

RESTful Api

| Type        | Technologies           |
| ------------- |:-------------:|
| Servers | Nginx, uWsgi |
| Database | PostgreSQL |
| Programming language | Python v.3.6 |
| Used libraries | Django, Django REST, Jsonschema |
| Debug tools | Postman |
| Tests | Pytest, Pytest-Django, Pytest-Cov, Mixer, RequestFactory |

### 4. Api documentation





#### Authentication of users.
----
  Returns a pair of keys to authenticate.

* **URL**

  localhost/v1/api/token/

* **Method:**

  `POST`
  
*  **URL Params**

   None

* **POST request:**

  * **Content:**
    ```json
        { "username": "admin", "password": "admin" }
    ```

    **Required:**
 
    `username=[string]`<br />
    `password=[string]`<br />

* **Success POST Response:**

  * **Code:** 200 <br />
    **Content:**
    ```json 
        {
            "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.....",
            "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9......."
        }
    ```
* **Error POST Response:**

  * **Code:** 400 <br />
    **Content:**
    ```json
        { "non_field_errors": [ "No active account found with the given credentials" ] }
    ```

    OR

  * **Code:** 400 <br />
    **Content:**
    ```json
        { "username": [ "This field is required." ],
          "password": [ "This field is required."]
        }
    ```
#### Refresh expired token.
----
  Returns the refreshed access token. Use "refresh" token received in authentication process.

* **URL**

  localhost/v1/api/token/refresh/

* **Method:**

  `POST`
  
*  **URL Params**

   None

* **POST request:**

  * **Content:**
    ```json
        { "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9....." }
    ```

    **Required:**
 
    `refresh=[string]`<br />

* **Success POST Response:**

  * **Code:** 200 <br />
    **Content:**
    ```json 
        { "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9......." }
    ```
* **Error POST Response:**

  * **Code:** 400 <br />
    **Content:**
    ```json
        {
            "detail": "Token is invalid or expired",
            "code": "token_not_valid"
        }
    ```

    OR

  * **Code:** 400 <br />
    **Content:**
    ```json
        { "refresh": [ "This field is required." ] }
    ```
#### Schoolboy exam list.
----
  Returns json data with information shortcut about all availables exams.

* **URL**

  localhost/v1/schoolboy/exam_list/

* **Method:**

  `GET`
  
*  **URL Params**

   None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:**
    ```json 
        [
            { 
                "title" : "Math exam",
                "author" : "Michael Bloom", 
                "difficulty": "Easy", 
                "url": "http://localhost/v1/schoolboy/new_exam/1/" 
            },
            { 
                "title" : "English exam",
                "author" : "John Smith", 
                "difficulty": "Medium", 
                "url": "http://localhost/v1/schoolboy/new_exam/2/" 
            }
        ]
    ```

    OR
    
  * **Code:** 204 <br />
    **Content:**
    ```json
        { "message" : "There are no exam sheets avalible at this moment." }
    ```

#### Schoolboy writes a new exam
----
  Returns blank exam in json data format. After receiving the data with answers it sends back the exam score.

* **URL**

  localhost/v1/schoolboy/new_exam/:id/

* **Method:**

  `GET` | `POST`
  
*  **URL Params**

  **Required:**
 
  `id=[integer]` - exam sheet id

* **Success GET Response:**

  * **Code:** 200 <br />
    **Content:**
    ```json 
        {
          "id": 1,
          "title": "Math exam",
          "version": 1,
          "questions": [
                {
                      "text": "How much is two plus two?",
                      "answers": [
                            {
                              "id": 1,
                              "text": "Three"
                            },
                            { 
                              "id": 2,
                              "text": "four"
                            }
                      ]
                }
          ]
        }
    ```
* **Error GET Response:**

  * **Code:** 404 <br />
    **Content:**
    ```json
        { "message" : "The exam sheet does not exist." }
    ```

    OR

  * **Code:** 404 <br />
    **Content:**
    ```json
        { "message" : "This exam is not avalible at this moment." }
    ```

    OR

  * **Code:** 410 <br />
    **Content:**
    ```json
        { "message" : "This exam is no longer avalible." }
    ```
* **POST request:**

  * **Content:**
    ```json
        { 
            "id": 1,
            "version": 3,
            "answers": [1,7]
        }
    ```

    **Required:**
 
    `id=[integer]` - exam sheet id<br />
    `version=[integer]` - version of exam sheet<br />
    `answers=[type=[array], items=[integer]]` - ids of answers
* **Success POST Response:**

  * **Code:** 200 <br />
    **Content:**
    ```json 
        { "message": "Your score is 75%" }
    ```
* **Error POST Response:**

  * **Code:** 406 <br />
    **Content:**
    ```json
        { "message" : "Corrupted data." }
    ```

    OR

  * **Code:** 406 <br />
    **Content:**
    ```json
        { "message" : "The exam sheet does not exist." }
    ```

    OR

  * **Code:** 406 <br />
    **Content:**
    ```json
        { "message" : "Wrong number of answers or answers do not correspond to questions." }
    ```

    OR

  * **Code:** 409 <br />
    **Content:**
    ```json
        { "message" : "Used exam sheet is out of date." }
    ```

    OR

  * **Code:** 410 <br />
    **Content:**
    ```json
        { "message" : "Used exam sheet is no loger avalible." }
    ```

    OR

  * **Code:** 410 <br />
    **Content:**
    ```json
        { "message" : "Used exam sheet was deleted." }
    ```

#### Teacher exam sheet list.
----
  Returns json data with information shortcut about exam sheets. New blank exam sheet can be created by POST method.

* **URL**

  localhost/v1/teacher/examsheet_list/

* **Method:**

  `GET` | `POST`
  
*  **URL Params**

   None

* **Success GET Response:**

  * **Code:** 200 <br />
    **Content:**
    ```json 
        [
            {
                "title": "Math exam",
                "available": true,
                "version": 13,
                "updated": "2019-02-26",
                "filled": 10,
                "passed": 5,
                "url": "http://localhost/v1/teacher/examsheet_edit/2/"
            },
            {
                "title": "English exam",
                "available": true,
                "version": 5,
                "updated": "2019-02-26",
                "filled": 4,
                "passed": 3,
                "url": "http://localhost/v1/teacher/examsheet_edit/1/"
            }
        ]
    ```

    OR
    
  * **Code:** 200 <br />
    **Content:**
    ```json
        { "message": "You did not add any exam sheets." }
    ```
* **POST request:**

  * **Content:**
    ```json
        { "title": "Math exam" }
    ```
* **Success POST Response:**

  * **Code:** 200 <br />
    **Content:**
    ```json 
        {
            "message": "Empty examsheet added.",
            "id": 12
        }
    ```
* **Error POST Response:**

  * **Code:** 406 <br />
    **Content:**
    ```json
        { "title": ["This field is required."] }
    ```

    OR

  * **Code:** 406 <br />
    **Content:**
    ```json
        { "title": ["This field may not be blank."] }
    ```

    OR

  * **Code:** 406 <br />
    **Content:**
    ```json
        { "title": ["exam sheet with this title already exists."] }
    ```
#### Teacher edits exam sheet
----
  Returns exam sheet in json data format. After receiving the data all information about exam can be updated. Exam can be archived by sending delete request.

* **URL**

  localhost/v1/teacher/exam_edit/:id/

* **Method:**

  `GET` | `POST` | `DELETE`
  
*  **URL Params**

  **Required:**
 
  `id=[integer]` - exam sheet id

* **Success GET Response:**

  * **Code:** 200 <br />
    **Content:**
    ```json 
        {
            "id": 1,
            "title": "Math exam",
            "available": true,
            "version": 3,
            "questions": [
                {
                    "id": 1,
                    "text": "How much is two plus two?",
                    "points": 3,
                    "answers": [
                        {
                            "id": 1,
                            "is_correct": true,
                            "text": "Four"
                        },
                        {
                            "id": 2,
                            "is_correct": false,
                            "text": "Three"
                        }
                    ]
                }
            ]
        }
    ```
* **Error GET Response:**

  * **Code:** 404 <br />
    **Content:**
    ```json
        { "message" : "The exam sheet does not exist." }
    ```

    OR

  * **Code:** 406 <br />
    **Content:**
    ```json
        { "message" : "You do not have rights to edit this examsheet." }
    ```

    OR

  * **Code:** 410 <br />
    **Content:**
    ```json
        { "message" : "This exam is no longer available." }
    ```
* **POST request:**

  * **Content:**
    ```json
         {
            "id": 1,
            "title": "Math exam",
            "available": true,
            "questions": [
                {
                    "id": 1,
                    "text": "How much is two plus two?",
                    "points": 3,
                    "answers": [
                        {
                            "id": 1,
                            "is_correct": true,
                            "text": "Four"
                        },
                        {
                            "id": 2,
                            "is_correct": false,
                            "text": "Three"
                        }
                        {
                            "id": 3,
                            "is_correct": false,
                            "text": "Three",
                            "delete": true
                        }
                    ]
                },
                {
                    "text": "How much is two minus two?",
                    "points": 4,
                    "answers": [
                        {
                            "is_correct": true,
                            "text": "Zero"
                        },
                        {
                            "is_correct": false,
                            "text": "One"
                        }
                    ]
                }
            ]
        }
    ```

    **Required:**
 
    `id=[integer]` - exam sheet id<br />
    `title=[string]` - title of exam sheet<br />
    `availavle=[bool]` - describes if exam is available to schoolboy

    **Optional params for question and answer objects:**
 
    `id=[integer]` - if not provided the application will create a new object<br />
    `delete=[bool]` - if provided the application will delete object<br /><br />

    In example shown above the answer with id=3 will be deleted and new question will be created.

* **Success POST Response:**

  * **Code:** 200 <br />
    **Content:**
    ```json 
        { "message": "Exam sheet set updated." }
    ```
* **Error POST Response:**

  * **Code:** 404 <br />
    **Content:**
    ```json
        { "message" : "The exam sheet does not exist." }
    ```

    OR

  * **Code:** 406 <br />
    **Content:**
    ```json
        { "message" : "Corrupted data." }
    ```

    OR

  * **Code:** 406 <br />
    **Content:**
    ```json
        { "message" : "Exam sheet with this title already exists." }
    ```

    OR

  * **Code:** 406 <br />
    **Content:**
    ```json
        { "message" : "Question does not correspond to exam sheet." }
    ```

    OR

  * **Code:** 406 <br />
    **Content:**
    ```json
        { "message" : "Answer does not correspond to question." }
    ```

    OR

  * **Code:** 406 <br />
    **Content:**
    ```json
        { "message" : "There must be at last two answers for every question." }
    ```

    OR

  * **Code:** 406 <br />
    **Content:**
    ```json
        { "message" : "There must be only one correct answer for every question." }
    ```

    OR

  * **Code:** 406 <br />
    **Content:**
    ```json
        { "message" : "Active exam has to have at lest one question." }
    ```

    OR

  * **Code:** 406 <br />
    **Content:**
    ```json
        { "message" : "You do not have rights to edit this examsheet." }
    ```

    OR

  * **Code:** 410 <br />
    **Content:**
    ```json
        { "message" : "This exam is no longer available." }
    ```
* **Success DELETE Response:**

  * **Code:** 200 <br />
    **Content:**
    ```json 
        { "message": "Exam sheet was deleted." }
    ```
* **Error DELETE Response:**

  * **Code:** 404 <br />
    **Content:**
    ```json
        { "message" : "The exam sheet does not exist." }
    ```

    OR

  * **Code:** 406 <br />
    **Content:**
    ```json
        { "message" : "You do not have rights to edit this examsheet." }
    ```

    OR

  * **Code:** 410 <br />
    **Content:**
    ```json
        { "message" : "This exam is no longer available." }
    ```
# rest-api









### 3. Application stack overview

General

| Type        | Technologies           |
| ------------- |:-------------:|
| Version control system  | Git, GitFlow |
| Virtual enviromnent | Docker and Docker-Compose |

RESTful Api

| Type        | Technologies           |
| ------------- |:-------------:|
| Servers | Nginx, uWsgi |
| Database | PostgreSQL |
| Programming language | Python v.3.6 |
| Used libraries | Django, Django REST, Jsonschema |
| Debug tools | Postman, DBeaver |
| Tests | Pytest, Pytest-Django, Pytest-Cov, Mixer, RequestFactory, Client |

Vue Api

| Type        | Technologies           |
| ------------- |:-------------:|
| Servers | XX |

| Programming language | Java Script |
| Used libraries | Vue, Vuex |
| Debug tools | Vue.js devtools, Eslint |
| Tests |  |


**Show schoolboy exam list.**
----
  Returns json data with information shortcuts about all availables exams.

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
        { "message" : "There are no exam sheets available at this moment." }
    ```

**The schoolboy writes a new exam**
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
                              "text": "three"
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
        { "message" : "This exam is not available at this moment." }
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
        { "message" : "Used exam sheet is no loger available." }
    ```

    OR

  * **Code:** 410 <br />
    **Content:**
    ```json
        { "message" : "Used exam sheet was deleted." }
    ```
  

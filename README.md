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
| Used libraries | Django, Django REST |
| Debug tools | Postman |
| Tests | Pytest, Pytest-Django, Pytest-Cov, Mixer, RequestFactory |




**Show schoolboy exam list.**
----
  Returns json data with information shortcuts about all availables exams.

* **URL**

  localhost/v1/schoolboy/exam_list/

* **Method:**

  `GET`
  
*  **URL Params**

   None

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:**
    ```JSONasPerl 
        [
            { 
                title : "Math exam",
                author : "Michael Bloom", 
                difficulty: "Easy", 
                url: "http://localhost/v1/schoolboy/new_exam/1/" 
            },
            { 
                title : "English exam",
                author : "John Smith", 
                difficulty: "Medium", 
                url: "http://localhost/v1/schoolboy/new_exam/2/" 
            }
        ]
    ```

    OR
    
  * **Code:** 204 <br />
    **Content:**
    ```json
        { 
            message : "There are no exam sheets avalible at this moment."
        }
    ```
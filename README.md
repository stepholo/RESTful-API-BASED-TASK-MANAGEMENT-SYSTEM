### RESTful API-BASED TASK MANAGEMENT SYSTEM

## Introduction
This project is a web service that allows users to manage their tasks using a task management API where users can create, update, delete tasks and set deadlines.
The project utilized Swagger for documentation and also laverages on the Swagger user interface to make it easier for the consumer.
- [Deployed site](http://16.171.57.238:5000/apidocs/#/)
- Project Blog Article [Blog](https://www.linkedin.com/pulse/revolutionizing-task-management-unveiling-our-innovative-stephen-oloo-dzokf%3FtrackingId=pcUEpgaPSZaPMm7U4FRoGw%253D%253D/?trackingId=pcUEpgaPSZaPMm7U4FRoGw%3D%3D)
- Linkedin Profile [Stephen](www.linkedin.com/in/stepholo0)

## Table of Content
* [Introduction](#Introduction)
* [Installation](#installation)
* [Usage](#usage)
* [Examples of console usage](#examples-of-console-usage)
* [Examples of curl usage](#examples-of-console-usage)
* [Authors](#authors)
* [License](#license)

## Installation
The API can be accessed through [Swagger](http://16.171.57.238:5000/apidocs/#/).
The platform provides a user friendly way of interacting with the API endpoint methods.

### Usage
Their are two methods of usage;
    - Using the console
    - curl method using the HTTP verbs - (GET, PUT, POST, DELETE)

## Examples of console usage
```bash
LENOVO@DESKTOP-JH999HJ MINGW64 ~/Desktop/RESTful API-BASED TASK MANAGEMENT SYSTEM (Development)
$ python3 console.py
Welcome to Task Command interpreter. Type `help` to view all commands
(task) help

Documented commands (type help <topic>):
========================================
EOF          delete_task  show_all_users               show_task_status
clear        delete_user  show_all_userspecific_tasks  update_task
create_task  help         show_specific_user           update_user
create_user  quit         show_task_priority

(task) help show_all_users
Show all users
            Usage: show_all_users User

(task) show_all_users User
0484b334-96ab-4c49-8f3a-e6a1fa81b863.John Doe - johndoe@example.com
2f910dd9-f8c5-4cbe-9631-38027b91e4c2.Stephen Oloo - stephen@hellotractor.com
ebcf49f5-e8c7-4066-8efb-ab34505c4ad9.Vera Akoth - beldineverah@gmail.com
f8d8fb5c-f319-4abf-8111-1a373b6fd6d1.Damaris Amondi - amondidamaris@gmail.com

(task) help show_all_userspecific_tasks
Show all task for a specific user
            usage: show_all_userspecifc_tasks oloobrian@gmail.com

(task) show_all_userspecifc_tasks johndoe@example.com
*** Unknown syntax: show_all_userspecifc_tasks johndoe@example.com

(task) show_all_userspecific_tasks johndoe@example.com
c79ed9fd-a55e-42f0-aeef-050c5cadb9fa. Code; study my books; status - done; priority - high; deadline - 2023-12-19 12:19:45
e95a81d2-dcf8-4129-bfa7-54841657354f. Play; play with cube; status - pending; priority - low; deadline - 2023-12-17 22:18:51

(task) show_all_userspecific_tasks stephen@hellotractor.com
158399dd-c6e7-4c63-a7f7-ff8eded5826d. Call; call renters; status - pending; priority - high; deadline - 2023-12-06 23:02:20
1dde760b-b39c-4dc0-a14e-6ab19548ebf5. Call; call renters; status - pending; priority - high; deadline - 2023-12-06 23:05:31
67c627e2-7040-4dcf-bbcd-4e4c643ea40b. Meeting; meet renters; status - pending; priority - low; deadline - 2023-12-07 23:09:45

(task)
```

## Examples of curl usage
```bash
LENOVO@DESKTOP-JH999HJ MINGW64 ~/Desktop/RESTful API-BASED TASK MANAGEMENT SYSTEM (Development)
curl -X GET "http://16.171.57.238:5000/api/v1/users" -H "accept: application/json"
[
  {
    "__class__": "User",
    "created_at": "2023-12-06T16:39:40.000000",
    "email_address": "johndoe@example.com",
    "first_name": "John",
    "id": "0484b334-96ab-4c49-8f3a-e6a1fa81b863",
    "last_name": "Doe",
    "updated_at": "2023-12-06T16:39:40.000000"
  },
  {
    "__class__": "User",
    "created_at": "2023-12-04T22:57:29.000000",
    "email_address": "stephen@hellotractor.com",
    "first_name": "Stephen",
    "id": "2f910dd9-f8c5-4cbe-9631-38027b91e4c2",
    "last_name": "Oloo",
    "updated_at": "2023-12-04T19:57:29.000000"
  },
  {
    "__class__": "User",
    "created_at": "2023-12-10T17:22:23.000000",
    "email_address": "okongoflorence@gmail.com",
    "first_name": "Florence",
    "id": "57861cb1-7bea-40c0-8e8d-6185b8b91cd9",
    "last_name": "Okongo",
    "updated_at": "2023-12-10T17:22:23.000000"
  },
  {
    "__class__": "User",
    "created_at": "2023-12-04T22:53:50.000000",
    "email_address": "beldineverah@gmail.com",
    "first_name": "Vera",
    "id": "ebcf49f5-e8c7-4066-8efb-ab34505c4ad9",
    "last_name": "Akoth",
    "updated_at": "2023-12-04T22:53:50.000000"
  },
  {
    "__class__": "User",
    "created_at": "2023-12-04T22:54:52.000000",
    "email_address": "amondidamaris@gmail.com",
    "first_name": "Damaris",
    "id": "f8d8fb5c-f319-4abf-8111-1a373b6fd6d1",
    "last_name": "Amondi",
    "updated_at": "2023-12-04T22:54:52.000000"
  }
]

LENOVO@DESKTOP-JH999HJ MINGW64 ~/Desktop/RESTful API-BASED TASK MANAGEMENT SYSTEM (Development)
curl -X GET "http://16.171.57.238:5000/api/v1/user/tasks/stephen%40hellotractor.com" -H "accept: application/json"
[
  {
    "__class__": "User",
    "created_at": "2023-12-04T22:57:29.000000",
    "email_address": "stephen@hellotractor.com",
    "first_name": "Stephen",
    "id": "2f910dd9-f8c5-4cbe-9631-38027b91e4c2",
    "last_name": "Oloo",
    "updated_at": "2023-12-04T19:57:29.000000"
  },
  [
    {
      "__class__": "Task",
      "completion_status": "pending",
      "created_at": "2023-12-04T23:02:20.000000",
      "days_to_complete": 2,
      "deadline": "Wed, 06 Dec 2023 23:02:20 GMT",
      "description": "call renters",
      "email_address": "stephen@hellotractor.com",
      "priority_level": "high",
      "task_id": "158399dd-c6e7-4c63-a7f7-ff8eded5826d",
      "title": "Call",
      "updated_at": "2023-12-04T23:02:20.000000",
      "user_id": "2f910dd9-f8c5-4cbe-9631-38027b91e4c2"
    },
    {
      "__class__": "Task",
      "completion_status": "pending",
      "created_at": "2023-12-04T23:05:31.000000",
      "days_to_complete": 2,
      "deadline": "Wed, 06 Dec 2023 23:05:31 GMT",
      "description": "call renters",
      "email_address": "stephen@hellotractor.com",
      "priority_level": "high",
      "task_id": "1dde760b-b39c-4dc0-a14e-6ab19548ebf5",
      "title": "Call",
      "updated_at": "2023-12-04T23:05:31.000000",
      "user_id": "2f910dd9-f8c5-4cbe-9631-38027b91e4c2"
    },
    {
      "__class__": "Task",
      "completion_status": "pending",
      "created_at": "2023-12-04T23:09:45.000000",
      "days_to_complete": 3,
      "deadline": "Thu, 07 Dec 2023 23:09:45 GMT",
      "description": "meet renters",
      "email_address": "stephen@hellotractor.com",
      "priority_level": "low",
      "task_id": "67c627e2-7040-4dcf-bbcd-4e4c643ea40b",
      "title": "Meeting",
      "updated_at": "2023-12-04T23:09:45.000000",
      "user_id": "2f910dd9-f8c5-4cbe-9631-38027b91e4c2"
    }
  ]
]
```
## Authors
- Stephen Oloo - [Github](https://github.com/stepholo) / [Twitter](https://twitter.com/Stevenob12)

## Licence

This project is licensed under the MIT License. You are free to use, modify, and distribute this software as per the terms of the MIT License.

### Conditions and Limitations

- This project incorporates third-party libraries that are distributed under different licenses. Please refer to their respective licenses for more information.

### Attribution

If you use this project in your work, please provide attribution by including a reference to the original repository.

### Disclaimer

This software is provided "as is," without warranty of any kind, express or implied.

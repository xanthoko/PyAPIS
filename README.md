# PyAPIS

A project that translates OpenAPI to a set of python web frameworks.

## Suported Frameworks
- [x] Django
- [ ] Flask
- [x] FastAPI
- [ ] Pyramid


## Installation
Clone the project and install the prerequisites with `pip install -r requirements.txt`


### Django
To tranlate the input to a Django Project execute `python parser.py /path/to/yml django`

A Django project called *demo* will be created inside the *Django* directory.
To test the project go inside *Django/demo* and run `python manage.py runserver`.
Just like that you have your django server up and running with the endpoints you declared.


### FastAPI
To tranlate the input to a FastAPI Project execute `python parser.py /path/to/yml fastapi`

A directory called *demo* will be created inside the *FastAPI* directory.
To test it go inside the *FastAPI/demo* directory and run `uvicorn main:app --reload`.
Just like that you have your FastAPI server up and running with the endpoints you declared.
# PyAPIS

A project that translates OpenAPI to a set of frameworks.

## Suported Frameworks
- [ ] Django
- [ ] Flask
- [ ] FastAPI
- [ ] Pyramid


## Installation
Clone the project and install the prerequisites with `pip install -r requirements.txt`


### Django
To tranlate the input to a Django Project execute `python parser.py /path/to/yml django`

A Django project called *demo* will be created inside the *Django* directory.
To test the project go inside the *Django* directory and run `python manage.py runserver`.
Just like that you have your django server up and running with the endpoints you declared.
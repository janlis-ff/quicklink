[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-8d7812.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Django 5.1.8](https://img.shields.io/badge/5.1.8-Django-0c4b33)](https://www.djangoproject.com/)
[![Django Rest Framework 3.16.0](https://img.shields.io/badge/3.16.0-DRF-ad0000)](https://www.django-rest-framework.org/)

# QuickLink
A simple URL shortener application built with Django and DRF.

![ezgif-497d72c00fc707](https://github.com/user-attachments/assets/3f557d70-5822-44ac-944f-3b77d6745a11)

### Running the project locally

```bash
docker compose up
```

Once the application is running, you can access a sample landing page at `http://localhost:8000/`.

### Running tests

```bash
docker compose run --rm django pytest
```

### API Documentation

You can access the OpenAPI documentation (swagger UI) at `http://localhost:8000/api/docs/`.

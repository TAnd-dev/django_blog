# django_blog

## Overview

### django_blog is a Django-based application that provides a platform for blogging, forum discussions, and an online shop. This repository includes modular apps for various functionalities, including user authentication, profile management, and static content management.

## Features
- Blog: Create, edit, and manage blog posts.
- Forum: Participate in discussions on various topics.
- Shop: Manage products and handle transactions.
- User Authentication: Secure user login and registration.
- User Profiles: Manage user information and preferences.
- Static Content: Serve static files and media.

## Installation
### Clone the repository:
`git clone https://github.com/TAnd-dev/django_blog.git`

`cd django_blog`

### Create a virtual environment and activate it:
`python3 -m venv env`

`source env/bin/activate`

### Install the dependencies:
`pip install -r requirements.txt`

### Apply migrations:
`python manage.py migrate`

### Run the development server:
`python manage.py runserver`

## Usage
Access the application at http://127.0.0.1:8000/. Register a new account or log in with an existing one to start using the blog, forum, and shop functionalities.

## Project Structure
- blog/: Blog-related functionality.
- forum/: Forum-related functionality.
- shop/: E-commerce functionality.
- user_auth/: User authentication and registration.
- user_profile/: User profile management.
- static/: Static files.
- templates/: HTML templates.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your changes. Ensure that your code follows the project's coding standards and includes appropriate tests.

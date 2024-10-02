# Inventory Management System API

A simple backend API for managing inventory using Django Rest Framework (DRF), PostgreSQL, and Redis. This project provides CRUD operations on inventory items and uses JWT for authentication. Redis is integrated for caching, and unit tests are implemented for verifying API functionality.

## Table of Contents

- [Features](#features)
- [Technologies](#technologies)
- [Setup Instructions](#setup-instructions)
- [Authentication](#authentication)
- [Running Tests](#running-tests)
- [API Endpoints](#api-endpoints)
- [Logging](#logging)

## Features

- **CRUD operations** on inventory items.
- **JWT authentication** for secure access.
- **Redis caching** to enhance performance for frequently accessed items.
- **PostgreSQL** as the database.
- **Logging** to monitor API usage and errors.
- **Unit tests** to ensure API functionality.

## Technologies

- Django 4.x
- Django Rest Framework
- PostgreSQL
- Redis
- JWT Authentication

## Setup Instructions

### Prerequisites

Ensure you have the following installed:

- Python 3.x
- PostgreSQL
- Redis

### Step 1: Clone the Repository

```bash
git clone https://github.com/nayeemabee/Inventory-Management-Project.git
cd Inventory-Management-Project
```

### Step 2: Activate a Virtual Environment

```bash
venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Create superuser (optional)
```bash
python manage.py createsuperuser
```

### Step 6: Start Redis

### Step 7: Run Server
```bash
python manage.py runserver
```

## Authentication

JWT-based authentication is implemented using djangorestframework-simplejwt. After logging in, you will receive access and refresh tokens. You can use the access token to authenticate with the API by including it in the Authorization header.

## Running Tests

To run the unit tests, use the following command:
```bash
python manage.py test
```

## API Endpoints (cUrls)

### 1. Register a New User
```bash
curl --location 'http://127.0.0.1:8000/auth/register/' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <YOUR_ACCESS_TOKEN>' \
--data-raw '{
    "username": "jhondoe@mail.com",
    "password": "qwerty"
}'
```

### 2. Login a User
```bash
curl --location 'http://127.0.0.1:8000/auth/login/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "jhondoe@mail.com",
    "password": "qwerty"
}'
```

### 3. Create a New Item
```bash
curl --location 'http://127.0.0.1:8000/api/items/' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <YOUR_ACCESS_TOKEN>' \
--data '{
    "name": "New item",
    "description": "description"
}'
```

### 4. Get All Items
```bash
curl --location --request GET 'http://127.0.0.1:8000/api/item-list/' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <YOUR_ACCESS_TOKEN>'
```

### 5. Get Item by ID
```bash
curl --location --request GET 'http://127.0.0.1:8000/api/items/<ITEM_ID>/' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <YOUR_ACCESS_TOKEN>'
```

### 6. Update an Item by ID
```bash
curl --location --request PUT 'http://127.0.0.1:8000/api/items/<ITEM_ID>/' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <YOUR_ACCESS_TOKEN>' \
--data '{
    "name": "updated item",
    "description": "description"
}'

```

### 7. Delete an Item by ID
```bash
curl --location --request DELETE 'http://127.0.0.1:8000/api/items/<ITEM_ID/' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <YOUR_ACCESS_TOKEN>'
```

Note:
Replace `<YOUR_ACCESS_TOKEN>` with the appropriate JWT token you received after logging in.

## Logging
The application uses Python’s `logging` module to capture errors and events. Log files are saved in the `logs/` directory.

### Log Levels:

- **DEBUG**: Development level logs.
- **INFO**: General information.
- **ERROR**: Errors and exceptions.





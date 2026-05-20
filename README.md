# 📚 Goodreads Clone

A full-featured web application inspired by Goodreads — built with Django & Django REST Framework. Includes REST APIs, unit tests for each app, and user authentication.

---

## 🚀 Features

- 📖 Browse and search books
- ⭐ Rate and review books
- 📝 Manage personal reading lists (Read, Currently Reading, Want to Read)
- 👤 User authentication (register, login, logout)
- 🔌 REST API for all major resources
- 🧪 Unit tests written for each app

---

## 🛠 Tech Stack

- **Backend:** Python, Django, Django REST Framework
- **Database:** PostgreSQL / SQLite
- **Frontend:** HTML, CSS, Bootstrap
- **Auth:** Django built-in authentication + Token Auth
- **Testing:** Django TestCase, APITestCase

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/gyelmuratov/goodreads.git
cd goodreads
```

### 2. Create and activate virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply migrations

```bash
python manage.py migrate
```

### 5. Create superuser (optional)

```bash
python manage.py createsuperuser
```

### 6. Run the development server

```bash
python manage.py runserver
```

Open your browser at **http://127.0.0.1:8000**

---

## 🔌 API Endpoints

### Books
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/books/` | List all books |
| POST | `/api/books/` | Create a book |
| GET | `/api/books/<id>/` | Get book detail |
| PUT | `/api/books/<id>/` | Update a book |
| DELETE | `/api/books/<id>/` | Delete a book |

### Reviews
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/reviews/` | List all reviews |
| POST | `/api/reviews/` | Create a review |
| GET | `/api/reviews/<id>/` | Get review detail |
| DELETE | `/api/reviews/<id>/` | Delete a review |

### Users
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/users/register/` | Register new user |
| POST | `/api/users/login/` | Login & get token |
| GET | `/api/users/me/` | Get current user info |

> **Auth:** Token-based authentication. Include header:
> `Authorization: Token <your_token>`

---

## 🧪 Running Tests

Run all tests:

```bash
python manage.py test
```

Run tests for a specific app:

```bash
python manage.py test books
python manage.py test users
python manage.py test api
```

Run with verbosity:

```bash
python manage.py test --verbosity=2
```

---

## 📁 Project Structure

```
goodreads/
├── books/           # Books app (models, views, urls, tests)
├── users/           # User auth app (models, views, urls, tests)
├── api/             # REST API app (serializers, viewsets, tests)
├── templates/       # HTML templates
├── static/          # CSS, JS, images
├── manage.py
└── requirements.txt
```

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.

---

## 📄 License

This project is licensed under the MIT License.

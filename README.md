# CRM System for a Cafe

An educational project: a CRM system for automating cafe operations. Developed in two versions — console and web.

---

## v1 — Console Application

**Stack:** Python, JSON

A simple CRM that runs in the terminal. Data is stored in a `database.json` file.

### Features

- Customer management: add, view, delete
- Order management: create, view, change status, delete
- Order priorities: low / medium / high
- Deadline tracking (format `YYYY-MM-DD`)
- Order filtering by customer
- History of completed and cancelled orders

### Running

```bash
cd v1/code
python project.py
```

No dependencies — only the Python standard library is used.

### Structure

```
v1/
├── code/
│   └── project.py      # Single application file
└── database.json       # Database (created automatically)
```

---

## v2 — Django Web Application

**Stack:** Python, Django 6, SQLite, Bootstrap 5

A full-featured web application with authentication, role-based access, and email notifications.

### Features

**Customer:**
- Registration and login via email
- Browse the menu (food / drinks) with images and prices
- Place orders with item quantities
- View active orders and order history
- Cancel an order

**Manager:**
- View all active orders and history
- Change order status: `New → In Progress → Completed / Cancelled`
- Email notification to the customer on status change
- View the customer list, delete accounts

### Running

1. Navigate to the project directory and activate the virtual environment:

```bash
cd v2/crm
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux / macOS
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file based on `.env.example`:

```
SECRET_KEY=your-secret-key
EMAIL_HOST_USER=your@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

4. Apply migrations and start the server:

```bash
python manage.py migrate
python manage.py runserver
```

The application is available at `http://127.0.0.1:8000/`.

To load sample menu data:

```bash
python manage.py loaddata orders/fixtures/menu.json
```

### Structure

```
v2/crm/
├── crm/                # Django settings (settings.py, urls.py)
├── accounts/           # Authentication, registration, roles
├── orders/             # Menu, orders, notifications
├── templates/          # Base HTML templates
├── media/              # Uploaded images
├── .env.example        # Environment configuration example
└── manage.py
```

### Data Models

| Model | Fields |
|---|---|
| `User` | email, name, phone, role (customer / manager) |
| `MenuItem` | name, description, price, category, image |
| `Order` | customer, status, created date |
| `OrderItem` | order, menu item, quantity |

### URL Routes

| Path | Description |
|---|---|
| `/login/`, `/register/` | Login and registration |
| `/dashboard/` | Personal account (redirects by role) |
| `/menu/` | Menu for the customer |
| `/my-orders/` | Customer's orders |
| `/manager/clients/` | Customer list (manager) |
| `/manager/orders/` | All orders (manager) |

### Dependencies

```
Django==6.0.3
Pillow==12.2.0
python-dotenv==1.2.2
```
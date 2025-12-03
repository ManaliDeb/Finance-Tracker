# Finance Tracker Flask App

To keep this Finance Tracker organized and easier to maintain, we chose a MVC-style structure (model-view-controller view). This project was originally forked from an open-source Finance Tracker. The original structure loosely followed this style. Our team adopted this structure intentionally and refined it by reorganizing routes, views, and database logic to create a clearer separation of concerns consistent with MVC principles.

## Decisions

- **model**:
    - SQLite database to store users and transactions
    - adding database functions in 'db.py'

- **view**: 
    - HTML templates with Jinja2
        (Jinja2 is a popular, fast, and expressive templating engine for Python. It is widely used in web development frameworks like Flask)
    - pages of templates include: Login, Regristration, Dashboard, Transactions, Statistics
- **Controller**: 
   - Flask route handlers in "app.py"
   - Logic for authentication, data retriveral, form processing

## Rationale
- Clear seperation of the responsibilties
- Helps to make debugging and testing easier

## Consequences
- **Pros**: 
   - Improved clarity and maintainabilty
   - Easier collaboration 
   - Consistent file organization
- **Cons**: 
   - Requires discipline to maintain the MVC structure

# Finance Tracker Flask App

This project was forked from an open-source Finance Tracker that originally had a more monolithic Flask structure. For our course project, we decided to adopt and refine a layered, MVC-style architecture to improve clarity, testability, and maintainability.

## Decisions
- Use a layered architecture with:
  - A **presentation layer** for routes and templates
  - A **service layer** for business logic
  - A **repository layer** for data access
  - A **domain/model layer** for core entities
- Keep the original schema compatible while improving organization.

## Rationale
- Aligns with MVC and layered architecture concepts covered in class.
- Makes the codebase easier to reason about and extend.
- Clearly separates concerns between UI, logic, and persistence.

## Consequences
- **Pros**: 
   -  Matches industry-style architectures.
    -  Encourages unit testing of services and repositories.
    - Makes responsibilities of files and folders more obvious.
- **Cons**: 
   - Requires more structure and discipline than a single-file Flask app.
   - Refactoring effort needed to keep routes, services, and repositories aligned.

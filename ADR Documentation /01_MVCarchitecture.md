# Finance Tracker Flask App

This project is a fork of the open-source Finance Tracker (0xramm/Finance-Tracker). The original code provides a working Flask app for tracking expenses and income. For our course project, we decided to keep this base and focus on understanding, documenting, and lightly extending its architecture and quality.

For a full structural overview, see `ARCHITECTURE.md`.

## Decisions
- Keep the original Flask-based structure and database schema.
- Use the refactored architecture description in `ARCHITECTURE.md` to explain the system in layered, MVC-style terms (presentation, domain, data access).
- Add our own documentation and tests on top of the fork.

## Rationale
- Starting from a working open-source app lets us concentrate on architecture, design, and testing rather than just rebuilding CRUD.
- This fits the assignment’s goal of adapting and improving an existing project.
- Documenting the architecture helps us and the grader understand how the app is organized.

## Consequences

** Pros **
- Faster to get to design and testing work.
- Clear story for the final report: we evaluated and extended an existing app.
- We can compare behavior with the original project if needed.

** Cons**
- We did not design every part of the code from scratch.
- Some legacy design decisions remain from the original project.

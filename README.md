# Railway Management System 🚆

A terminal-based application for managing railway operations, staff workflows, and customer services. Designed for clarity, maintainability, and extensibility—perfect for team learning and future growth!

## 🏗️ Architecture: MVC Pattern

This project follows a Model-View-Controller (MVC) style layered architecture to ensure clean, maintainable code:

- **`app/models/`**: Data models; defines how railway entities are represented.
- **`app/repositories/`**: Storage layer; handles only raw storage logic, no validation or business rules.
- **`app/services/`**: Business logic layer; handles validation, orchestrates actions, interacts with repositories, and enforces rules.
- **`app/menus/`**: Terminal UI; a stack-based menu manager that talks to services and displays results to the user.

## 🗃️ Data Storage

Currently, data is stored in-memory within `app/repositories/` and is lost when the app closes.
_Note: Future updates will implement persistent JSON storage using Pydantic serialization._

## 👥 User Roles

The system supports three main user types:

### 👑 Admin

- Manage staff members.

### 🚉 Staff

- Manage railways and trains.

### 🎫 Customer

- Manage wallet.
- Buy and manage tickets.
- Update profile information.

## 🚀 Running the Project

Set up your environment and launch the app using:

```bash
uv run -m app.main
```

## 🔮 Future Improvements

We plan to expand and polish this project with the following integrations:

- **Rich**: For beautiful terminal output.
- **Pydantic**: For flexible, validated data models.
- **InquirerPy**: For interactive terminal menus.
- **Loguru**: For slick logging.
- **JSON persistence**: Using Pydantic serialization.

## 📚 Contributing

We welcome contributions! Please read our [CONTRIBUTING.md](CONTRIBUTING.md) for details on our development workflow and setup instructions.

- Open PRs into the `dev` branch.
- When `dev` is stable, it will be merged into `main`.

## 📝 Project Vision

Our goal is to create a structured, extensible terminal app for multi-role railway management. We aim to keep the codebase clean, layered, and easy to grow as new features are added.

##📄 License

This project is licensed under the [MIT License](LICENSE) - see the [LICENSE](LICENSE) file for details.dd a license here if/when the project adopts one.

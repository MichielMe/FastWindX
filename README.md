# 🚀 FastWindX: The Ultimate Web Development Framework

![FastWindX Logo](https://via.placeholder.com/1200x300)

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.95.0-009688.svg)](https://fastapi.tiangolo.com)
[![HTMX](https://img.shields.io/badge/HTMX-1.9.0-3366cc.svg)](https://htmx.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.3.0-38bdf8.svg)](https://tailwindcss.com/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)

> 🌟 Elevate your web development experience with FastWindX - where speed meets simplicity!

FastWindX is a cutting-edge web application framework that combines the power of FastAPI, the interactivity of HTMX, and the flexibility of Tailwind CSS. It's designed to help developers create lightning-fast, scalable, and interactive web applications with ease and elegance.

## ✨ Features

- 🚄 **FastAPI Backend**: Harness the speed and simplicity of FastAPI for robust API development.
- 🔄 **HTMX Frontend**: Create dynamic, AJAX-powered frontends without complex JavaScript.
- 🎨 **Tailwind CSS**: Craft beautiful, responsive UIs with the utility-first CSS framework.
- 🔐 **Built-in Authentication**: Secure your app with a pre-configured JWT authentication system.
- 🗃️ **SQLModel Integration**: Intuitive database operations with SQLModel ORM.
- 🚦 **Asynchronous by Design**: Fully asynchronous architecture for high performance.
- 🐳 **Docker Ready**: Easy deployment with included Dockerfile and docker-compose setup.
- 🛠️ **CLI Tool**: Streamline your workflow with our command-line interface for project management.

## 🚀 Quick Start

Get up and running with FastWindX in minutes!

1. **Install FastWindX**:

   ```bash
   pip install fastwindx
   ```

2. **Create a new project**:

   ```bash
   fastwindx createproject my_awesome_app
   ```

3. **Navigate to your project**:

   ```bash
   cd my_awesome_app
   ```

4. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   npm install
   ```

5. **Run your app**:

   ```bash
   fastwindx run
   ```

6. 🎉 Visit `http://localhost:8000` and see your app in action!

## 🛠 Environment Setup

Before running FastWindX, you need to set up your environment variables.

1. **Create a .env file**:

   ```bash
   cp .env.example .env
   ```

2. **Edit the .env file**:
   Open the .env file in your preferred text editor and update the values as needed. Pay special attention to:
   - `DATABASE_URL`: Your database connection string
   - `SECRET_KEY`: A secret key for security (generate a strong, unique key)
   - Any other app-specific settings

3. **⚠️ Important**: Never commit your .env file to version control. It's already in .gitignore for your safety.

## 🐳 Docker Compose Setup

FastWindX comes with a pre-configured Docker Compose setup, making it easy to get your entire development environment up and running with just a few commands. This setup includes:

- 🚀 Your FastWindX application
- 🐘 PostgreSQL database
- 🔍 pgAdmin for database management

### Prerequisites

- Make sure you have Docker and Docker Compose installed on your system:
  - [Docker Installation Guide](https://docs.docker.com/get-docker/)
  - [Docker Compose Installation Guide](https://docs.docker.com/compose/install/)
- Ensure you've created your .env file as described in the Environment Setup section above.

### Running with Docker Compose

1. **Navigate to your project directory**:

   ```bash
   cd my_awesome_app
   ```

2. **Build and start the services**:

   ```bash
   docker-compose up --build
   ```

3. 🎉 Your FastWindX app is now running at `http://localhost:8000`

### Accessing Services

- 🚀 **FastWindX App**: [http://localhost:8000](http://localhost:8000)
- 🔍 **pgAdmin**: [http://localhost:5050](http://localhost:5050)
  - Email: `admin@fastwindx.com` (or as set in your `docker-compose.yml`)
  - Password: Check your `docker-compose.yml` file

### Database Connection

To connect to the PostgreSQL database using pgAdmin:

1. Open pgAdmin and login
2. Add a new server with the following details:
   - Host: `db` (the service name in docker-compose)
   - Port: `5432`
   - Username: `fastwindx` (or as set in your `docker-compose.yml`)
   - Password: Check your `docker-compose.yml` file

### Stopping the Services

To stop the Docker Compose services:

```bash
docker-compose down
```

Add `-v` flag to remove volumes if you want to start fresh next time:

```bash
docker-compose down -v
```

### 💡 Pro Tip

For development, you can run the services in detached mode and view logs as needed:

```bash
docker-compose up -d
docker-compose logs -f
```

This Docker Compose setup provides a complete development environment, allowing you to focus on building your FastWindX application without worrying about database setup or management tools.

## 📚 Documentation

For detailed documentation, check out our [Wiki](https://github.com/yourusername/fastwindx/wiki).

- 🔧 [Configuration Guide](https://github.com/yourusername/fastwindx/wiki/Configuration)
- 🗃️ [Database Migrations](https://github.com/yourusername/fastwindx/wiki/Database-Migrations)
- 🚢 [Deployment Guide](https://github.com/yourusername/fastwindx/wiki/Deployment)
- 🧪 [Testing](https://github.com/yourusername/fastwindx/wiki/Testing)

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. 🍴 Fork the repository
2. 🌿 Create your feature branch: `git checkout -b feature/AmazingFeature`
3. 💾 Commit your changes: `git commit -m 'Add some AmazingFeature'`
4. 🚀 Push to the branch: `git push origin feature/AmazingFeature`
5. 🔍 Open a pull request

Please read our [Contributing Guide](CONTRIBUTING.md) for more details.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) for the incredible Python web framework
- [HTMX](https://htmx.org/) for simplifying web interactivity
- [Tailwind CSS](https://tailwindcss.com/) for the amazing utility-first CSS framework
- [SQLModel](https://sqlmodel.tiangolo.com/) for the intuitive ORM

---

<p align="center">
  <a href="https://github.com/yourusername/fastwindx/stargazers">⭐ Star us on GitHub!</a>
</p>

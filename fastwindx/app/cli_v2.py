import shutil
import subprocess
from pathlib import Path
from typing import Any, List, Set

import click
from jinja2 import Environment, FileSystemLoader
from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

# Initialize Rich console
console = Console()


def ignore_files(dir: str, files: List[str]) -> Set[str]:
    """Specify files and directories to ignore when copying."""
    exclude = {"cli.py", "__pycache__", "*.pyc", "*.pyo", "*.DS_Store"}
    return {file for file in files if any(Path(file).match(pattern) for pattern in exclude)}


def box_print(message: str, style: str = "blue", padding: int = 1) -> None:
    lines = message.split("\n")
    width = max(len(line) for line in lines)
    box_width = width + 2 * padding + 2

    panel = Panel(
        Text(message, justify="center"), box=box.HEAVY, padding=(padding, padding), style=style, width=box_width
    )
    console.print(panel)


def print_logo() -> None:
    logo = """
███████╗ █████╗ ███████╗████████╗██╗    ██╗██╗███╗   ██╗██████╗ ██╗  ██╗
██╔════╝██╔══██╗██╔════╝╚══██╔══╝██║    ██║██║████╗  ██║██╔══██╗╚██╗██╔╝
█████╗  ███████║███████╗   ██║   ██║ █╗ ██║██║██╔██╗ ██║██║  ██║ ╚███╔╝
██╔══╝  ██╔══██║╚════██║   ██║   ██║███╗██║██║██║╚██╗██║██║  ██║ ██╔██╗
██║     ██║  ██║███████║   ██║   ╚███╔███╔╝██║██║ ╚████║██████╔╝██╔╝ ██╗
╚═╝     ╚═╝  ╚═╝╚══════╝   ╚═╝    ╚══╝╚══╝ ╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝  ╚═╝
                        :: FastWindX CLI ::
    """
    console.print(logo, style="magenta")


def print_success(message: str) -> None:
    console.print(f"✅ {message}", style="green bold")


def print_error(message: str) -> None:
    console.print(f"❌ Error: {message}", style="red bold")


def print_info(message: str) -> None:
    console.print(f"ℹ️  {message}", style="cyan")


def print_command(command: str) -> None:
    console.print(f"$ {command}", style="yellow")


def print_header(message: str) -> None:
    header = Text(message, style="bold blue")
    console.rule(header)


def custom_help(ctx: click.Context, param: click.Parameter, value: Any) -> None:
    if not value or ctx.resilient_parsing:
        return
    print_logo()
    box_print("FastWindX CLI Help", style="blue", padding=2)
    print("\n")
    print_info("Available commands:")
    print_header("createproject_full")
    print_info("  Create a new FastWindX project with all dependencies installed.")
    print_info("  Usage: fastwindx createproject_full PROJECT_NAME")
    print_header("createproject")
    print_info("  Create a new FastWindX project without installing dependencies.")
    print_info("  Usage: fastwindx createproject PROJECT_NAME")
    print_header("run")
    print_info("  Run the FastWindX development server.")
    print_info("  Usage: fastwindx run")
    print_header("General Options")
    print_info("  --help  Show this message and exit.")
    ctx.exit()


@click.group()
@click.option("--help", is_flag=True, callback=custom_help, expose_value=False, is_eager=True)
def main() -> None:
    """FastWindX CLI tool for project management."""


@main.command()
@click.argument("project_name")
def createprojectfull(project_name: str) -> None:
    """Create a new FastWindX project with dependencies."""
    print_logo()
    print_info(f"Creating new FastWindX project: {project_name}")

    template_dir = Path(__file__).parent.parent

    if not template_dir.exists():
        print_error(f"Template directory not found at {template_dir}")
        return

    project_path = Path(project_name)
    project_path.mkdir(exist_ok=True)

    # Copy the entire content of the 'app' directory to the new project directory
    shutil.copytree(template_dir, project_path, dirs_exist_ok=True, ignore=ignore_files)

    env = Environment(loader=FileSystemLoader(project_path), autoescape=True)

    for file_path in project_path.rglob("*"):
        if file_path.is_file() and file_path.suffix in (".py", ".yml", ".md"):
            relative_path = file_path.relative_to(project_path)
            template = env.get_template(str(relative_path))
            rendered_content = template.render(project_name=project_name)
            file_path.write_text(rendered_content)

    templates_dir = project_path / "templates"
    if templates_dir.exists():
        env = Environment(loader=FileSystemLoader(templates_dir), autoescape=True)
        for file_path in templates_dir.rglob("*.html"):
            relative_path = file_path.relative_to(templates_dir)
            template = env.get_template(str(relative_path))
            rendered_content = template.render(project_name=project_name)
            file_path.write_text(rendered_content)

    print_info("Installing dependencies...")
    try:
        subprocess.run(["pip", "install", "-r", str(project_path / "requirements.txt")], check=True)
    except subprocess.CalledProcessError:
        print_error("Failed to install dependencies. Please check your requirements.txt file.")
        return

    print_info("Installing npm packages and building CSS...")
    try:
        subprocess.run(["npm", "install"], cwd=project_path, check=True)
        subprocess.run(["npm", "run", "build:css"], cwd=project_path, check=True)
    except subprocess.CalledProcessError:
        print_error("Failed to install npm packages or build CSS. Please check your package.json file.")
        return

    print_success(f"Project {project_name} created successfully!")
    print_info("To start your project, run:")
    print_command(f"cd {project_name}")
    print_command("fastwindx run")

    print_info("To run your project with Docker Composer, run:")
    print_command(f"cd {project_name}")
    print_command("docker-compose up\n\n")


@main.command()
@click.argument("project_name")
def createproject(project_name: str) -> None:
    """Create a new FastWindX project without installing dependencies."""
    print_logo()
    print_info(f"Creating new FastWindX project: {project_name}")

    template_dir = Path(__file__).parent.parent

    if not template_dir.exists():
        print_error(f"Template directory not found at {template_dir}")
        return

    project_path = Path(project_name)
    project_path.mkdir(exist_ok=True)

    # Copy the entire content of the 'app' directory to the new project directory
    shutil.copytree(template_dir, project_path, dirs_exist_ok=True, ignore=ignore_files)

    env = Environment(loader=FileSystemLoader(project_path), autoescape=True)

    for file_path in project_path.rglob("*"):
        if file_path.is_file() and file_path.suffix in (".py", ".yml", ".md"):
            relative_path = file_path.relative_to(project_path)
            template = env.get_template(str(relative_path))
            rendered_content = template.render(project_name=project_name)
            file_path.write_text(rendered_content)

    templates_dir = project_path / "templates"
    if templates_dir.exists():
        env = Environment(loader=FileSystemLoader(templates_dir), autoescape=True)
        for file_path in templates_dir.rglob("*.html"):
            relative_path = file_path.relative_to(templates_dir)
            template = env.get_template(str(relative_path))
            rendered_content = template.render(project_name=project_name)
            file_path.write_text(rendered_content)

    print_success(f"Project {project_name} created successfully!")

    print_info("To install dependencies, run:")
    print_command(f"cd {project_name}")
    print_command("pip install -r requirements.txt")

    print_info("To install npm packages and build CSS, run:")
    print_command(f"cd {project_name}")
    print_command("npm install")
    print_command("npm run build:css")

    print_info("To start your project, run:")
    print_command(f"cd {project_name}")
    print_command("fastwindx run")

    print_info("To run your project with Docker Composer, run:")
    print_command(f"cd {project_name}")
    print_command("docker-compose up\n\n")


@main.command()
def run() -> None:
    """Run the FastWindX development server."""
    print_logo()
    print_info("Starting FastWindX development server...")
    try:
        subprocess.run(["uvicorn", "app.main:app", "--reload"], check=True)
    except subprocess.CalledProcessError:
        print_error("Failed to start the development server. Please check your main.py file.")


if __name__ == "__main__":
    main()

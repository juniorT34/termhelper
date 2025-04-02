import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path


def get_executable_name():
    """Get platform-specific executable name."""
    return "cmdhelper.exe" if platform.system() == "Windows" else "cmdhelper"


def check_pyinstaller():
    """Check if PyInstaller is installed, if not install it."""
    try:
        subprocess.run(
            [sys.executable, "-c", "import PyInstaller"], check=True, capture_output=True
        )
        print("PyInstaller is already installed")
    except subprocess.CalledProcessError:
        print("Installing PyInstaller...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("PyInstaller installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install PyInstaller: {e}")
            raise


def cleanup():
    """Clean up build artifacts."""
    dirs_to_clean = ["build", "dist", "release"]
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
    print("Cleaned build directories")


def build():
    """Build the executable and optionally Docker image."""
    try:
        check_pyinstaller()
        cleanup()

        # Get platform-specific settings
        executable_name = get_executable_name()
        data_separator = ";" if platform.system() == "Windows" else ":"

        # Create spec file if it doesn't exist
        if not os.path.exists("cmdhelper.spec"):
            print("Creating spec file...")
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "PyInstaller",
                    f"--name={executable_name}",
                    "--onefile",
                    "--add-data",
                    f"cmdhelper/data/*.yaml{data_separator}cmdhelper/data",
                    "--add-data",
                    f"cmdhelper/web/templates/*{data_separator}cmdhelper/web/templates",
                    "--add-data",
                    f"cmdhelper/web/static/*{data_separator}cmdhelper/web/static",
                    "cmdhelper/__main__.py",
                ],
                check=True,
            )

        # Run PyInstaller build
        print("Building executable...")
        result = subprocess.run(
            [sys.executable, "-m", "PyInstaller", "cmdhelper.spec", "--clean"], check=True
        )

        # Create release directory
        release_dir = Path("release")
        release_dir.mkdir(exist_ok=True)

        # Copy executable and README
        dist_executable = os.path.join("dist", executable_name)
        if os.path.exists(dist_executable):
            shutil.copy2(dist_executable, release_dir)

            # Make the file executable on Linux
            if platform.system() != "Windows":
                executable_path = os.path.join(release_dir, executable_name)
                os.chmod(executable_path, 0o755)

            print(f"\nBuild complete! Executable '{executable_name}' is in the 'release' directory")

            # Ask about Docker build
            if platform.system() != "Windows":
                docker_choice = input("\nWould you like to build the Docker image as well? (y/N): ")
                if docker_choice.lower() == "y":
                    from docker_build import build_docker

                    build_docker()

            return True
        else:
            print("Error: Executable not found after build")
            return False

    except subprocess.CalledProcessError as e:
        print(f"Build failed: {str(e)}")
        return False
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False


if __name__ == "__main__":
    success = build()
    sys.exit(0 if success else 1)

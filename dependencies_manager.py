import importlib
import subprocess
import sys
import yaml

# Function to check and install packages
def install_package(package):
    """Install a package via pip if not already installed."""
    try:
        importlib.import_module(package.split("==")[0])  # ignore version if given
    except ImportError:
        print(f"📦 Installing missing package: {package}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Main function to read dependencies and ensure they are installed
def main():
    # Load dependencies from YAML
    with open("dependencies.yml", "r") as f:
        deps = yaml.safe_load(f)

    # Collect all unique packages
    all_packages = []
    for section, content in deps.items():
        all_packages.extend(content.get("packages", []))

    # Deduplicate
    all_packages = list(set(all_packages))

    print("🔎 Checking required packages...")
    for pkg in all_packages:
        install_package(pkg)

    print("✅ All required packages are installed.")

if __name__ == "__main__":
    main()

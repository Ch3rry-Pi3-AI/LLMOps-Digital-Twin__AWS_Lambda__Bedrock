"""
Lambda Deployment Packager for the Digital Twin Backend

This script automates the creation of an AWS Lambda deployment package for the
llmops-digital-twin backend. It performs the following steps:

1. Cleans previous build artifacts
2. Installs all Python dependencies inside a Docker container that matches the
   AWS Lambda Python 3.12 runtime
3. Collects application files (`server.py`, `lambda_handler.py`, etc.)
4. Copies the `data/` directory used for contextual persona resources
5. Builds a deployment ZIP (`lambda-deployment.zip`) suitable for uploading
   to AWS Lambda or for use in a Lambda Layer

Using Docker ensures full binary compatibility with Lambda's Linux environment.
"""

# ============================================================
# Imports
# ============================================================

import os
import shutil
import zipfile
import subprocess


# ============================================================
# Main Deployment Function
# ============================================================

def main() -> None:
    """
    Build the AWS Lambda deployment package for the Digital Twin backend.

    Steps:
    - Remove old package folders and ZIP files
    - Build a clean `lambda-package/` directory
    - Install dependencies using the AWS Lambda Python 3.12 Docker image
    - Copy application source files and the `data/` folder
    - Package the result as `lambda-deployment.zip`
    """
    print("🚀 Creating Lambda deployment package...")

    # ------------------------------------------------------------
    # Cleanup previous artifacts
    # ------------------------------------------------------------
    if os.path.exists("lambda-package"):
        shutil.rmtree("lambda-package")

    if os.path.exists("lambda-deployment.zip"):
        os.remove("lambda-deployment.zip")

    # ------------------------------------------------------------
    # Create fresh deployment directory
    # ------------------------------------------------------------
    os.makedirs("lambda-package")
    print("📁 Created clean lambda-package/ directory")

    # ------------------------------------------------------------
    # Install dependencies using Lambda's Python 3.12 runtime
    # ------------------------------------------------------------
    print("📦 Installing dependencies inside Lambda runtime Docker image...")

    subprocess.run(
        [
            "docker",
            "run",
            "--rm",
            "-v",
            f"{os.getcwd()}:/var/task",
            "--platform",
            "linux/amd64",  # Ensures x86_64 CPU architecture for Lambda compatibility
            "--entrypoint",
            "",  # Bypass Lambda's default entrypoint
            "public.ecr.aws/lambda/python:3.12",
            "/bin/sh",
            "-c",
            (
                "pip install "
                "--target /var/task/lambda-package "
                "-r /var/task/requirements.txt "
                "--platform manylinux2014_x86_64 "
                "--only-binary=:all: "
                "--upgrade"
            ),
        ],
        check=True,
    )

    # ------------------------------------------------------------
    # Copy application source files to the package
    # ------------------------------------------------------------
    print("📄 Copying backend source files...")

    source_files = ["server.py", "lambda_handler.py", "context.py", "resources.py"]

    for file in source_files:
        if os.path.exists(file):
            shutil.copy2(file, "lambda-package/")
            print(f"   • Copied {file}")

    # ------------------------------------------------------------
    # Copy the `data/` directory containing persona resources
    # ------------------------------------------------------------
    if os.path.exists("data"):
        shutil.copytree("data", "lambda-package/data")
        print("📂 Copied data/ folder")

    # ------------------------------------------------------------
    # Create the final ZIP file
    # ------------------------------------------------------------
    print("📦 Creating zip file...")

    with zipfile.ZipFile("lambda-deployment.zip", "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk("lambda-package"):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, "lambda-package")
                zipf.write(file_path, arcname)

    # ------------------------------------------------------------
    # Output the final package size
    # ------------------------------------------------------------
    size_mb = os.path.getsize("lambda-deployment.zip") / (1024 * 1024)
    print(f"✅ Created lambda-deployment.zip ({size_mb:.2f} MB)")


# ============================================================
# Entry Point
# ============================================================

if __name__ == "__main__":
    main()

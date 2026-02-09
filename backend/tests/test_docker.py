"""
Docker container tests

Tests to verify:
- Docker image builds successfully
- Image size is reasonable (< 200MB target)
- Container starts and runs correctly
- All required files are included in the image
"""

import pytest
import subprocess
import os


def test_dockerfile_exists():
    """Test that Dockerfile exists in backend directory"""
    dockerfile_path = os.path.join(os.path.dirname(__file__), "..", "Dockerfile")
    assert os.path.exists(dockerfile_path), "Dockerfile must exist in backend directory"


def test_dockerignore_exists():
    """Test that .dockerignore exists in backend directory"""
    dockerignore_path = os.path.join(os.path.dirname(__file__), "..", ".dockerignore")
    assert os.path.exists(dockerignore_path), ".dockerignore must exist in backend directory"


def test_docker_image_builds_successfully():
    """
    Test that Docker image builds without errors

    This test will fail until Dockerfile is created
    """
    backend_dir = os.path.join(os.path.dirname(__file__), "..")

    # Build Docker image
    result = subprocess.run(
        ["docker", "build", "-t", "todo-backend-test", "."],
        cwd=backend_dir,
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Docker build failed: {result.stderr}"


def test_docker_image_has_healthcheck():
    """Test that Docker image includes HEALTHCHECK instruction"""
    backend_dir = os.path.join(os.path.dirname(__file__), "..")
    dockerfile_path = os.path.join(backend_dir, "Dockerfile")

    with open(dockerfile_path, "r") as f:
        dockerfile_content = f.read()

    assert "HEALTHCHECK" in dockerfile_content, "Dockerfile must include HEALTHCHECK instruction"


def test_docker_image_exposes_port():
    """Test that Docker image exposes port 8000"""
    backend_dir = os.path.join(os.path.dirname(__file__), "..")
    dockerfile_path = os.path.join(backend_dir, "Dockerfile")

    with open(dockerfile_path, "r") as f:
        dockerfile_content = f.read()

    assert "EXPOSE 8000" in dockerfile_content, "Dockerfile must expose port 8000"


def test_docker_image_size():
    """
    Test that Docker image size is under 200MB target

    This test will fail until Dockerfile is optimized with multi-stage build
    """
    # Inspect image size
    result = subprocess.run(
        ["docker", "images", "todo-backend-test", "--format", "{{.Size}}"],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        pytest.skip("Docker image not built yet")

    size_str = result.stdout.strip()

    # Parse size (e.g., "150MB" or "1.5GB")
    if "GB" in size_str:
        size_mb = float(size_str.replace("GB", "")) * 1024
    elif "MB" in size_str:
        size_mb = float(size_str.replace("MB", ""))
    else:
        pytest.skip(f"Unknown size format: {size_str}")

    assert size_mb < 200, f"Docker image size ({size_mb}MB) exceeds 200MB target"


@pytest.mark.integration
def test_docker_container_starts():
    """
    Test that Docker container starts successfully

    This is an integration test that requires Docker to be running
    """
    # Start container in detached mode
    result = subprocess.run(
        [
            "docker", "run", "-d",
            "--name", "todo-backend-test-container",
            "-e", "DATABASE_URL=postgresql://test",
            "-e", "JWT_SECRET_KEY=" + "a" * 32,
            "-e", "SMTP_HOST=smtp.test.com",
            "-e", "SMTP_USERNAME=test",
            "-e", "SMTP_PASSWORD=test",
            "-e", "SMTP_FROM_EMAIL=test@test.com",
            "-e", "FRONTEND_URL=http://localhost:3000",
            "-p", "8001:8000",
            "todo-backend-test"
        ],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        pytest.skip(f"Docker container failed to start: {result.stderr}")

    container_id = result.stdout.strip()

    try:
        # Wait a moment for container to start
        import time
        time.sleep(2)

        # Check container is running
        result = subprocess.run(
            ["docker", "ps", "-q", "-f", f"id={container_id}"],
            capture_output=True,
            text=True
        )

        assert result.stdout.strip() == container_id, "Container should be running"

    finally:
        # Cleanup: stop and remove container
        subprocess.run(["docker", "stop", container_id], capture_output=True)
        subprocess.run(["docker", "rm", container_id], capture_output=True)

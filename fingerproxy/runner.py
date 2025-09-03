import os
import platform
import subprocess

def get_executable_path():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dist_dir = os.path.join(base_dir, 'dist')

    system = platform.system().lower()
    machine = platform.machine().lower()

    if system == "windows":
        suffix = ".exe"
        if "arm" in machine or "aarch64" in machine:
            folder = "fingerproxy_windows_arm64_v8.0"
        else:
            folder = "fingerproxy_windows_amd64_v1"
    elif system == "linux":
        suffix = ""
        if "arm" in machine or "aarch64" in machine:
            folder = "fingerproxy_linux_arm64_v8.0"
        else:
            folder = "fingerproxy_linux_amd64_v1"
    elif system == "darwin":
        suffix = ""
        if "arm" in machine or "aarch64" in machine:
            folder = "fingerproxy_darwin_arm64_v8.0"
        else:
            folder = "fingerproxy_darwin_amd64_v1"
    else:
        raise RuntimeError(f"Unsupported platform: {system}")

    exe_path = os.path.join(dist_dir, folder, f"fingerproxy{suffix}")
    if not os.path.isfile(exe_path):
        raise FileNotFoundError(f"Executable not found: {exe_path}")

    return exe_path

def run_service():
    exe_path = get_executable_path()
    print(f"Starting fingerproxy: {exe_path}")
    try:
        # 阻塞运行，输出直接显示到终端
        subprocess.run([exe_path], check=True)
    except KeyboardInterrupt:
        print("\nfingerproxy interrupted by user")
    except subprocess.CalledProcessError as e:
        print(f"fingerproxy exited with code {e.returncode}")

if __name__ == "__main__":
    run_service()

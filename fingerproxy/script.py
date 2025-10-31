import os
import platform
import subprocess
import psutil
import json


def get_executable_path():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dist_dir = os.path.join(base_dir, "dist")

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


def get_file_path():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "daemon_pid.json")
    return file_path


PID_FILE = get_file_path()


def _save_pid(pid):
    with open(PID_FILE, "w") as f:
        json.dump({"pid": pid}, f)


def _load_pid():
    if os.path.exists(PID_FILE):
        with open(PID_FILE, "r") as f:
            return json.load(f)["pid"]
    return None


def run():
    """启动后台进程并记录 PID"""
    if status():
        print("后台进程已启动，关闭执行：fingerproxy_stop")
        return
    system = platform.system().lower()
    cmd = get_executable_path()
    if system == "Windows":
        DETACHED_PROCESS = 0x00000008
        CREATE_NEW_PROCESS_GROUP = 0x00000200
        proc = subprocess.Popen(
            cmd,
            creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
        )
    else:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            preexec_fn=os.setsid,
        )
    _save_pid(proc.pid)
    print(f"[{system}] 后台进程已启动，PID: {proc.pid}")


def stop():
    """停止后台进程"""
    pid = _load_pid()
    if not pid:
        print("没有记录 PID，无法停止进程")
        return
    try:
        p = psutil.Process(pid)
        p.terminate()  # 优雅结束
        p.wait(timeout=5)
        print(f"进程 {pid} 已停止")
    except psutil.NoSuchProcess:
        print(f"进程 {pid} 不存在")
    except Exception as e:
        print(f"停止进程 {pid} 失败: {e}")
    finally:
        if os.path.exists(PID_FILE):
            os.remove(PID_FILE)


def status():
    """查看后台进程状态"""
    pid = _load_pid()
    if not pid:
        print("没有记录 PID")
        return False
    if psutil.pid_exists(pid):
        print(f"进程 {pid} 正在运行")
        return True
    else:
        print(f"进程 {pid} 已停止")
        return False


if __name__ == "__main__":
    run()

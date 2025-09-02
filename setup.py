from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import shutil

# 自动收集 dist 目录下的二进制文件
dist_dir = os.path.join(os.path.dirname(__file__), 'dist')

package_data_files = []
for root, dirs, files in os.walk(dist_dir):
    for file in files:
        # 相对路径
        file_path = os.path.relpath(os.path.join(root, file), start='fingerproxy')
        package_data_files.append(file_path)


class CustomInstall(install):
    def run(self):
        # 获取安装路径
        install_path = os.path.join(self.install_lib, 'your_package_name', 'dist')
        print("install path ===. ",install_path)
        # 删除旧的 dist 文件夹
        if os.path.exists(install_path):
            print(f"Removing old dist folder: {install_path}")
            shutil.rmtree(install_path)
        # 执行默认安装流程
        install.run(self)

setup(
    name='fingerproxy',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'fingerproxy': package_data_files,
    },
    entry_points={
        'console_scripts': [
            'fingerproxy=fingerproxy.runner:run_service',
        ]
    },
    zip_safe=False,
    cmdclass={
        'install': CustomInstall,
    },
)




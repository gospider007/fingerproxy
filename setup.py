from setuptools import setup, find_packages
import os

# 自动收集 dist 目录下的二进制文件
dist_dir = os.path.join(os.path.dirname(__file__), 'dist')

package_data_files = []
for root, dirs, files in os.walk(dist_dir):
    for file in files:
        # 相对路径
        file_path = os.path.relpath(os.path.join(root, file), start='fingerproxy')
        package_data_files.append(file_path)

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
  
)
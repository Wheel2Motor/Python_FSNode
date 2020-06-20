REM 如果使用的python需要使用python3命令来启动，就把下面所有的python换成python3
REM 如果使用的pip3需要使用pip3命令来启动，就把下面所有的pip换成pip3

REM 从豆瓣镜像下载pyinstaller
pip install pyinstaller -i https://pypi.douban.com/simple

REM 从官方镜像下载pyinstaller
REM pip install pyinstaller

pyinstaller -F fsnode_util.py -n FSNode测试工具.exe

copy .\dist\* .\
del .\*.spec
python -c "import shutil;shutil.rmtree('./dist')"
python -c "import shutil;shutil.rmtree('./build')"
python -c "import shutil;shutil.rmtree('./__pycache__')"
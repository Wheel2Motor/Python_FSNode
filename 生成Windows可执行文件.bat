REM ���ʹ�õ�python��Ҫʹ��python3�������������Ͱ��������е�python����python3
REM ���ʹ�õ�pip3��Ҫʹ��pip3�������������Ͱ��������е�pip����pip3

REM �Ӷ��꾵������pyinstaller
pip install pyinstaller -i https://pypi.douban.com/simple

REM �ӹٷ���������pyinstaller
REM pip install pyinstaller

pyinstaller -F fsnode_util.py -n FSNode���Թ���.exe

copy .\dist\* .\
del .\*.spec
python -c "import shutil;shutil.rmtree('./dist')"
python -c "import shutil;shutil.rmtree('./build')"
python -c "import shutil;shutil.rmtree('./__pycache__')"
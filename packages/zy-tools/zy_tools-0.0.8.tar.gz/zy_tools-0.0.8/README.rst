cd 到 setup.py 路径；分别执行以下两条命令
# 将项目进行打包
1、python3 setup.py sdist build
# 将项目上传，输入下面命令后，会要求输入用户名和密码
2、twine upload dist/*
# -*- coding: utf-8 -*-
"""
@auth: chenping
@desc: 批量修改vc项目的设置,设置内容:
    1. PlatformToolset 设置成 v100
    2. AdditionalIncludeDirectories 中添加 openssl的include文件路径
    3. 
"""

import os, logging

openssl_include = ur"S:\workdir\zc-deploy\references\netxms\openssl-OpenSSL_1_0_2e\release\include"

def main(srcPath):
    init_logging()
    logging.info(u"工具开始运行....")

    handlers = []
    handlers.append(handle_includedirset)
    handlers.append(handle_platformset)
    handlers.append(handle_dependences)

    vcxProjs = getVcxProjs(srcPath)
    for vcxProj in vcxProjs:
        setVcxProj(vcxProj, handlers)

    logging.info(u"工具运行结束!")
    
def init_logging():
    """"""
    formatter = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(filename = 'run.log', level = logging.DEBUG, format = formatter)
    
    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)
    sh.setFormatter(logging.Formatter(formatter))
    
    rootlogger = logging.getLogger()
    rootlogger.addHandler(sh)

def getVcxProjs(srcPath):
    logging.info(u"开始扫描c++项目文件...")

    vcxProjs = []
    for root, dirs, files in os.walk(srcPath):
        for _file in files:
            if _file.endswith(".vcxproj"):
                vcxProjs.append(os.path.join(root, _file))

    logging.info(u"扫描到项目数目:%d" % len(vcxProjs))
    return vcxProjs

def setVcxProj(progFile, handlers):
    
    logging.info(u"开始处理项目文件:[%s]..." % progFile)
    new_content = []

    with open(progFile, 'r') as fileobj:
        lines = fileobj.readlines()
        for line in lines:
            if line == "":
                continue

            new_line = None
            for handler in handlers:
                new_line = handler(line)
                if new_line != None:
                    break

            if new_line == None:
                new_line = line.replace('\n', '')
            new_content.append(new_line)

    with open(progFile, 'w+') as fileobj:
        new_content = [item + '\n' for item in new_content]
        fileobj.writelines(new_content)
    pass

def handle_platformset(line):
    if line.find("<PlatformToolset>") == -1:
        return

    return "<PlatformToolset>v100</PlatformToolset>"

def handle_includedirset(line):
    if line.find("<AdditionalIncludeDirectories>") == -1:
        return

    content = line.replace("\n", "").replace("<AdditionalIncludeDirectories>", "").\
                    replace("</AdditionalIncludeDirectories>", "")
    content = content.strip() + ";" + openssl_include + r";S:\workdir\zc-deploy\references\netxms\zlib-1.2.8"
    return "<AdditionalIncludeDirectories>%s</AdditionalIncludeDirectories>" % content

def handle_dependences(line):
    if line.find("<AdditionalDependencies>") == -1:
        return

    content = line.replace("\n", "").replace("<AdditionalDependencies>", "").replace("</AdditionalDependencies>", "").strip()
    content = content.replace("ssleay32.lib", r"S:\workdir\zc-deploy\references\netxms\openssl-OpenSSL_1_0_2e\release\lib\ssleay32.lib")
    content = content.replace("libeay32.lib", r"S:\workdir\zc-deploy\references\netxms\openssl-OpenSSL_1_0_2e\release\lib\libeay32.lib")

    return "<AdditionalDependencies>%s</AdditionalDependencies>" % content

if __name__ == '__main__':
    srcPath = r"S:\workdir\zc-deploy\references\netxms\netxms-2.1-M1\src"
    main(srcPath)
FROM mcr.microsoft.com/windows/servercore:1607
WORKDIR /Users/Public/Estrattore
COPY EstrazioneDati.exe Bin/
COPY EstrazioneDati_container.exe.config Bin/EstrazioneDati.exe.config
COPY myconfig.xml cfg/
RUN MKDIR Log
COPY Log.txt Log/
COPY python-3.7.4-embed-amd64/*.* python/
COPY get-pip.py .
RUN .\python\python.exe get-pip.py 

FROM centos:centos7
COPY Centos-7.repo /etc/yum.repos.d/CentOS-Base.repo
ADD Python-3.8.17.tgz /opt/
ADD get-pip.py /opt/
RUN cd /opt/Python-3.8.17 && \
    yum clean all && \
    yum makecache && \
    yum groupinstall "Development Tools" -y && \
    yum install zlib zlib-devel -y && \
    yum install -y openssl openssl-devel && \
    yum install -y tcl-devel tk-devel && \
    yum install libffi-devel -y && \
    ./configure --enable-optimizations && \
    make altinstall && \
    ln -s /usr/local/bin/python3.8 /usr/bin/python3 && \
    python3 /opt/get-pip.py && \
    ln -s /usr/local/bin/pip /usr/bin/pip3 && \
    pip3 install setuptools -i https://pypi.tuna.tsinghua.edu.cn/simple && \
    rm -rf /opt/*

CMD ["/bin/bash"]

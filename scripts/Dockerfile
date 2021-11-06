FROM centos
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && yum -y install epel-release \
    && yum repolist \
    && yum install -y openssl-devel bzip2-devel expat-devel gdbm-devel readline-devel sqlite-devel gcc make\
    && yum -y install python3-devel \
    && yum -y install crontabs \
    && yum install -y git \
    && yum -y install python36
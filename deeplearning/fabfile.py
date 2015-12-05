from fabric.api import env,local,run,sudo,put,cd,lcd,puts,task,get
from fabric.operations import local as lrun, run
from fabric.state import env
import os,sys,logging
# logging.basicConfig(level=logging.INFO,
#                     format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
#                     datefmt='%m-%d %H:%M',
#                     filename='logs/fab.log',
#                     filemode='a')
from workspace.settings import USER,private_key,HOST
env.user = USER
env.key_filename = private_key
env.hosts = [HOST,]

@task
def clear_logs():
    """
    remove logs
    """
    local('rm logs/*.log &')

@task
def notebook_server():
    """
    Run IPython notebook on an AWS server
    run("openssl req -x509 -nodes -days 365 -newkey rsa:1024 -keyout mycert.key -out mycert.pem")
    c = get_config()
    c.NotebookApp.open_browser = False
    c.NotebookApp.ip = '0.0.0.0'
    c.NotebookApp.port = 8888
    c.NotebookApp.certfile = u'/home/ubuntu/mycert.pem'
    c.NotebookApp.enable_mathjax = False
    c.NotebookApp.password = u'{}'
    :return:
    """
    from IPython.lib.security import passwd
    sudo("/home/ubuntu/anaconda/bin/ipython notebook --ip=0.0.0.0  --NotebookApp.password={} --no-browser".format(passwd())) #--certfile=mycert.pem


@task
def notebook():
    """
    deactivate
    pip freeze > requirements.txt
    local("sudo port select --set python python27")
    local("sudo port select --set ipython ipython27")
    local("sudo port select --set pip pip27")
    local("sudo port select --set virtualenv virtualenv27")
    :return:
    """
    local("ipython-2.7 notebook")



@task
def freeze():
    local("source ~/portenv/bin/activate;pip freeze >> requirements.txt")


@task
def connect():
    """
    Creates connect.sh for the current host
    :return:
    """
    fh = open("connect.sh",'w')
    fh.write("#!/bin/bash\n"+"ssh -i "+env.key_filename+" "+"ubuntu"+"@"+HOST+"\n")
    fh.close()

@task
def backup():
    get("workspace/*","workspace")

@task
def upload():
    try:
        sudo("rm -rf workspace")
    except:
        pass
    put("workspace","")


@task
def setup_caffe():
    """
    sudo apt-get update
    sudo apt-get install libprotobuf-dev libleveldb-dev libsnappy-dev libopencv-dev libhdf5-serial-dev protobuf-compiler
    sudo apt-get install libgflags-dev libgoogle-glog-dev liblmdb-dev libatlas-dev
    sudo apt-get install libatlas-base-dev
    sudo apt-get install libprotobuf-dev libleveldb-dev libsnappy-dev libopencv-dev libboost-all-dev libhdf5-serial-dev libgflags-dev libgoogle-glog-dev liblmdb-dev protobuf-compiler libatlas-base-dev
    sudo apt-get install python-dev python-pip gfortran
    pip install protobuf
    conda uninstall system
    conda install system
    conda update ipython ipython-notebook ipython-qtconsole
    conda install matplotlib
    apt-get install libatlas-base-dev
    conda uninstall system
    conda install system
    pip install protobuf
    sudo ln -s /usr/local/cuda/lib64/libcudnn.so.6.5.48 /usr/lib/libcudnn.so
    :return:
    """
    sudo("apt-get update")
    sudo("apt-get install -y libprotobuf-dev libleveldb-dev libsnappy-dev libopencv-dev libhdf5-serial-dev protobuf-compiler")
    sudo("apt-get install -y libgflags-dev libgoogle-glog-dev liblmdb-dev libatlas-dev libatlas-base-dev")
    sudo("apt-get install -y libprotobuf-dev libleveldb-dev libsnappy-dev libopencv-dev libboost-all-dev libhdf5-serial-dev libgflags-dev libgoogle-glog-dev liblmdb-dev protobuf-compiler libatlas-base-dev")
    sudo("apt-get install -y python-dev python-pip gfortran")
    run("conda uninstall -y system")
    run("conda install  -y  system")
    run("conda update  -y ipython ipython-notebook ipython-qtconsole")
    run("conda install -y  matplotlib")
    run("git clone http://github.com/Russell91/apollocaffe.git")
    sudo("pip install protobuf")
    sudo("pip uninstall protobuf")
    run("pip install Munkres")
    with cd("cd apollocaffe"):
        local("pip install -r python/requirements.txt")
        local("make -j8")
        local("export PYTHONPATH=$PYTHONPATH:/home/ubuntu/apollocaffe/python")
        local("export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/ubuntu/apollocaffe/build/lib")
    sudo("sudo /home/ubuntu/anaconda/bin/ipython notebook --ip=0.0.0.0")
    sudo("vim /etc/ld.so.conf.d/caffe.conf")
    sudo('cat "/home/ubuntu/apollocaffe/build/lib " >> /etc/ld.so.conf.d/caffe.conf')
    sudo('cat "/usr/local/cuda/lib64" >> /etc/ld.so.conf.d/caffe.conf')
    sudo("ldconfig")


@task
def tensorboard():
    local("source ~/portenv/bin/activate;tensorboard --logdir=.")
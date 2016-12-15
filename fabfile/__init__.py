# -*- coding: utf-8 -*-
import os.path
from fabric.api import env, task, run, put, cd, sudo
from fabric.contrib.files import exists, append, contains, sed

from .utils import mkdir
from . import conf_file


env.use_ssh_config = True

BASE_PATH = '$HOME/tmp-fabric-toolkit'


@task
def test():
    """执行uname -a命令"""
    run('uname -a')


@task
def update():
    sudo('apt-get update')


@task
def upgrade():
    sudo('apt-get upgrade')


@task
def cn_source():
    with cd('/etc/apt'):
        bak = ''
        if exists('sources.list.bak'):
            bak = '2'
        sudo('cp sources.list sources.list.bak' + bak)
    sed('/etc/apt/sources.list', '//us.', '//cn.',
        use_sudo=True, backup='')


@task
def sudo_nopassword():
    """
    sudo命令无需密码
    http://stackoverflow.com/questions/323957/how-do-i-edit-etc-sudoers-from-a-script
    """
    user = run('whoami')
    add_content = '{}\tALL=(ALL) NOPASSWD:ALL'.format(user)
    with cd(BASE_PATH):
        tmp = os.path.join(run('pwd'), 'sudoers.tmp')
    run('sudo cat /etc/sudoers > {}'.format(tmp))
    if contains(tmp, add_content):
        return
    append(tmp, add_content)
    sudo('EDITOR="cp {0}" visudo'.format(tmp))


@task
def default_editor():
    """更改默认编辑器"""
    sudo('update-alternatives --config editor')


@task
def dotfiles():
    """设置git，vim等的默认配置"""
    mkdir(BASE_PATH)
    with cd(BASE_PATH):
        if not exists('dotfiles'):
            run('git clone https://github.com/codeif/dotfiles.git')
        with cd('dotfiles'):
            run('git pull')
            run('./bootstrap.sh -f')
    sudo('apt-get install exuberant-ctags')


@task
def install_pip():
    if not exists('/usr/bin/python'):
        sudo('apt-get -y install python')
    if not exists('/usr/bin/python3'):
        sudo('apt-get -y install python3')
    if not exists('/usr/local/bin/pip'):
        run('curl --silent --show-error --retry 3 '
            'https://bootstrap.pypa.io/get-pip.py | '
            'sudo -H python')
    run('sudo -H pip install -U pip')


@task
def pip_conf():
    """使用豆瓣的pip源"""
    if not exists('~/.pip/'):
        run('mkdir ~/.pip')
    path = conf_file.get_path('pip.conf')
    put(path, '~/.pip/')


@task
def install_nginx():
    if not exists('/usr/sbin/nginx'):
        sudo('apt-get -y install nginx')


@task
def install_supervisor():
    if not exists('/usr/bin/supervisorctl'):
        sudo('apt-get -y install supervisor')
        sudo('service supervisor start')
        # 设置开机启动
        sudo('update-rc.d supervisor defaults')
        # in ubuntu 16.04
        sudo('systemctl enable supervisor.service')


@task
def ntpdate():
    """同步时间"""
    if not exists('/usr/sbin/ntpdate'):
        sudo('apt-get -y install ntpdate')
    sudo('ntpdate cn.pool.ntp.org')


@task
def all_task():
    sudo_nopassword()
    cn_source()
    update()
    default_editor()
    dotfiles()
    install_pip()
    pip_conf()
    install_nginx()
    install_supervisor()
Fabric常用工具集合
==================

- 使用说明，以安装nginx为例

.. code-block::

    fab -H name@yourserver install_nginx

- 所有命令

==================  ============================
命令                说明
==================  ============================
all_task
cn_source
default_editor      更改默认编辑器
dotfiles            设置git，vim等的默认配置
git-aware-prompt    git显示分支名
install_nginx
install_pip
install_supervisor
install_virtualenv
ntpdate             同步时间
pip_conf            使用豆瓣的pip源
sudo_nopassword     sudo命令无需密码
test                执行uname -a命令
update
upgrade
==================  ============================

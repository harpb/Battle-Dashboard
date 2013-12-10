from fabric.api import *
import pprint

# Fill out USER and HOSTS configuration before running
env.user = "root"
if env.key_filename == None:
    env.key_filename = ["~/.ssh/id_rsa"]

ENVIRONMENTS = {
    "prod": {
        "default_branch": "master",
        "repo_dir": "/home/harpb/battle-dashboard",
        "servers": [
            '66.175.218.7'
        ],
        "type": 'LOCAL'
    },
    "local": {
        "default_branch": "master",
        "repo_dir": '',
        "servers": [
            'localhost'
        ],
        "type": 'LOCAL'
    },
}

for env_name, server_env in ENVIRONMENTS.iteritems():
    server_env['pyenv_path'] = server_env['repo_dir'] + '/pyenv'
    server_env['webapp_path'] = server_env['repo_dir'] + '/django_app'
    server_env['static_path'] = server_env['webapp_path'] + '/battle/static'
    server_env['server_script'] = server_env['webapp_path'] + '/gevent_wsgi_server.py'

#===============================================================================
# ENVIRONMENTS
#===============================================================================
def local():
    env.settings = ENVIRONMENTS['local']
    env.hosts = env.settings['servers']
    if env.settings['repo_dir'] is '':
        raise Exception('repo_dir must be defined.')
    

def prod():
    env.settings = ENVIRONMENTS['prod']
    env.hosts = env.settings['servers']

#===============================================================================
# HELPERS
#===============================================================================
def run_in_background(cmd, server_env):
#    run("nohup export SERVER_ENVIRONMENT=PROD %s >& /dev/null < /dev/null &" % cmd, shell=False, pty=False)
# #        run("export -p", shell=False, pty=False)
    run('bash -c export SERVER_ENVIRONMENT=%s' % server_env['type'])
    run('export SERVER_ENVIRONMENT=%s' % server_env['type'])
    run('declare -x SERVER_ENVIRONMENT=%s' % server_env['type'])
    with prefix('export SERVER_ENVIRONMENT=%s' % server_env['type']):
        full_cmd = "export DJANGO_SETTINGS_MODULE=django_app.settings; export SERVER_ENVIRONMENT=%s; nohup %s >& /dev/null < /dev/null &" % (
                server_env['type'], cmd)
        run(full_cmd, shell = False, pty = False)

def django_manage(cmd, background = False, server_env = None):
    if not server_env:
        server_env = env.settings
    full_cmd = '%s/bin/python %s/manage.py %s' % (
            server_env['pyenv_path'], server_env['webapp_path'], cmd)
    if background:
        run_in_background(full_cmd)
    else:
        with prefix("export SERVER_ENVIRONMENT=%s" % server_env['type']):
            run(full_cmd)

#===============================================================================
# ACTIONS
#===============================================================================
def start_server(server_env = None):
    if not server_env:
        server_env = env.settings
    sudo('service nginx start')
    cmd = '%s/bin/python %s' % (server_env['pyenv_path'], server_env['server_script'])
    run_in_background(cmd, server_env)

def stop_django(server_env = None):
    if not server_env:
        server_env = env.settings
    try:
        run('pkill -f %r' % server_env['server_script'])
    except:
        pass

def stop_server(server_env = None):
    if not server_env:
        server_env = env.settings
    sudo('service nginx stop')
    stop_django(server_env)

def restart_server():
    try:
        stop_server()
    except:
        pass
    start_server()

def pull_changes():
    # PULL changes
    with cd(env.settings["repo_dir"]):
        run("git status")
        run("git pull")

def build_pyenv():
    run('apt-get update')
    run('apt-get -y upgrade')
    run('apt-get -y dist-upgrade')
    run('apt-get install -y libxml2-dev libxslt-dev python-crypto')
    run("npm install -g bower")
    pull_changes()
#    run('pip install lxml')
    with cd(env.settings["repo_dir"]):
        run("rm -rf ./pyenv/build")
        run("./pyenv/bin/pip install -r pipfile --download-cache=_pip_cache --upgrade --exists-action=s ")

def build_windows_pyenv():
    pull_changes()
    run("npm install -g bower")
#    run('pip install lxml')
    with cd(env.settings["repo_dir"]):
        run("rm -rf ./pyenv/build")
        run("./pyenv/Scripts/pip install -r pipfile --download-cache=_pip_cache --upgrade --exists-action=s ")

def django_sync():
    # UPDATE static files
    django_manage('collectstatic -l --noinput')
    django_manage('syncdb --migrate')

def npm_install():
    with cd(env.settings["static_path"]):
        run("bower install --allow-root")

def refresh():
    pull_changes()
    npm_install()
    django_sync()
    # REFRESH Processes
    restart_server()

def setup():
    run("git clone git@github.com:harpb/Battle-Dashboard.git %r" % env.settings["repo_dir"])
    with cd(env.settings["repo_dir"]):
        run('virtualenv pyenv --prompt=battle --system-site-packages')
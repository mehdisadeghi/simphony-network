"""
This module is part of simphony-network package.
"""
from fabric.api import cd, env, prefix, run, task, settings


@task
def setup_env():
    code_dir = '~/.virtualenvs/simphony'
    with settings(warn_only=True):
        if run("test -d %s" % code_dir).failed:
            run('mkdir -p %s' % code_dir)
            with cd('~/.virtualenvs/simphony'):
                run('curl -O https://pypi.python.org/packages/source/v/virtualenv/virtualenv-13.1.0.tar.gz')
                run('tar xzvf virtualenv-13.1.0.tar.gz')
                run('rm -rf virtualenv-13.1.0.tar.gz')
                run('python virtualenv-13.1.0/virtualenv.py .')
                run('rm -rf virtualenv-13.1.0')


@task
def deploy():
    with prefix('. ~/.virtualenvs/simphony/bin/activate'):
        with cd('~/.virtualenvs/simphony'):
            run('git clone git@bitbucket.org:idhem/simphony-network.git')
            #run('cd simphony-network && pip install -r requirements.txt')
            #abspath_requirements = os.path.abspath('../requirements.txt')
            #put(abspath_requirements, '~/.virtualenvs/simphony')
            #run('pip install -r requirements.txt')
        with cd('~/.virtualenvs/simphony/simphony-network'):
            run('pip install -r requirements.txt')
            run('python setup.py install')


@task
def start():
    with cd('~/.virtualenvs/simphony'):
        with prefix('. ./bin/activate'):
            run('simphony')

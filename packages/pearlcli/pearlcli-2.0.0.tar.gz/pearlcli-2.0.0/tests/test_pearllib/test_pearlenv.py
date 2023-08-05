import os
from pathlib import Path

import pytest

from unittest import mock

from pearllib.pearlenv import PearlEnvironment, Package

_MODULE_UNDER_TEST = 'pearllib.pearlenv'


@pytest.mark.parametrize(
    'pearl_home_var, home, expected_home',
    [
        pytest.param(
            None,
            None,
            'home-dir/.local/share/pearl'
        ),
        pytest.param(
            'home/myhome2/.local/share/pearl2',
            None,
            'home/myhome2/.local/share/pearl2',
        ),
        pytest.param(
            'home/myhome2/.local/share/pearl2',
            'home/myhome3/.local/share/pearl3',
            'home/myhome3/.local/share/pearl3',
        ),
        pytest.param(
            None,
            'home/myhome3/.local/share/pearl3',
            'home/myhome3/.local/share/pearl3',
        ),
    ]
)
def test_pearl_env_home(pearl_home_var, home, expected_home, tmp_path):
    with mock.patch(_MODULE_UNDER_TEST + '.os') as os_mock:
        home_dir = tmp_path / 'home-dir'
        (home_dir / '.local/share/pearl').mkdir(parents=True)
        default_environ = {'HOME': home_dir}

        if pearl_home_var is not None:
            (tmp_path / pearl_home_var).mkdir(parents=True)
            os_mock.environ = {'PEARL_HOME': str(tmp_path / pearl_home_var)}
            os_mock.environ.update(default_environ)
        else:
            os_mock.environ = dict(default_environ)

        if home is not None:
            home = tmp_path / home
            home.mkdir(parents=True)
        assert str(PearlEnvironment._get_home(home=home)) == str(tmp_path / expected_home)


def test_pearl_env_home_not_directory():
    with mock.patch(_MODULE_UNDER_TEST + '.os') as os_mock:
        os_mock.environ = {'HOME': '/home/myhome'}
        PearlEnvironment._get_home(env_initialized=False)
        with pytest.raises(ValueError):
            PearlEnvironment._get_home()


def test_pearl_env_root_raise_error():
    with pytest.raises(ValueError):
        PearlEnvironment._get_root(Path('/path/to/root'))


def test_pearl_env_root_from_arg(tmp_path):
    assert tmp_path == PearlEnvironment._get_root(tmp_path)


def test_config_filename():
    assert PearlEnvironment._get_config_filename(Path('/myhome2/pearl.conf')) == Path('/myhome2/pearl.conf')
    assert PearlEnvironment._get_config_filename(None) == Path('{}/.config/pearl/pearl.conf'.format(os.environ['HOME']))


def test_packages(tmp_path):
    pearl_home = tmp_path / 'home'
    pearl_home.mkdir()
    pearl_root = tmp_path / 'root'
    pearl_root.mkdir()

    pearl_conf = pearl_home / 'pearl.conf'
    pearl_conf.write_text("""
PEARL_REPO_NAME = 'test'
PEARL_PACKAGES = {
    'b-test-pkg': {
        'url': 'https://github.com/username/test-pkg',
        'description': 'My descr'
    },
    'a-test-pkg': {
        'url': 'https://github.com/username/test-pkg',
        'description': 'My descr'
    },
}
""")
    pearl_env = PearlEnvironment(home=pearl_home, root=pearl_root, config_filename=pearl_conf)
    assert pearl_env.packages['test']['a-test-pkg'].url == 'https://github.com/username/test-pkg'
    assert pearl_env.packages['test']['a-test-pkg'].description == 'My descr'
    assert pearl_env.packages['test']['b-test-pkg'].url == 'https://github.com/username/test-pkg'
    assert pearl_env.packages['test']['b-test-pkg'].description == 'My descr'


def test_load_repos_init_repo(tmp_path):
    pearl_home = tmp_path / 'home'
    pearl_home.mkdir()
    pearl_root = tmp_path / 'root'
    pearl_root.mkdir()

    pearl_conf = pearl_home / 'pearl.conf'
    pearl_conf.touch()

    with mock.patch(_MODULE_UNDER_TEST + '.subprocess') as subprocess_mock:
        pearl_env = PearlEnvironment(home=pearl_home, root=pearl_root, config_filename=pearl_conf)
        repo_path = pearl_env.home / 'repos/a10c24fd1961ce3d1b87c05cc008b593'
        assert pearl_env.load_repos(('https://github.com/pearl-hub/repo.git',)) == [repo_path / 'pearl-config/repo.conf']

        assert subprocess_mock.run.call_args[0][0] == ['git', 'clone', '--depth', '1', 'https://github.com/pearl-hub/repo.git', str(repo_path), '--quiet']


@pytest.mark.parametrize(
    'update_repos',
    [
        pytest.param(True),
        pytest.param(False)
    ]
)
def test_load_repos_update_repo(update_repos, tmp_path):
    pearl_home = tmp_path / 'home'
    pearl_home.mkdir()
    pearl_root = tmp_path / 'root'
    pearl_root.mkdir()

    repo_dir = pearl_home / "repos/a10c24fd1961ce3d1b87c05cc008b593/.git"
    repo_dir.mkdir(parents=True)

    pearl_conf = pearl_home / 'pearl.conf'
    pearl_conf.touch()

    with mock.patch(_MODULE_UNDER_TEST + '.subprocess') as subprocess_mock:
        pearl_env = PearlEnvironment(home=pearl_home, root=pearl_root, config_filename=pearl_conf)
        repo_path = pearl_env.home / 'repos/a10c24fd1961ce3d1b87c05cc008b593'
        assert pearl_env.load_repos(('https://github.com/pearl-hub/repo.git',), update_repos=update_repos) == [repo_path / 'pearl-config/repo.conf']
        if update_repos:
            assert subprocess_mock.run.call_args[0][0] == ['git', '-C', str(repo_path), 'pull', '--quiet']
        else:
            assert subprocess_mock.run.call_count == 0


def test_package():
    pkg = Package(Path('/home'), 'repo', 'pkg1', 'https://pkg1', 'pkg1 descr')
    assert pkg.name == 'pkg1'
    assert pkg.repo_name == 'repo'
    assert pkg.full_name == 'repo/pkg1'
    assert pkg.url == 'https://pkg1'
    assert pkg.description == 'pkg1 descr'
    assert pkg.dir == Path('/home/packages/repo/pkg1')
    assert pkg.vardir == Path('/home/var/repo/pkg1')
    assert not pkg.is_local()

    pkg = Package(Path('/home'), 'repo', 'pkg1', '/pkg1', 'pkg1 descr')
    assert pkg.is_local()

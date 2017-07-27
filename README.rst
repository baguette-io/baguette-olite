==============
baguette-olite
==============

.. image:: https://travis-ci.org/baguette-io/baguette-olite.svg?branch=master
    :target: https://travis-ci.org/baguette-io/baguette-olite

Python wrapper for gitolite. Fork from https://github.com/PressLabs/pyolite.

Easy and simple to user, just `pip install baguette-olite`.

Gitolite Setup Prereqs
======================

Using Pyolite is very easy, but requires some initial set up. First, your **gitolite-admin** repo must contain a directory called `repos` and another one called 
`groups`, and all `.conf` files in these directories should be included in your `gitolite.conf` file. For example, your **gitolite-admin** repo might have the following structure:

::

    ├── gitolite.conf
    └── repos
        └── [ empty ]
    └── groups
        └── [ empty ]

And your `gitolite.conf` file might look like this:

::

    repo gitolite-admin
        RW+     =   admin

    repo testing
        RW+     =   @all

    include	    "repos/*.conf"
    include	    "groups/*.conf"

This is required because Pyolite makes changes to files only inside the **repos** and **groups** directories.

Repository API
==============

First, we need to initialize a `pyolite` object with the path to `gitolite`'s repository.

::

    from pyolite import Pyolite

    # initial olite object
    admin_repository = '/home/absolute/path/to/gitolite/repo/'
    olite = Pyolite(admin_repository=admin_repository)

After that, we can create and get a repo using `create` and `get` methods.

::

    # create a repo
    repo = olite.repos.get('my_repo')
    repo = olite.repos.create('ydo')

    # List existing Pyolite repos
    repos = olite.repos.all()
    for repo_it in repos:
        print(repo_it.name)


Every repo has an `users` object, in order to facilitate basic operations: adding, editing and removing users from a repository.

::

    print("Repo's users: %s" % repo.users)
    # list a repo's users
    users_as_list = repo.users.list()

    # add a new user
    user = olite.users.create(name='bob', key_path="~/.ssh/third_rsa.pub")
    repo.users.add(olite.users.get('admin'), permission='W+')
    repo.users.add('bob', permission='R')

    # change user's permissions
    repo.users.edit(olite.users.get('admin'), permission='WR+')
    repo.users.edit('bob', permission='RCW')

    # remove user
    repo.users.remove('admin')

Users API
=========

You an easly manipulate `users` aswell, using allmost the same API.

::

    from pyolite import Pyolite

    # initial olite object
    admin_repository = '/home/absolute/path/to/gitolite/repo/'
    olite = Pyolite(admin_repository=admin_repository)

    # create user object
    vlad = olite.users.create(name='bob',
                          key_path='~/.ssh/second_rsa.pub')

    # get user by name
    vlad = olite.users.get(name='admin')

    # add new key to user
    vlad.keys.append('/path/to/key')
    vlad.keys.append('just put the key here')

    # check if user is admin or not
    print(vlad.is_admin)

    # list user's keys and repos
    keys_as_list = vlad.list_keys()
    repos_as_list = vlad.list_repos()

    # delete a user by name
    deleted_user = olite.users.delete('username')
    print(deleted_user)

Groups API
==========

You an easly manipulate `groups` aswell, using allmost the same API.

::

    from pyolite import Pyolite

    # initial olite object
    admin_repository = '/home/absolute/path/to/gitolite/repo/'
    olite = Pyolite(admin_repository=admin_repository)

    # create group object
    group1 = olite.groups.create('group1')
    # create is idempotent
    group1 = olite.groups.create('group1')

    #get or create( `create()` wrapper)
    group2 = olite.groups.get_or_create('group2')
    group2 = olite.groups.get_or_create('group2')

    # get group by name
    group1 = olite.groups.get('group1')

    # list all groups
    olite.groups.all()

    # delete a group by name
    olite.groups.delete('group1')

    # add an user to the gorup
    olite.groups.user_add('group1', 'user1')

    # delete an user from a group
    olite.groups.user_delete('group1', 'user1')

    # add a group to a repo
    olite.groups.repo_add('group1', 'repo1', 'RW')

    # delete a group from a repo
    olite.groups.repo_delete('group1', 'repo1')

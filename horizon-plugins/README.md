Horizon plugins consist a bunch of files. `openstack_dashboard` dir 'mirrors' corresponding directory structure of Horizon installation.

Directories under `openstack_dashboard/dashboards` are actual dashboards implementations (top level main menu items and its views).

`openstack_dashboard/dashboards/inventory` directory:

1. `dashboard.py` - Inventory dashboard declaration module.
2. `chef` and `nodes` - Inventory dashboard views modules for Inventory/Chef and Inventory/Nodes.
3. `templates/*` - Inventory views templates.
4. `static/*` - support files and libs.

`openstack_dashboard/enabled` direcoty contains dashboards and their views 'triggers` -- files for enabling plugins:

1. `_5000_inventory.py` - Inventory dashboard 'trigger'.
2. `_5010_inventory_nodes.py` - Inventory/Nodes view 'trigger'.
3. `_5020_inventory_chef.py` - Inventory/Chef view 'trigger'.

Files should be respectively placed under OpenStack Horizon root `openstack_dashboards` directory.

`openstack_dashboard/local/local_settings.py` must provide following configuration options:


Inventory/Chef options:

- INVENTORY_CHEF_URL
- INVENTORY_CHEF_KEY
- INVENTORY_CHEF_USER


Inventory/Nodes options:

- INVENTORY_MAAS_KEY
- INVENTORY_MAAS_URL

## Installation

0. `$ pip install PyChef`
1. `$ git clone git@github.com:nephoscale/horizon-plugins.git`
2. `$ cd horizon-plugins`
3. `$ sudo cp -R openstack_dashboard/dashboards/* ${HORIZON_ROOT}/openstack_dashboard/dashboards/``
4. `$ sudo cp -R openstack_dashboard/enabled/* ${HORIZON_ROOT}/openstack_dashboard/enabled/`
5. Edit `${HORIZON_ROOT}/openstack_dashboard/local/local_settings.py` and add/edit required config options.

Note:

If you see `OSError: libcrypto.so: cannot open shared object file: No such file or directory` in apache logs, 
just `ln -s` `libcrypto.so.1.0.0` into system lib directory and restart apache. For example, on Ubuntu 14.04 x64 do:
```
$ sudo ln -s /lib/x86_64-linux-gnu/libcrypto.so.1.0.0 /lib/x86_64-linux-gnu/libcrypto.so
$ sudo service apache2 restart 
```


###Setup Signups dashboard
0. After clonning horizon-plugins repo copy or symlink `openstack_dashboard/dashboards/identity/signups` dir into 
`${HORIZON_ROOT}/openstack_dashboard/identity` dir, and copy (or symlink) enable file `openstack_dashboard/enabled/_3080_identity_signups_panel.py` into
`${HORIZON_ROOT}/openstack_dashboard/enabled/` dir.
1. Edit `local_settings.py` and add signups dashboard config options `SIGNUP_ROLES`.
2. git clone python-urbaneclient.
3. Copy or symlink `python-urbaneclient/urbaneclient` into `${HORIZON_ROOT}/openstack_dashboard/identity/signups/` dir.
4. `sudo pip install --upgrade -r python-urbaneclient/requirements.txt`
5. `service apache reload`


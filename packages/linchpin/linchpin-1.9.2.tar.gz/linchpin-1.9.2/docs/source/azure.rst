The dependencies is perfectly working for the latest version of Ansible, 
if you are not using the latest version, may not work.

Azure VM
===================

The Azure provider manages multiple types of resources.

azure_vm
-------

Azure VM Instances can be provisioned using this resource.

* Example <workspaces/azure/Pinfile>`
* azure_vm module <https://docs.ansible.com/ansible/latest/modules/azure_rm_virtualmachine_module.html#id4>`_

Topology Schema
~~~~~~~~~~~~~~~

Within Linchpin, the :term:`azure_vm` :term:`resource_definition` has more
options than what are shown in the examples above. For each :term:`azure_vm`
definition, the following options are available.

+----------------------+------------+---------------+-----------------------+--------------------+
| Parameter            | required   | type          | ansible value         | comments           |
+======================+============+===============+=======================+====================+
| role                 | true       | string        | N/A                   |                    |
+----------------------+------------+---------------+-----------------------+--------------------+
| vm_name              | true       | string        | name                  | It can't include   |
|                      |            |               |                       | '_' and other      |
|                      |            |               |                       | special char       |
+----------------------+------------+---------------+-----------------------+--------------------+
| private_image        | false      | string        | image                 | This takes         |
|                      |            |               |                       | private images     |
|                      |            |               |                       |                    |
+----------------------+------------+---------------+-----------------------+--------------------+
| virtual_network_name | false      | string        | virtual_network_name  |                    |
+----------------------+------------+---------------+-----------------------+--------------------+
| vm_username          | false      | string        | image                 |                    |
+----------------------+------------+---------------+-----------------------+--------------------+
| vm_password          | false      | string        | image                 |                    |
+----------------------+------------+---------------+-----------------------+--------------------+
| count                | false      | int           |                       |                    |
+----------------------+------------+---------------+-----------------------+--------------------+
| resource_group       | true       | string        | resource_group        |                    |
+----------------------+------------+---------------+-----------------------+--------------------+
| vm_size              | false      | string        | vm_size               |                    |
+----------------------+------------+---------------+-----------------------+--------------------+
| public_image         | false      | dict          | image                 | This para takes    |
|                      |            |               |                       | public images      |
|                      |            |               |                       |                    |
+----------------------+------------+---------------+-----------------------+--------------------+
| vm_username          | false      | string        | admin_username        |                    |
+----------------------+------------+---------------+-----------------------+--------------------+
| vm_password          | false      | string        | admin_password        |                    |
+----------------------+------------+---------------+-----------------------+--------------------+
| public_key           | false      | string        |                       | Copy you key here  |
+----------------------+------------+---------------+-----------------------+--------------------+
| delete_all_attached  | false      | string        | remove_on_absent      |                    |
+----------------------+------------+---------------+-----------------------+--------------------+
| availability_set     | false      | string        | availability_set      |                    |
+----------------------+------------+---------------+-----------------------+--------------------+


azure_nsg
-------

Azure Network Security Group can be provisioned using this resource.

* Example <workspaces/azure/Pinfile>`
* azure_nsg module <https://docs.ansible.com/ansible/latest/modules/azure_rm_securitygroup_module.html?highlight=azure%20security#examples>`_

Topology Schema
~~~~~~~~~~~~~~~

Within Linchpin, the :term:`azure_vm` :term:`resource_definition` has more
options than what are shown in the examples above. For each :term:`azure_vm`
definition, the following options are available.

+----------------------+------------+---------------+-----------------------+--------------------+
| Parameter            | required   | type          | ansible value         | comments           |
+======================+============+===============+=======================+====================+
| role                 | true       | string        | N/A                   |                    |
+----------------------+------------+---------------+-----------------------+--------------------+
| name                 | true       | string        | name                  |                    |
+----------------------+------------+---------------+-----------------------+--------------------+
| purge_rules          | false      | string        | purge_rules           |                    |
+----------------------+------------+---------------+-----------------------+--------------------+
| rules                | false      | list(dict)   | rules                  |                    |
+----------------------+------------+---------------+-----------------------+--------------------+


⚫ If you declare both public and private image, only the private will be taken

azure_api
-------

Any Azure resources can be provisioned using this role, it supported by the Azure Api

* Example <workspaces/azure/Pinfile>`
* azure_api module <https://docs.ansible.com/ansible/latest/modules/azure_rm_resource_module.html#azure-rm-resource-module>`_
* Azure API <https://docs.microsoft.com/en-us/rest/api/?view=Azure>`_

Topology Schema
~~~~~~~~~~~~~~~

Within Linchpin, the :term:`azure_api` :term:`resource_definition` has more
options than what is shown in the examples above. For each :term:`azure_api`
definition, the following options are available.

+----------------------+------------+---------------+-----------------------+--------------------+
| Parameter            | required   | type          | ansible value         | comments           |
+======================+============+===============+=======================+====================+
|  role                | true       | string        | N/A                   |                    |
+----------------------+------------+---------------+-----------------------+--------------------+
|  resource_group      | true       | string        | resource_group        |                    |
+----------------------+------------+---------------+-----------------------+--------------------+
|  resource_type       | true       | string        | resource_type         |                    |
+----------------------+------------+---------------+-----------------------+--------------------+
|  resource_name       | true       | string        | resource_name         |                    |
+----------------------+------------+---------------+-----------------------+--------------------+
|  api_version         | true       | string        | api_version           |                    |
+----------------------+------------+---------------+-----------------------+--------------------+
|  body_path           | true       | string        |                       |Path to request body|
+----------------------+------------+---------------+-----------------------+--------------------+
|  url                 | true       | string        | url                   |                    |
+----------------------+------------+---------------+-----------------------+--------------------+



azure_loadbalancer
-------

With this role you can provision and configure the Azure Load Balancer

* Example <workspaces/azure/Pinfile>`
* azure_loadbalancer module <https://docs.ansible.com/ansible/latest/modules/azure_rm_loadbalancer_module.html?highlight=azure%20load%20balance>`_

Topology Schema
~~~~~~~~~~~~~~~

Within Linchpin, the :term:`azure_loadbalancer` :term:`resource_definition` has more
options than what is shown in the examples above. For each :term:`azure_loadbalancer`
definition, the following options are available.

+-----------------------------+------------+---------------+-----------------------------+--------------------+
| Parameter                   | required   | type          | ansible value               | comments           |
+=============================+============+===============+=============================+====================+
|  role                       | true       | string        | N/A                         |                    |
+-----------------------------+------------+---------------+-----------------------------+--------------------+
|  resource_group             | false      | string        | resource_group              |                    |
+-----------------------------+------------+---------------+-----------------------------+--------------------+
|  name                       | true       | string        |  name                       |                    |
+-----------------------------+------------+---------------+-----------------------------+--------------------+
|  frontend_ip_configuration  | false      | string        |  frontend_ip_configuration  |                    |
+-----------------------------+------------+---------------+-----------------------------+--------------------+
|  backend_address_pools      | false      | string        |  backend_address_pools      |                    |
+-----------------------------+------------+---------------+-----------------------------+--------------------+
|  probes                     | false      | string        |  probes                     |                    |
+-----------------------------+------------+---------------+-----------------------------+--------------------+
|  inbound_nat_pools          | false      | string        | inbound_nat_pools           |                    |
+-----------------------------+------------+---------------+-----------------------------+--------------------+
|  inbound_nat_rules          | false      | string        | inbound_nat_rules           |                    |
+-----------------------------+------------+---------------+-----------------------------+--------------------+
|  load_balacing_rules        | false      | string        | load_balacing_rules         |                    |
+-----------------------------+------------+---------------+-----------------------------+--------------------+



azure_publicipaddress
-------

With this role, you can provision and manage Azure public ip address

* Example <workspaces/azure/Pinfile>`
* azure_publicipaddress module <https://docs.ansible.com/ansible/latest/modules/azure_rm_publicipaddress_module.html?highlight=azure%20public%20address>`_

Topology Schema
~~~~~~~~~~~~~~~

Within Linchpin, the :term:`azure_publicipaddress` :term:`resource_definition` has more
options than what is shown in the examples above. For each :term:`azure_publicipaddress`
definition, the following options are available.

+-----------------------------+------------+---------------+-----------------------------+--------------------+
| Parameter                   | required   | type          | ansible value               | comments           |
+=============================+============+===============+=============================+====================+
|  role                       | true       | string        | N/A                         |                    |
+-----------------------------+------------+---------------+-----------------------------+--------------------+
|  resource_group             | false      | string        | resource_group              |                    |
+-----------------------------+------------+---------------+-----------------------------+--------------------+
|  allocation_method          | true       | string        | allocation_method           |                    |
+-----------------------------+------------+---------------+-----------------------------+--------------------+
|  domain_name                | false      | string        | domain_name                 |                    |
+-----------------------------+------------+---------------+-----------------------------+--------------------+
|  sku                        | false      | string        | sku                         |                    |
+-----------------------------+------------+---------------+-----------------------------+--------------------+


azure_availabilityset
-------

Any Azure resources can be provisioned using this role, it supported by the Azure Api

* Example <workspaces/azure/Pinfile>`
* azure_availabilityset module <https://docs.ansible.com/ansible/latest/modules/azure_rm_availabilityset_module.html?highlight=azure%20avail>`_

Topology Schema
~~~~~~~~~~~~~~~

Within Linchpin, the :term:`azure_availabilityset` :term:`resource_definition` has more
options than what is shown in the examples above. For each :term:`azure_availabilityset`
definition, the following options are available.

+-----------------------------+------------+---------------+-----------------------------+--------------------+
| Parameter                   | required   | type          | ansible value               | comments           |
+=============================+============+===============+=============================+====================+
|  role                       | true       | string        | N/A                         |                    |
+-----------------------------+------------+---------------+-----------------------------+--------------------+
|  resource_group             | false      | string        | resource_group              |                    |
+-----------------------------+------------+---------------+-----------------------------+--------------------+
|  name                       | true       | string        |  name                       |                    |
+-----------------------------+------------+---------------+-----------------------------+--------------------+
|  location                   | false      | string        |  name                       |                    |
+-----------------------------+------------+---------------+-----------------------------+--------------------+
| platform_update_domain_count| false      | string        | platform_update_domain_count|                    |
+-----------------------------+------------+---------------+-----------------------------+--------------------+
| platform_fault_domain_count | false      | string        | platform_fault_domain_count |                    |
+-----------------------------+------------+---------------+-----------------------------+--------------------+
|  sku                        | false      | string        | sku                         |                    |
+-----------------------------+------------+---------------+-----------------------------+--------------------+



azure_network_interface
-------

Azure network interface can be provisioned using this role

* Example <workspaces/azure/Pinfile>`
* azure_rm_networkinterface module <https://docs.ansible.com/ansible/latest/modules/azure_rm_networkinterface_module.html?highlight=azure%20network%20interface>`_

Topology Schema
~~~~~~~~~~~~~~~

Within Linchpin, the :term:`azure_rm_networkinterface` :term:`resource_definition` has more
options than what is shown in the examples above. For each :term:`azure_rm_networkinterface`
definition, the following options are available.

+-----------------------------+------------+---------------+-----------------------------+--------------------+
| Parameter                   | required   | type          | ansible value               | comments           |
+=============================+============+===============+=============================+====================+
|  role                       | true       | string        | N/A                         |                    |
+-----------------------------+------------+---------------+-----------------------------+--------------------+
|  resource_group             | false      | string        | resource_group              |                    |
+-----------------------------+------------+---------------+-----------------------------+--------------------+
|  name                       | true       | string        |  name                       |                    |
+-----------------------------+------------+---------------+-----------------------------+--------------------+
|  virtual_network_name       | false      | string        |  virtual_network            |                    |
+-----------------------------+------------+---------------+-----------------------------+--------------------+
| subnet_name                 | false      | string        | platform_update_domain_count|                    |
+-----------------------------+------------+---------------+-----------------------------+--------------------+


azure_resource_group
-------

Azure network interface can be provisioned using this role

* Example <workspaces/azure/Pinfile>`
* azure_rm_resourcegroup module <https://docs.ansible.com/ansible/latest/modules/azure_rm_resourcegroup_module.html?highlight=azure%20resource%20group>`_

Topology Schema
~~~~~~~~~~~~~~~

Within Linchpin, the :term:`azure_rm_networkinterface` :term:`resource_definition` has more
options than what is shown in the examples above. For each :term:`azure_rm_networkinterface`
definition, the following options are available.

+-----------------------------+------------+---------------+-----------------------------+--------------------+
| Parameter                   | required   | type          | ansible value               | comments           |
+=============================+============+===============+=============================+====================+
|  role                       | true       | string        | N/A                         |                    |
+-----------------------------+------------+---------------+-----------------------------+--------------------+
|  resource_group             | false      | string        | resource_group              |                    |
+-----------------------------+------------+---------------+-----------------------------+--------------------+
|  name                       | true       | string        |  name                       |                    |
+-----------------------------+------------+---------------+-----------------------------+--------------------+
|  location                   | false      | string        |  location                   |                    |
+-----------------------------+------------+---------------+-----------------------------+--------------------+

azure_virtual_network
-------

Azure virtual network can be provisioned using this role

* Example <workspaces/azure/Pinfile>`
* azure_rm_virtualnetwork module <https://docs.ansible.com/ansible/latest/modules/azure_rm_virtualnetwork_module.html?highlight=azure%20virtual%20network>`_

Topology Schema
~~~~~~~~~~~~~~~

Within Linchpin, the :term:`azure_rm_virtualnetwork` :term:`resource_definition` has more
options than what is shown in the examples above. For each :term:`azure_rm_virtualnetwork`
definition, the following options are available.

+-----------------------------+------------+---------------+-----------------------------+--------------------+
| Parameter                   | required   | type          | ansible value               | comments           |
+=============================+============+===============+=============================+====================+
|  role                       | true       | string        | N/A                         |                    |
+-----------------------------+------------+---------------+-----------------------------+--------------------+
|  resource_group             | false      | string        | resource_group              |                    |
+-----------------------------+------------+---------------+-----------------------------+--------------------+
|  name                       | true       | string        |  name                       |                    |
+-----------------------------+------------+---------------+-----------------------------+--------------------+
|  address_prefixes           | false      | string        |  address_prefixes           |                    |
+-----------------------------+------------+---------------+-----------------------------+--------------------+

azure_virtual_subnet
-------

Azure network interface can be provisioned using this role

* Example <workspaces/azure/Pinfile>`
* azure_rm_subnet module <https://docs.ansible.com/ansible/latest/modules/azure_rm_subnet_module.html?highlight=azure%20subnet>`_

Topology Schema
~~~~~~~~~~~~~~~

Within Linchpin, the :term:`azure_rm_subnet` :term:`resource_definition` has more
options than what is shown in the examples above. For each :term:`azure_rm_subnet`
definition, the following options are available.

+-----------------------------+------------+---------------+-----------------------------+--------------------+
| Parameter                   | required   | type          | ansible value               | comments           |
+=============================+============+===============+=============================+====================+
|  role                       | true       | string        | N/A                         |                    |
+-----------------------------+------------+---------------+-----------------------------+--------------------+
|  resource_group             | false      | string        | resource_group              |                    |
+-----------------------------+------------+---------------+-----------------------------+--------------------+
|  name                       | true       | string        |  name                       |                    |
+-----------------------------+------------+---------------+-----------------------------+--------------------+
|  virtual_network_name       | false      | string        |  virtual_network_name       |                    |
+-----------------------------+------------+---------------+-----------------------------+--------------------+
|  address_prefix             | false      | string        |  address_prefix             |                    |
+-----------------------------+------------+---------------+-----------------------------+--------------------+


Credentials Management
----------------------
 Support IAM user (instruction below)         
 example: docs/source/example/workspaces/azure/azure.key

IAM Instruction
---------------------
⚫ FROM UI Azure website
1. Go to Azure Active Directory
2. Go to app registration on the left bar
3. Create a new app
4. Take notes of Application (client) ID (this is client_id)
5. Take notes of Directory (tenant) ID (this is tenant)
6. Go to Certificates & secrets on left bar 
7. Upload or create a new key and take note of it  (this is secret)
8. Go to the ACESS CONTROL of you resource group or subscription
9. Click Add button to add new role assignment
10. Assign the role of Contributor to the App you just created
11. Go to subscription find out the subscription id (this is subscription_id)
11. Fill out the form below and put it into your workplace
client_id:
tenant:
secret: 
subscription_id:

⚫ FROM AZ cmd line

accountname@Azure:~$ az ad sp create-for-rbac --name ServicePrincipalName
Changing "ServicePrincipalName" to a valid URI of "http://ServicePrincipalName", which is the required format used for service principal names
Creating a role assignment under the scope of "/subscriptions/dcc74c29-4db6-4c49-9a0f-ac0ee03fa17e"
  Retrying role assignment creation: 1/36
  Retrying role assignment creation: 2/36
  Retrying role assignment creation: 3/36
  Retrying role assignment creation: 4/36
{
  "appId": "xxxxxxxxxxxxxxxxxxxxxxxxxx",
  "displayName": "ServicePrincipalName",
  "name": "http://ServicePrincipalName",
  "password": "xxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxx",
  "tenant": "xxxxx-xxxxx-xxxx-xxxx-xxxxxxxxxxxx"
}

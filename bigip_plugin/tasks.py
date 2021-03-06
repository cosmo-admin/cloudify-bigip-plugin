########
# Copyright (c) 2014 GigaSpaces Technologies Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# * See the License for the specific language governing permissions and
#    * limitations under the License.

from cloudify.decorators import operation
from cloudify import ctx
from bip_proxy import BigIpProxy


""" Shortcut for obtaining a proxy object for BIG-IP.
Expected dictionary keys:

host: the BIG-IP hostname
username: used to authenticate against BIG-IP
password: used to authenticate against BIG-IP """


def _get_bip_proxy(d):
    hostname, username, password = [d[x] for x in ['host', 'username', 'password']]
    ctx.logger.debug('Constructing BIG-IP proxy: {0}/{1}'.format(hostname, username))
    return BigIpProxy(hostname, username, password)


""" Creates a pool.
Expected node-level properties:

pool_id: the pool's identifier
lb_method: load-balancing method (see LocalLB's documentation) """


@operation
def create_pool(**kwargs):
    pool_id, lb_method = [ctx.node.properties[x] for x in ['pool_id', 'lb_method']]
    ctx.logger.info('Creating pool: pool_id={0}, lb_method={1}'.format(pool_id, lb_method))
    _get_bip_proxy(ctx.node.properties).create_pool(pool_id, lb_method)


""" Deletes a pool.
Expected node-level properties:

pool_id: the pool's identifier """


@operation
def delete_pool(**kwargs):
    pool_id = ctx.node.properties['pool_id']
    ctx.logger.info('Deleting pool: id={0}'.format(pool_id))
    _get_bip_proxy(ctx.node.properties).delete_pool(pool_id)


""" Adds a member to a previously-created pool.
Expected source properties:

pool_id: the pool's identifier
host, username, password: parameters used to connect to BIG-IP

Operation parameters:

address: the member's address (hostname or IP address)
port:    the member's port """


@operation
def add_member(address, port, **kwargs):
    pool_id = ctx.source.node.properties['pool_id']
    ctx.logger.info('Adding member: pool id={0}, address={1}, port={2}'.format(pool_id, address, port))
    _get_bip_proxy(ctx.source.node.properties).add_member(pool_id, address, port)


""" Removes a member from a previously-created pool.
Expected source properties:

pool_id: the pool's identifier
host, username, password: parameters used to connect to BIG-IP

Operation parameters:

address: the member's address (hostname or IP address)
port:    the member's port """


@operation
def remove_member(address, port, **kwargs):
    pool_id = ctx.source.node.properties['pool_id']
    ctx.logger.info('Removing member: pool id={0}, address={1}, port={2}'.format(pool_id, address, port))
    _get_bip_proxy(ctx.source.node.properties).remove_member(pool_id, address, port)

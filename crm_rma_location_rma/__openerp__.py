# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Yanina Aular
#    Copyright 2014 Vauxoo
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{'name': 'RMA Location',
 'version': '1.0',
 'author': "Vauxoo, Odoo Community Association (OCA)",
 'license': 'AGPL-3',
 'category': 'Generic Modules/CRM & SRM',
 'depends': ['stock',
             'procurement',
             ],
 'description': """
RMA Location
============

Bridge Module.

RMA Location added in warehouse to control products in rma.

 """,
 'website': 'http://www.camptocamp.com',
 'data': ['stock_warehouse_view.xml',
          ],
 'installable': True,
 'auto_install': False,
 }
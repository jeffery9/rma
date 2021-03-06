# -*- coding: utf-8 -*-
# ########################################################################
#                                                                        #
#                                                                        #
# ########################################################################
#                                                                        #
# Copyright (C) 2009-2011  Akretion, Emmanuel Samyn, Benoît Guillot      #
#                                                                        #
# This program is free software: you can redistribute it and/or modify   #
# it under the terms of the GNU General Public License as published by   #
# the Free Software Foundation, either version 3 of the License, or      #
# (at your option) any later version.                                    #
#                                                                        #
# This program is distributed in the hope that it will be useful,        #
# but WITHOUT ANY WARRANTY; without even the implied warranty of         #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
# GNU General Public License for more details.                           #
#                                                                        #
# You should have received a copy of the GNU General Public License      #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.  #
##########################################################################

from openerp import models, fields, api


class return_instruction(models.Model):

    _name = "return.instruction"
    _description = "Instructions for product return"

    name = fields.Char('Title', required=True)

    instructions = fields.Text(
        'Instructions',
        help="Instructions for product return")

    is_default = fields.Boolean('Is default',
                                help="If is default, will be use "
                                "to set the default value in "
                                "supplier infos. Be careful to "
                                "have only one default")


class product_supplierinfo(models.Model):

    _inherit = "product.supplierinfo"

    @api.model
    def get_warranty_return_partner(self):
        result = [('company', 'Company'),
                  ('supplier', 'Supplier'),
                  ('other', 'Other'),
                  ]
        return result

    @api.model
    def _get_default_instructions(self):
        """ Get selected lines to add to exchange """
        instruction_ids = self.env['return.instruction']\
            .search([('is_default', '=', True)])
        if instruction_ids:
            return instruction_ids[0]
        else:
            return instruction_ids

    @api.depends('warranty_return_partner')
    def _get_warranty_return_address(self):
        """ Method to return the partner delivery address or if none,
        the default address

        dedicated_delivery_address stand for the case a new type of
        address more particularly dedicated to return delivery would be
        implemented.

        """
        for record in self:
            return_partner = record.warranty_return_partner
            partner_id = record.company_id.partner_id.id
            if return_partner:
                if return_partner == 'supplier':
                    partner_id = record.name.id
                elif return_partner == 'company':
                    if record.company_id.crm_return_address_id:
                        partner_id = record.company_id.\
                            crm_return_address_id.id
                elif return_partner == 'other':
                    if record.warranty_return_other_address:
                        partner_id = record.\
                            warranty_return_other_address.id
                record.warranty_return_address = partner_id

    warranty_duration = fields.Float(
        'Period',
        help="Warranty in month for this product/supplier relation. Only "
             "for company/supplier relation (purchase order) ; the  "
             "customer/company relation (sale order) always use the "
             "product main warranty field")

    warranty_return_partner = fields.Selection(
        get_warranty_return_partner,
        'Return type',
        required=True,
        default='company',
        help="Who is in charge of the warranty return treatment toward the"
                " end customer. Company will use the current compagny "
                " delivery or default address and so on for supplier and "
                "brand manufacturer. Doesn't necessarly mean that the "
                "warranty to be applied is the one of the return partner "
                "(ie: can be returned to the company and be under the "
                "brand warranty")

    return_instructions = fields.Many2one(
        'return.instruction',
        'Instructions',
        default=_get_default_instructions,
        help="Instructions for product return")

    active_supplier = fields.Boolean(
        'Active supplier',
        help="Is this supplier still active, only for information")

    warranty_return_address = fields.Many2one(
        'res.partner',
        compute='_get_warranty_return_address',
        string="Return address",
        help="Where the goods should be returned  "
             "(computed field based on other infos.)")

    warranty_return_other_address = fields.Many2one(
        'res.partner',
        string='Return address',
        help="Where the customer has to send back the product(s) "
             "if warranty return is set to 'other'.")

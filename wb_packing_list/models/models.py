# -*- coding: utf-8 -*-
from odoo import models, exceptions, fields, api, _
from odoo.exceptions import Warning 
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError
from odoo import exceptions
import datetime
import logging

from odoo.tools.float_utils import float_compare, float_is_zero, float_round

class Packing_List(models.Model):
    _inherit = 'stock.picking.batch'
    se_imprimio_lista = fields.Boolean(string='Lista de Empaque')

    @api.multi
    def packing_list_print(self): 
        _logger = logging.getLogger(__name__)
        _logger.info('Nombre operación %s', self.name)

        pickings = self.mapped('picking_ids')
        if not pickings:
            raise UserError(_('Nada que imprimir.'))
        return self.env.ref('packing_list.action_packing_list_report').report_action(self)

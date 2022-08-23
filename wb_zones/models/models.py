# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api, _
from odoo import exceptions
from odoo.exceptions import Warning 

class zones(models.Model):
    _name = 'zones'
    _description = 'Zonas de Picking'
    _rec_name = 'empleado_zone'

    empleado_zone = fields.Many2one('res.users','Usuario',required=True, default=lambda self: self.env.uid, widget =" many2many_tags")
    zone = fields.Char('Zona', required=True, help='Introduce un nombre de la Zona donde vas a realizar la recolección')
    marcas_zone = fields.Char('Marcas')

    #@api.multi
    def name_get(self):
        res = []
        for record in self:
            res.append((record.id, "%s %s" % (record.empleado_zone.name, record.zone)))
        return res


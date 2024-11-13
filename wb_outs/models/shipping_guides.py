# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CodesOfShipping(models.Model):
    _name = 'wb_outs.guide_codes'
    _description = 'wb_outs.guide_codes'

    code = fields.Char(
        string = "Shipping code",
        required = True
    )

    shiping_guide_id = fields.Many2One(
        string ="Shipping guide",
        comodel_name = "wb_outs.master_shipping_guides"
    )

class MasterShippingGuides(models.Model):
    _name = 'wb_outs.master_shipping_guides'
    _description = 'wb_outs.master_shipping_guides'

    #A SHIPPING GUIDE HAS A SALE ORDER ATTACH TO IT
    sale_id = fields.Many2one(
        string = "Sale ID",
        comodel_name = "sale.order"
    )

    number_sg = fields.Integer(
        string = "Number of Shipping guide", 
        readonly = True
    )

    #IT CAN HAVE ONE OR MULTIPLE PRODUCTS OF THE
    #SALE ORDER ATTACHED TO IT
    products_ids = fields.One2many(
        string = "Products",
        comodel_name = "product.product",
        inverse_name = "shiping_guide_id"
    )

    possible_scannable_codes = fields.One2many(
        string = "Codes",
        comodel_name = "wb_outs.guide_codes",
        inverse_name = "shiping_guide_id"
    )

    #CHECK IF THE GUIDE HAS BEEN SCANNED
    scanned = fields.Boolean(
        string = "Scanned"
    )

    #CHECK WHEN THE GUIDE HAS BEEN SCANNED
    scanned_timestamp = fields.Datetime(
        string = "Scanned at"
    )

    #CHECK WHO SCANNED THE GUIDE
    scanned_by = fields.Many2one(
        string = "Scanned by",
        comodel_name = "res.users"
    )

    #########################################################
    #THIS FIELDS ARE MERELY INFORMATIVE AND SHOULD COME FROM
    #THE SALE ORDER 
    carrier = fields.Many2one(
        compute = '_compute_carier',
        string = "Carrier",
        comodel_name = "sale.order",
    )
    @api.depends('sale_id')
    def _compute_carier(self):
        for record in self:
            sale_id = record.sale_id
            if not sale_id:
                record.carrier = False
                return None
            else:
                sale_id_carrier = sale_id.carrier_selection_relational
                record.carrier = False if not sale_id_carrier else sale_id_carrier
                return None

    #LOG THE STOCK MOVEMENTS
    stock_movs = fields.One2many(
        string = "Stock movements",
        comodel_name = "stock.picking",
        inverse_name = "shiping_guide_id",
        compute = '_compute_stock',
    ) 

    def get_stock_mov(self, stock_mov_type):
        if not self.sale_id:
            return False
        else:
            sale_id = self.sale_id.name
            stock_movement = self.env["stock.picking"].search(
                [
                    ("origin", "=", sale_id),
                    ("name", "ilike", stock_mov_type)
                ]
            )
            return False if len(stock_movement)<=0 else stock_movement[0]
        
    @api.depends('sale_id')    
    def _compute_stock(self):
        movement_stock_type = [
            "/PICK/",
            "/VALPICK/",
            "/OUT/"
        ]
        for record in self:
            record.stock_movs = [(5, 0, 0)]
            for mov_type in movement_stock_type:
                stock_mov_id = self.get_stock_mov(mov_type)
                if stock_mov_id:
                    self.field = [(4, stock_mov_id.id, 0)]

    #NAME, COMPOSED BY THE SALE ORDER, 
    #THE NUM IF THERE ARE MORE SHIPPING GUIDES AND THE CARRIER
    name = fields.Char(
        string = "Shipping ID",
        compute = '_compute_name',
    ) 

    @api.depends('sale_id')    
    def _compute_name(self):
        for record in self:
            sale_id = record.sale_id
            carrier_id = record.carrier
            
            sale_name = "" if not sale_id else sale_id.name
            carrier_name = "" if not carrier_id else carrier_id.name

            #IS THERE ANOTHER SHIPPING GUIDE FOR THIS SALE ORDER
            if sale_id:
                other_sg = self.env["wb_outs.master_shipping_guides"].search(
                    [
                        ("sale_id", "=", sale_id)
                    ]
                )
                if len(other_sg)>0:
                    tmp_int = 0
                    for sg in other_sg:
                        if sg.number_sg > tmp_int:
                            tmp_int = sg.number_sg
                    record.number_sg = tmp_int+1
                else:
                    record.number_sg = 1

                record.name = f"{sale_name}({record.number_sg}) - {carrier_name}"
            
            else:
                record.name = ""
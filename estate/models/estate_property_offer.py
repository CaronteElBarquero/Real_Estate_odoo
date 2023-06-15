from odoo import api,fields, models
from odoo.exceptions import UserError

from datetime import timedelta


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Real Estate Property Offer'
    _order = 'price desc'

    price = fields.Float('Price', required=True)
    validity_days = fields.Integer('Validity', default=7)
    create_date = fields.Date('Creation Date', default=fields.Date.today)
    date_deadline = fields.Date('Deadline', compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    status = fields.Selection(
        
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        copy = False,
        # help='Se usa para poder determinar el estado de la oferta'
    )

    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    property_type_id = fields.Many2one('estate.property.type', related='property_id.type_id', store=True)

    _sql_constraints = [
        (
            "check_price",
            "CHECK(price > 0)",
            "El precio de oferta debe ser mayor que 0",
        ),
    ]

    def action_accepted(self):
        self.ensure_one()
        if self.property_id.state == "offer_accepted":
            raise UserError("No se puede aceptar una oferta si ya hay una oferta aceptada")
        
        self.write({'status': 'accepted'})
        self.property_id.write({'state': 'offer_accepted', 'partner_id': self.partner_id.id, 'selling_price': self.price})


    def action_refused(self):
        self.ensure_one()
        self.write({'status': 'refused'})
        self.property_id.write({"state": "offer_received"})

    
    @api.model
    def create(self, vals):
        property_id = self.env['estate.property'].browse(vals['property_id'])
        if property_id.state == "sold":
            raise UserError("No se puede crear una oferta para una propiedad vendida")
        property_id.state = "offer_received"
        if vals.get('price', 0) < property_id.best_price:
            raise UserError("El precio de la oferta debe ser mayor que la mejor oferta actual")
        return super().create(vals)


    @api.depends("validity_days")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date & record.validity_days:
                record.date_deadline = record.create_date + timedelta(days=record.validity_days)
            else:
                record.date_deadline = fields.Date.today()


    def _inverse_date_deadline(self):
        for record in self:
            delta = record.date_deadline - record.create_date
            record.validity_days = delta.days
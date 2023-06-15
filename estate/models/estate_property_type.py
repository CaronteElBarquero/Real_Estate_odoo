from odoo import api,fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Real Estate Property Type'
    _order = 'name asc'

    name = fields.Char('Name', required=True)
    property_ids = fields.One2many('estate.property', 'type_id', string='Properties')
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string='Offers')
    offer_count = fields.Integer(
        string='Offer Count',
        compute='_compute_offer_count',
    )

    sequence = fields.Integer(
        string='Sequence',
        default=1,
        help='Se usa para poder determinar el orden de los tipos de propiedades'
    )

    _sql_constraints = [
        ("check_name", "UNIQUE(name)", "El nombre debe ser unico"),
    ]

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

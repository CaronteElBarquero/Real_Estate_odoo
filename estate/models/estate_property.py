from odoo import api,fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare

from datetime import timedelta


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'
    _order = 'id desc'

    name = fields.Char('Name', required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price')
    bedrooms = fields.Integer('Bedrooms')
    living_area = fields.Integer('Living Area')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area')
    
    
    garden_orientation = fields.Selection(
        string='Orientacion del Jardin',
        selection=[('norte', 'Norte'), ('sur', 'Sur'), ('este', 'Este'), ('oeste', 'Oeste')],
        help='Se usa para poder determinar la orientacion del jardin'
    )

    date_availability = fields.Date('Date Availability', default=lambda self: fields.Date.today() + timedelta(days=90))
    active = fields.Boolean('Active', default=True)
    user_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)

    state = fields.Selection(
        copy=False,
        required=True,
        default='new',
        string='States',
        selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'),
                     ('sold', 'Sold'), ('canceled', 'Canceled')],
        # help='Se usa para poder determinar el estado de la propiedad'
    )

    total_area = fields.Integer(
        string='Total Area',
        compute='_compute_total_area',
    )

    best_price = fields.Float(
        compute='_compute_best_price',
    )

    type_id = fields.Many2one('estate.property.type', string='Property Type')

    partner_id = fields.Many2one('res.partner', string='Buyer')
    tag_ids = fields.Many2many('estate.property.tag', string='Property Tags')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Property Offers')

    _sql_constraints = [
        (
            "check_expected_price",
            "CHECK(expected_price > 0)",
            "El precio esperado debe ser mayor que 0",
        ),
        (
            "check_selling_price",
            "CHECK(selling_price > 0)",
            "El precio de venta debe ser mayor que 0",
        ),
    ]

    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area


    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0.0


    @api.onchange("garden")
    def _onchange_garden(self):
        if not self.garden:
            self.garden_area = 0
            self.garden_orientation = False
        else:
            self.garden_area = 10
            self.garden_orientation = 'norte'


    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for record in self:
            calculated_selling_price = record.expected_price * 0.9
            for offers in record.offer_ids:
                if offers.status == "accepted":
                    if float_compare(record.selling_price, calculated_selling_price, 2) < 0:
                        raise ValidationError("El precio de venta no puede ser menor que el 90% del precio esperado")


    def unlink(self):
        for record in self:
            if record.state == "sold" or record.state == "new":
                raise UserError("No se puede eliminar una propiedad vendida o nueva")
        return super().unlink()


    def action_set_sold(self):
        self.ensure_one()
        if self.state == "canceled":
            raise UserError("No se puede vender una propiedad cancelada")
        elif self.state != "offer_accepted":
            raise UserError("No se puede vender una propiedad que no tiene una oferta aceptada")
        self.state = "sold"


    def action_set_cancel(self):
        self.ensure_one()
        if self.state == "sold":
            raise UserError("No se puede cancelar una propiedad vendida")
        self.state = "canceled"








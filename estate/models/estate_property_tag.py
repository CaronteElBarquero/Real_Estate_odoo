from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate property tag"
    _order = "name asc"

    name = fields.Char("Title", required=True, translate=True)
    color = fields.Integer("Color")

    _sql_constraints = [
        ("check_name", "UNIQUE(name)", "El nombre debe ser unico"),
    ]

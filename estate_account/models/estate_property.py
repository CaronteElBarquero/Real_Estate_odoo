from odoo import fields, models

class EstateProperty(models.Model):

    _inherit = 'estate.property'

    def action_set_sold(self):
        

        accountMove = self.env["account.move"]
        journal = accountMove.with_context(default_move_type="out_invoice")._get_default_journal()

        accountMove = self.env["account.move"].create({
            "partner_id": self.partner_id.id,
            "move_type": "out_invoice",
            "journal_id": journal.id,
            "invoice_line_ids": [
                (
                    0,
                    0,
                    {
                        "name": self.name,
                        "quantity": 1,
                        "price_unit": self.selling_price * 0.06,
                    },
                ),
                (
                    0,
                    0,
                    {
                        "name": "Administrative Fees",
                        "quantity": 1,
                        "price_unit": 100.00,
                    },
                ),
            ],
        })


        return super().action_set_sold()

from odoo import fields, models

class ResUsers(models.Model):
    _inherit = "res.users"

    book_ids = fields.One2many("library.book", "librarian_id", domain=[('state', 'in', ('available', 'not_available'))])

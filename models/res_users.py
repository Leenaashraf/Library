from odoo import fields, models

class ResUsers(models.Model):
    _inherit = "res.users"

    book_ids = fields.One2many("library.book", "librarian_id", domain=[('state', 'in', ('available', 'borrowed'))])
    wishlist_book_ids = fields.Many2many("library.book", "library_book_wishlist_rel", "user_id", "book_id", string="My Wishlist")
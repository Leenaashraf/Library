from odoo import models, fields

class LibraryBookTag(models.Model):
    _name = "library.book.tag"
    _description = "Book Tags"

    name = fields.Char(string="Tag Name", required=True)
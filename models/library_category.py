from odoo import models, fields

class LibraryCategory(models.Model):
    _name = "library.category"
    _description = "Book Categories"

    name = fields.Char(string="Category Name", required=True)
    description = fields.Text(string="Description")

    _check_name = models.Constraint(
        "UNIQUE(name)",
        "Category name must be unique"
    )
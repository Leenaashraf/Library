from odoo import models, fields

class LibraryAuthor(models.Model):
    _name = "library.author"
    _description = "Library Author"

    name = fields.Char(string = "Author Name", required=True)
    biography = fields.Text(strings="Biography")
    email=fields.Char(string="Email")
    phone=fields.Char(string="Phone")
    nationality=fields.Char(string="Nationality")
    date_of_birth=fields.Char(string="Date of Birth")

    book_ids=fields.One2many("library.book", "author_id", string="Book")
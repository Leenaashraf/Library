from odoo import models, fields, api
from odoo.exceptions import UserError

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Books'

    name = fields.Char(string="Title", required=True)
    author = fields.Char(string="Author", required=True)
    isbn = fields.Char(string="ISBN")
    publication_year = fields.Date(string="Publication Date")
    description = fields.Text(string="Description")
    total_copies = fields.Integer(string="Total Copies", default=1)
    available_copies = fields.Integer(string="Available Copies", compute="_compute_available_copies", store=True)
    category_id = fields.Many2one("library.category", string="Category")
    borrow_record_ids = fields.One2many("library.borrow.record", "book_id", string="Borrow Records")
    state = fields.Selection(
        selection=[
            ('available', 'Available'),
            ('borrowed', 'Borrowed'),
            ('lost', 'Lost'),
            ('damaged', 'Damaged')
        ],
        default='available',
        string="Status"
    )
    tag_ids = fields.Many2many("library.book.tag", string="Tags")
    librarian_id = fields.Many2one("res.users", string="Librarian", default=lambda self: self.env.user)

    @api.depends("total_copies", "borrow_record_ids.state")
    
    def _compute_available_copies(self):
        for record in self:
            active_borrows = self.env["library.borrow.record"].search_count([
                ("book_id", "=", record.id),
                ("state", "=", "borrowed")
            ])
            record.available_copies = record.total_copies - active_borrows
            if record.available_copies <= 0:
                record.state = 'borrowed'
            elif record.state == 'borrowed':
                record.state = 'available'

    def mark_lost(self):
        for record in self:
            if record.state == 'borrowed':
                raise UserError("Cannot mark as lost while book is borrowed")
            record.state = 'lost'

    def mark_damaged(self):
        for record in self:
            if record.state == 'borrowed':
                raise UserError("Cannot mark as damaged while book is borrowed")
            record.state = 'damaged'

    def restore_book(self):
        for record in self:
            record.state = 'available'

    _check_total_copies = models.Constraint(
        "CHECK(total_copies > 0)",
        "Total copies must be greater than 0"
    )
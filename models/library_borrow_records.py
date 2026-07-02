from odoo import api, models, fields
from odoo.exceptions import UserError
from datetime import timedelta

class LibraryBorrowRecord(models.Model):
    _name = "library.borrow.record"
    _description = "Library Borrow Records"

    name = fields.Char(string="Reference", compute="_compute_name")
    book_id = fields.Many2one("library.book", string="Book", required=True)
    member_id = fields.Many2one("library.member", string="Member", required=True)
    borrow_date = fields.Date(string="Borrow Date", default=fields.Date.today)
    due_date = fields.Date(string="Due Date", compute="_compute_due_date", store=True)
    return_date = fields.Date(string="Return Date")
    state = fields.Selection(
        selection=[
            ('borrowed', 'Borrowed'),
            ('returned', 'Returned'),
            ('overdue', 'Overdue'),
            ('lost', 'Lost')
        ],
        default='borrowed'
    )
    librarian_id = fields.Many2one("res.users", string="Processed By", default=lambda self: self.env.user)
    notes = fields.Text(string="Notes")

    @api.depends("book_id", "member_id")
    def _compute_name(self):
        for record in self:
            record.name = f"{record.book_id.name or ''} - {record.member_id.name or ''}"

    @api.depends("borrow_date")
    def _compute_due_date(self):
        for record in self:
            if record.borrow_date:
                record.due_date = record.borrow_date + timedelta(days=14)

    def lend_book(self):
        for record in self:
            if record.book_id.available_copies <= 0:
                raise UserError("No copies available for lending")
            if record.member_id.state != 'active':
                raise UserError("Member is not active")
            if record.state != 'borrowed':
                raise UserError("Record is not in borrowed state")
            record.book_id.state = 'not_available'

    def return_book(self):
        for record in self:
            if record.state not in ('borrowed', 'overdue'):
                raise UserError("Only borrowed or overdue books can be returned")
            record.state = 'returned'
            record.return_date = fields.Date.today()

    def mark_overdue(self):
        for record in self:
            if record.state == 'borrowed' and record.due_date < fields.Date.today():
                record.state = 'overdue'

    def mark_lost(self):
        for record in self:
            if record.state not in ('borrowed', 'overdue'):
                raise UserError("Only borrowed or overdue records can be marked as lost")
            record.state = 'lost'
            record.book_id.total_copies -= 1
            if record.book_id.total_copies <= 0:
                record.book_id.state = 'lost'

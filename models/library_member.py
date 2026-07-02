from odoo import models, fields
from odoo.exceptions import UserError

class LibraryMember(models.Model):
    _name = "library.member"
    _description = "Library Members"

    name = fields.Char(string="Member Name", required=True)
    email = fields.Char(string="Email")
    phone = fields.Char(string="Phone")
    member_id = fields.Char(string="Member ID", required=True, copy=False)
    active_borrow_count = fields.Integer(string="Active Borrows", compute="_compute_active_borrow_count")
    borrow_record_ids = fields.One2many("library.borrow.record", "member_id", string="Borrow Records")
    state = fields.Selection(
        selection=[
            ('active', 'Active'),
            ('suspended', 'Suspended'),
            ('expired', 'Expired')
        ],
        default='active'
    )

    def _compute_active_borrow_count(self):
        for record in self:
            record.active_borrow_count = self.env["library.borrow.record"].search_count([
                ("member_id", "=", record.id),
                ("state", "=", "borrowed")
            ])

    def suspend_member(self):
        for record in self:
            if record.active_borrow_count > 0:
                raise UserError("Cannot suspend member with active borrows")
            record.state = 'suspended'

    def activate_member(self):
        for record in self:
            record.state = 'active'
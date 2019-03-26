from odoo import api, fields, models, _
import time

SESSION_STATES =[('draft','Draft'),('confirmed','Confirmed'),
                 ('done','Done')]

class session(models.Model):
    _name = 'academic.session'

    name = fields.Char("Name", required=True)

    course_id = fields.Many2one(comodel_name="academic.course",
                                string="Course", required=False, )
    instructor_id  = fields.Many2one(comodel_name="res.partner",
                                     string="Instructor", required=False, )
    start_date  = fields.Date(string="Start Date", required=False,
                              default=lambda self:time.strftime("%Y-%m-%d"))
    duration = fields.Integer(string="Duration", required=False, )
    seats = fields.Integer(string="Seats", required=False, )
    active  = fields.Boolean(string="Active", default=True)
    
    attendee_ids = fields.One2many(comodel_name="academic.attendee",
                                   inverse_name="session_id",
                                   string="Attendees",
                                   required=False, )

    taken_seats = fields.Float(compute="_calc_taken_seats", string="Taken Seat", required=False, )

    image_small  = fields.Binary(string="Image Small",  )
    
    state = fields.Selection(string="State", selection=SESSION_STATES,
                             required=True,
                             readonly=True,
                             default=SESSION_STATES[0][0])
    
    
    @api.multi
    def action_draft(self):
        self.state = SESSION_STATES[0][0]
        
    @api.multi
    def action_confirm(self):
        
        self.state = SESSION_STATES[1][0]
        
    @api.multi
    def action_done(self):
        self.state = SESSION_STATES[2][0]
        
    
    @api.depends('attendee_ids','seats')
    def _calc_taken_seats(self):
        for rec in self:
            if rec.seats>0:
                rec.taken_seats = 100.0 * len(rec.attendee_ids)/rec.seats
            else:
                rec.taken_seats = 0.0
        
    @api.onchange('seats')
    def onchange_seats(self):
        if self.seats>0:
            self.taken_seats = 100.0 * len(self.attendee_ids)/self.seats
        else:
            self.taken_seats = 0.0

    @api.multi
    def _cek_instruktur(self):
        for session in self:
            x = [att.partner_id.id for att in session.attendee_ids]
            if session.instructor_id.id in x:
                return False

        return True

    _constraints = [(_cek_instruktur, 'Instructor cannot be Attendee', ['instructor_id', 'attendee_ids'])]

    
    @api.multi
    def copy(self, default=None):
        self.ensure_one()
        default = dict(default or {},
                       name=_('Copy of %s') % self.name)
        return super(session, self).copy(default=default)

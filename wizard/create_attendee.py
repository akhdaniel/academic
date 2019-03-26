from odoo import api, fields, models, _

class CreateAttendeeWizard(models.TransientModel):
    _name = 'academic.create.attendee.wizard'


    def _get_default_session(self):
        context = self.env.context
        if context.get('active_model') == 'academic.session':
            return context.get('active_ids', False)
        return False


    #session_id = fields.Many2one(comodel_name="academic.session",
    #                             string="Session", required=False, 
    #                             default=_get_default_session
    #                             )

    session_ids = fields.Many2many(comodel_name="academic.session",
                                 string="Session", required=False, 
                                 default=_get_default_session
                                 )

    attendee_ids = fields.One2many(comodel_name="academic.attendee.wizard",
                                   inverse_name="wizard_id",
                                   string="Attendees to Add",
                                   required=False, )

    @api.multi  
    def action_add_attendee(self):
      self.ensure_one()
      sessions = self.session_ids

      # att_data = [{'parner_id':1}, {'partner_id':2}, {'partner_id':3}]
      att_data = [{'partner_id': att.partner_id.id} 
        for att in self.attendee_ids]

      # attendee_ids = [(0,0,{'parner_id':1}), (0,0,{'parner_id':2}), (0,0,{'parner_id':3})]
      for session in sessions:
        session.attendee_ids = [(0, 0, data) for data in att_data]

      return {'type': 'ir.actions.act_window_close'}


class AttendeeWizard(models.TransientModel):
    _name = 'academic.attendee.wizard'
    
    wizard_id = fields.Many2one(
               comodel_name = "academic.create.attendee.wizard",
               string="Wizard", required=False, )
    partner_id = fields.Many2one(comodel_name="res.partner",
               string="Partner", required=True, )

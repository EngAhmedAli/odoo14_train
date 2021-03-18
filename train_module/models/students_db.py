# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from datetime import datetime,date

STATE = [('draft', 'Draft'),
         ('med_interview', 'Medical Interview'),
         ('acad_interview', 'Academic Interview'),
         ('first_register', 'First Year Registered'),
         ('second_register', 'Second Year Registered'),
         ('third_register', 'Third Year Registered'),
         ('fourth_register', 'Fourth Year Registered'),
         ('dismiss', 'Dismissed'),
         ('alumni', 'Alumni')
         ]
###################################################################################################
class salesinherit(models.Model):
    _inherit = "sale.order"

    services_type = fields.Selection([("free","Free"),("paied","Paied")],string="Services Type",default="free")
###################################################################################################
class student_student(models.Model):
    _name = "student.student"
    _description = "Student Information"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name", required=True, index=True, translate=True)
    active = fields.Boolean(string="Active", default=True)
    image = fields.Binary("Image")
    uni_no = fields.Char(string="Ministry University No.", required=True, copy=False)
    seat_no = fields.Char(string="Seat No.")
    dob = fields.Date(string="Date of Birth", required=True)
    age = fields.Integer(string="Age",readonly=True,store=True,compute="_get_calc_age")
    @api.onchange('dob')
    def _get_calc_age(self):
        for rec in self:
            d1 = datetime.strptime(str(date.today()),"%Y-%m-%d")
            d2 = datetime.strptime(str(rec.dob),"%Y-%m-%d")
            rec.age = (d1-d2).days/365
    gender = fields.Selection([("male", "Male"), ("female", "Female")], "Gender", default="male")
    fdate = fields.Date("First Registration Date")
    ldate = fields.Datetime("Last Registration Date", readonly=True)
    degree_id = fields.Many2one("degree.detail", "Degree to Register For")
    result_ids = fields.One2many("schoolresult.result", "student_id", "Subject's Results")
    hobbies_ids = fields.Many2many("hobbies.details", "student_hobbies_rel", "student_id", "hobbie_id",
                                   "Hobbies Information")
    regfees = fields.Float("Registration Fees", default="0.0")
    tutfees = fields.Float("Tuition Fees ($)", default="0.0")
    @api.onchange('degree_id')
    def _get_tutfees(self):
        for rec in self:
            self.tutfees = self.degree_id.degfees
    totfees = fields.Float(string="Total Fees ($)", store=True, readonly=True, compute='_get_total_fees')

    @api.depends('regfees', 'tutfees')
    def _get_total_fees(self):
        for record in self:
            if not record.regfees:
                self.totfees = record.regfees + record.tutfees
            else:
                self.totfees = record.regfees + record.tutfees

    ref = fields.Reference(
        selection=[("res.partner", "Partner"), ("res.users", "User"), ("student.student", "Student")],
        string="Reference")
    ref_link = fields.Char("External Link")
    responsible_id = fields.Many2one("res.partner", "Responsible Person / Next Of Kin")
    phone = fields.Char(related="responsible_id.phone", string="NOK Phone")
    email = fields.Char(related="responsible_id.email", string="NOK Email")
    health_issues = fields.Selection([("yes", "Yes"), ("no", "No")], "Health Issues", default="no")
    health_notes = fields.Text("Health Issue(s) Details", copy=False)
    template = fields.Html("Template")
    # Represents state of student
    state = fields.Selection(STATE, "Status", readonly=True, default="draft")
    quality_check = fields.Selection([('',''),('good','good'),('very_good','very_good'),('excellent','excellent')],string="Quality Check")
    student_sequence = fields.Char(string='Number', required=True, copy=False, readonly=True,
                                   index=True, default=lambda self: _('New'))

    @api.model
    def create(self, vals):
        if vals.get('student_sequence', _('New')) == _('New'):
            vals['student_sequence'] = self.env['ir.sequence'].next_by_code('student.Sequence') or _('New')
        result = super(student_student, self).create(vals)
        return result


##########################################################################################################
class schoolresult_result(models.Model):
    _name = "schoolresult.result"
    _description = "student's Secondary School Results"

    student_id = fields.Many2one("student.student", "Student")
    subject_id = fields.Many2one("schoolresult.subject", "Subject")
    result = fields.Float("Result")


##########################################################################################################
class schoolresult_subject(models.Model):
    _name = "schoolresult.subject"
    _description = "student's Secondary School Subjects"

    name = fields.Char("Subject")


##########################################################################################################
class hobbies_details(models.Model):
    _name = "hobbies.details"
    _description = "Student hobbies"

    name = fields.Char("Name")


###################################################################################################
class degree_detail(models.Model):
    _name = "degree.detail"
    _description = "A registry of all possible degrees offered by university / college"

    name = fields.Char("Name", required=True)
    # Department or faculty
    dorf_id = fields.Many2one("dorf.information", "Department or Faculty", required=True)
    # Department or division
    dord_id = fields.Many2one("dord.information", "Division or Department")
    degfees = fields.Float("Fees per Year ($)")
###################################################################################################
class dorf_information(models.Model):
    _name = "dorf.information"
    _description = "A registry of all departments or faculties"
    _rec_name = 'code'

    code = fields.Char("Code", required=True)
    name = fields.Char("Name", required=True)

    # Make faculty name unique
    _sql_constraints = [
        ('dorf_code_unique',
         'UNIQUE(code)',
         "Faculty name must be unique!"),
    ]
###################################################################################################
class dord_information(models.Model):
    _name = "dord.information"
    _description = "A registry of all divisions or departments"
    _rec_name = 'code'

    code = fields.Char("Code", required=True)
    name = fields.Char("Name", required=True)
    # A division / department is owned by a department / faculty
    dorf_id = fields.Many2one("dorf.information", "Department or Faculty", required=True)
###################################################################################################
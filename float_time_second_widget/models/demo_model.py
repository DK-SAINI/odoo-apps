# -*- coding: utf-8 -*-

from odoo import models, fields


class DemoModel(models.Model):
    _name = "demo.model"
    _description = "Demo Model for Float Time Second"

    time_value = fields.Float(string="Time (HH:MM:SS)")

from odoo import fields, models


class SurveyQuestion(models.Model):
    _inherit = "survey.question"

    should_be_equal = fields.Boolean("The total value MUST be equal")
    error_message = fields.Char(string="Client error message")
    condition_to_meet = fields.Integer(string="Condition to meet (Up to OR equal)")
    apply_condition = fields.Boolean(string="Apply condition")

    def _validate_matrix(self, answers):
        if self.apply_condition:
            ids = [int(item[0]) for item in answers.values()]
            answers_ids = self.env["survey.question.answer"].browse(ids)
            sum_answers = sum(answers_ids.mapped("weight"))
            if (self.should_be_equal and sum_answers != self.condition_to_meet) or (
                not self.should_be_equal and sum_answers > self.condition_to_meet
            ):
                return {self.id: self.error_message}
        return super()._validate_matrix(answers)

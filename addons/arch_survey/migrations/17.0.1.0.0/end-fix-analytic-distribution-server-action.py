from odoo.upgrade import util


def migrate(cr, version):
    env = util.env(cr)
    server_action = env.ref("studio_customization.pre_remplir_compte_a_e314d19b-847c-4813-951f-d37f4d2e535b")
    server_action.state = "code"
    server_action.code = (
        """record.write({"analytic_distribution": dict([(record.x_studio_account_analytic_id.id,100)])})"""
    )

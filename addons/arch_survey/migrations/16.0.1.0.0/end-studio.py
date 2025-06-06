import logging

from odoo.upgrade import util
from odoo.upgrade.custom_util import (
    AddElements,
    RemoveElements,
    RemoveFields,
    ReplaceValue,
    UpdateAttributes,
    activate_views,
    edit_views,
)


_logger = logging.getLogger(__name__)


def remove_fields_from_models(cr):
    models_and_fields = {
        "account.move": ["x_studio_compte_analytique", "x_studio_dossier", "x_studio_projet"],
        "account.payment": [
            "x_studio_projet",
            "x_studio_projetd",
            "x_studio_comp",
            "x_studio_compte_analytiqu",
            "x_studio_dossier",
            "x_studio_many2one_field_XwLu4",
            "x_studio_many2one_field_hjZ4X",
        ],
        "account.bank.statement.line": [
            "x_studio_projet",
            "x_studio_projetd",
            "x_studio_comp",
            "x_studio_compte_analytiqu",
            "x_studio_dossier",
            "x_studio_many2one_field_XwLu4",
            "x_studio_many2one_field_hjZ4X",
        ],
        "purchase.order.line": ["x_studio_compte_analytique", "x_studio_projet", "x_studio_related_field_Fs6lN"],
        "stock.picking": ["x_studio_projet"],
        "project.project": [
            "x_studio_purchase_lines_ids",
            "x_studio_montant_des_achats",
            "x_studio_marge_complementaire",
            "x_studio_marge_consolidee",
            "x_studio_marge_reelle",
            "x_studio_marge_reelle_valeur",
        ],
    }

    for model, fields in models_and_fields.items():
        for field in fields:
            util.remove_field(cr, model, field, cascade=True)


def add_invisible_sibling(field_name, position, path=""):
    return AddElements(
        f"{path}//field[@name='{field_name}']",
        f"""
            <field name="{field_name}" invisible="1"/>
            """,
        position,
    )


VIEW_OPERATIONS = {
    "studio_customization.odoo_studio_project__c0ea6d5e-1da7-4b39-9682-84189e1852c5": [
        RemoveFields(
            [
                "x_studio_marge_reelle_valeur",
                "x_studio_marge_complementaire",
                "x_studio_marge_consolidee",
                "x_studio_marge_reelle",
                "x_studio_montant_des_achats",
            ]
        ),
        UpdateAttributes(
            """//xpath[@expr="//tree[1]/field[@name='name']" and @position="after"]""",
            expr="//tree[1]/field[@name='display_name']",
        ),
    ],
    "studio_customization.odoo_studio_project__498db5ec-35d3-42f3-8a7e-a2d26fb8b7b4": [
        RemoveFields(
            [
                "x_studio_marge_complementaire",
                "x_studio_marge_consolidee",
                "x_studio_marge_reelle",
                "x_studio_montant_des_achats",
                "x_studio_purchase_lines_ids",
                "non_allow_billable",
                "subtask_project_id",
            ]
        ),
        RemoveElements("""//xpath[@expr="/form[1]/sheet[1]/notebook[1]/page[5]/group[1]" and @position='after']"""),
        RemoveElements("""//xpath[@expr="/form[1]/sheet[1]/group[1]/group[2]/field[3]" and @position='attributes']"""),
        RemoveElements(
            """//xpath[@expr="//field[@name='x_studio_sales_ids']/tree//field[@name='company_id']" and @position='attributes']"""
        ),
        RemoveElements(
            """//xpath[@expr="/form[1]/sheet[1]/group[1]/group[2]/field[2]" and @position='after' and not(*)]"""
        ),
        RemoveElements(
            """//xpath[@expr="/form[1]/sheet[1]/group[1]/group[2]/field[2]" and \
            @position='attributes'][attribute[@name='attrs' and .='{"invisible": [["x_studio_marge_reelle","=",0]]}']]"""
        ),
        RemoveElements(
            """//xpath[@expr="/form[1]/sheet[1]/notebook[1]/page[8]/group[1]/group[1]/field[1]" and @position='attributes']"""
        ),
        RemoveElements(
            """//xpath[@expr="/form[1]/sheet[1]/notebook[1]/page[8]/group[1]/group[1]/field[1]" and @position='before']"""
        ),
        RemoveElements(
            """//xpath[@expr="/form[1]/sheet[1]/notebook[1]/page[8]/group[1]/group[1]/field[2]" and @position='replace']"""
        ),
        RemoveElements(
            """//xpath[@expr="/form[1]/sheet[1]/notebook[1]/page[8]/group[1]/group[1]/field[1]" and @position='after']"""
        ),
        RemoveElements(
            """//xpath[@expr="//field[@name='x_studio_doublon_ids']/tree//field[@name='x_studio_montant_des_ventes']" and \
            @position='after']"""
        ),
        RemoveElements(
            """//xpath[@expr="/form[1]/sheet[1]/notebook[1]/page[8]/group[1]/group[1]" and @position='inside']"""
        ),
        RemoveElements(
            """//xpath[@expr="/form[1]/sheet[1]/notebook[1]/page[8]/group[1]/group[1]/field[2]" and @position='attributes']"""
        ),
        RemoveElements(
            """//xpath[@expr="//field[@name='x_studio_doublon_ids']/tree//field[@name='x_studio_montant_des_heures_bis']" and \
            @position='after']"""
        ),
        RemoveElements(
            """//xpath[@expr="//field[@name='x_studio_doublon_ids']/tree//field[@name='x_studio_montant_des_heures_bis']" and \
            @position='replace']"""
        ),
        RemoveElements(
            """//xpath[@expr="//field[@name='x_studio_doublon_ids']/tree//field[@name='x_studio_marge_reelle']" and \
            @position='replace']"""
        ),
        AddElements(
            """//data""",
            """
            <xpath expr="//form[@class='o_form_project_project']//header">
              <field name="privacy_visibility" invisible="1"/>
            </xpath>
            """,
            "inside",
        ),
        RemoveElements(
            """//xpath[@expr="//field[@name='x_studio_doublon_ids']/tree//field[@name='x_studio_montant_des_achats']" and \
            @position='after']"""
        ),
        RemoveElements("""//xpath[@expr="//field[@name='x_studio_purchase_lines_ids']" and @position='inside']"""),
        RemoveElements(
            """//xpath[@expr="//field[@name='x_studio_purchase_lines_ids']/tree//field[@name='name']" and @position='replace']"""
        ),
        RemoveElements(
            """//xpath[@expr="//field[@name='x_studio_purchase_lines_ids']/tree//field[@name='product_uom']" and \
            @position='replace']"""
        ),
        RemoveElements(
            """//xpath[@expr="//field[@name='x_studio_purchase_lines_ids']/tree//field[@name='product_id']" and \
            @position='attributes']"""
        ),
        RemoveElements(
            """//xpath[@expr="//field[@name='x_studio_purchase_lines_ids']/tree//field[@name='partner_id']" and \
            @position='after']"""
        ),
        RemoveElements(
            """//xpath[@expr="//field[@name='x_studio_purchase_lines_ids']/tree//field[@name='price_subtotal']" and \
            @position='attributes']"""
        ),
        RemoveElements(
            """//xpath[@expr="//field[@name='x_studio_purchase_lines_ids']/tree//field[@name='order_id']" and @position='after']"""
        ),
        RemoveElements(
            """//xpath[@expr="//form[1]/sheet[1]/div[not(@name)][1]/div[@name='options_active']/div[1]/label[1]"]"""
        ),
        UpdateAttributes(
            """//xpath[@expr="//page[@name='description_page']" and @position='attributes']""",
            expr="//page[@name='description']",
        ),
        UpdateAttributes(
            """//xpath[@expr="//button[@name='action_view_so']" and @position='after']""",
            expr="//button[@name='871']",
            position="after",
        ),
        UpdateAttributes(
            """//xpath[@expr="//button[@name='154']" and @position='after']""",
            expr="//button[@name='870']",
        ),
        RemoveElements(
            """//xpath[@expr="/form[1]/sheet[1]/notebook[1]/page[8]" and @position='attributes'][attribute[@name='attrs' and \
            .='{"invisible": [["x_studio_marge_complementaire","=",0]]}']]"""
        ),
        RemoveElements("""//xpath[@expr="//button[@name='154']" and @position='replace']"""),
        RemoveElements(
            """//xpath[@expr="/form[1]/sheet[1]/notebook[1]/page[2]/group[1]/group[1]/field[4]" and @position="after"]""",
        ),
        RemoveElements(
            """//xpath[@expr="/form[1]/sheet[1]/notebook[1]/page[2]/group[1]/group[1]/field[5]" and @position="after"]""",
        ),
        UpdateAttributes(
            """//xpath[@expr="//field[@name='task_ids']/tree//field[@name='user_id']" and @position="attributes"]""",
            expr="//field[@name='task_ids']/tree//field[@name='user_ids']",
        ),
        RemoveElements(
            """//xpath[@expr="/form[1]/sheet[1]/notebook[1]/page[5]/field[1]" and @position='attributes']"""
        ),
        UpdateAttributes(
            """//xpath[@expr="/form[1]/sheet[1]/notebook[1]/page[2]/group[1]/group[1]/field[6]" and @position="attributes"]""",
            expr="/form[1]/sheet[1]/notebook[1]/page[2]/group[1]/group[1]/field[4]",
        ),
        ReplaceValue("account_analytic_id", "analytic_distribution"),
        UpdateAttributes("""//xpath[@expr="//field[@name='task_ids']"]//field[@name='user_id']""", name="user_ids"),
        add_invisible_sibling("company_id", "after", path="//tree[@string='Tasks']"),
        add_invisible_sibling("progress", "after", path="//tree[@string='Tasks']"),
        AddElements(
            """//xpath[@expr="//field[@name='x_studio_sales_ids']" and @position='inside']/tree/field[@name='company_id' \
            and @groups='base.group_multi_company' and @optional='show' and @readonly='1']""",
            '<field name="company_id" invisible="1"/>',
            position="after",
        ),
        AddElements(
            """//xpath[@expr="//field[@name='x_studio_doublon_ids']" and @position='inside']/tree/field[@name='label_tasks' and \
            @optional='hide']""",
            '<field name="company_id" invisible="1"/>',
            position="after",
        ),
        RemoveElements(
            """//xpath[@expr="//form[1]/sheet[1]" and @position='after']""",
        ),
        AddElements(
            """//data""",
            """
            <xpath expr="//field[@name='allocated_hours']" position="after">
              <field name="allow_timesheets" invisible="1"/>
              <field name="allow_billable" invisible="1"/>
            </xpath>
            """,
            "inside",
        ),
        RemoveElements("""//xpath[@expr="/form[1]/sheet[1]/notebook[1]/page[5]" and @position='attributes']"""),
        RemoveElements("""//xpath[@expr="/form[1]/sheet[1]/notebook[1]/page[7]" and @position='attributes']"""),
        AddElements(
            """//data""",
            """
            <xpath expr="//page[@name='studio_page_Srb78']" position="replace"/>
            """,
            "inside",
        ),
        RemoveElements(
            """//xpath[@expr="/form[1]/sheet[1]/notebook[1]/page[2]/group[1]/group[1]/field[4]" and @position='attributes']"""
        ),
    ],
    "studio_customization.odoo_studio_purchase_83c390a4-3e2b-4458-9076-19cb4bcde6ad": [
        RemoveElements("""//xpath[@expr="//field[@name='partner_ref']" and @position='after']""")
    ],
    "studio_customization.odoo_studio_purchase_b0d8752e-320a-4aab-bd89-9238856ed92e": [
        RemoveElements("""//xpath[@expr="//field[@name='order_id']"]/field[@name='x_studio_compte_analytique']"""),
        ReplaceValue("account_analytic_id", "analytic_distribution"),
    ],
    "studio_customization.odoo_studio_crm_lead_c3f946f5-6549-49dc-a1cd-84c1c366d22e": [
        AddElements(
            """//xpath[@expr="//field[@name='team_id']"]""", """<field name="team_id" invisible="1"/>""", "inside"
        ),
        RemoveElements("""//xpath[@expr="//field[@name='team_id']"]//field[@name='activity_type_id']"""),
    ],
    "studio_customization.odoo_studio_stock_mo_2ccc7511-388e-437d-9f30-dcfb3bd8bd80": [
        AddElements(
            """//xpath[@expr="//field[@name='company_id']"]""",
            """
            <field name='company_id' invisible="1"/>
            <field name="product_uom_category_id"/>
            """,
            "inside",
        ),
    ],
    "studio_customization.odoo_studio_purchase_dc691821-ae7b-4cc5-bf10-ceadce8a116b": [
        RemoveElements("""//xpath[@expr="//filter[@name='groupby_supplier']"]/filter[@name='studio_group_by_15c6Y']"""),
        RemoveElements("""//xpath[@expr="//field[@name='order_id']"]/field[@name='x_studio_compte_analytique']"""),
    ],
    "studio_customization.odoo_studio_purchase_a7c4d792-8292-4554-acc6-5fe24214bf75": [
        RemoveElements("""//xpath[@expr="//field[@name='partner_id']" and @position='after']"""),
        RemoveElements("""//xpath[@expr="//tree[1]/field[@name='name']" and @position='after']"""),
    ],
    "studio_customization.odoo_studio_hr_emplo_b33da50b-0402-4fb7-92c1-2bc1e6afb405": [
        ReplaceValue("timesheet_cost", "hourly_cost")
    ],
    "studio_customization.odoo_studio_hr_emplo_7db2d8f7-6a90-49f4-ac7f-bc59ef102961": [
        ReplaceValue("timesheet_cost", "hourly_cost")
    ],
    "studio_customization.odoo_studio_product__2c94e633-817f-434a-8db8-d5d64d6f6380": [
        ReplaceValue("partner_id", "name"),
        RemoveElements("""//xpath[@expr="//field[@name='seller_ids']"]//field[@name='name']"""),
        AddElements(
            """//xpath[@expr="//field[@name='seller_ids']"]//field[@name='sequence']""",
            """<field name="partner_id" readonly="0"/>""",
            "after",
        ),
        add_invisible_sibling("company_id", "after", path="//tree[@string='Vendor Information']"),
    ],
    "studio_customization.odoo_studio_crm_lead_07a764d6-0abb-483e-bed1-50261965e455": [
        ReplaceValue("lost_reason", "lost_reason_id")
    ],
    "studio_customization.odoo_studio_stock_pi_86039416-7310-458f-a486-8b6a735c66ca": [
        ReplaceValue("product_uom_qty", "reserved_uom_qty"),
        AddElements(
            """//xpath[@expr="//field[@name='move_line_ids_without_package']"]//field[@name='result_package_id']""",
            """<field name='result_package_id' invisible="1"/>""",
            "after",
        ),
        AddElements(
            """//xpath[@expr="//field[@name='move_line_ids_without_package']"]//field[@name='location_id']""",
            """<field name='location_id' invisible="1"/>""",
            "after",
        ),
        AddElements(
            """//xpath[@expr="//field[@name='move_line_ids_without_package']"]//field[@name='location_dest_id']""",
            """<field name='location_dest_id' invisible="1"/>""",
            "after",
        ),
        AddElements(
            """//xpath[@expr="//field[@name='move_line_ids_without_package']"]//field[@name='package_id']""",
            """<field name='package_id' invisible="1"/>""",
            "after",
        ),
        RemoveElements(
            """//xpath[@expr="//form[1]/sheet[1]/group[1]/group[2]/field[@name='owner_id']" and @position='after']"""
        ),
    ],
    "studio_customization.odoo_studio_crm_lead_ab884308-7211-4dbd-a725-c8a563d014c8": [
        RemoveElements("""//xpath[@expr="/form[1]/sheet[1]/group[1]/group[5]/field[3]"]"""),
        RemoveElements("""//xpath[@expr="/form[1]/sheet[1]/group[1]/group[5]/field[4]"]"""),
        RemoveElements("""//xpath[@expr="//group[@name='opportunity_info']" and @position='attributes']"""),
        RemoveElements(
            """//xpath[@expr="//form[1]/sheet[1]/group[1]/group[not(@name)][1]/field[@name='tag_ids']" and @position='after']"""
        ),
    ],
    "studio_customization.odoo_studio_purchase_65477693-0dc4-43f8-91d4-30bf520b3ea2": [
        RemoveElements("""//xpath[@expr="//field[@name='company_id']" and @position='replace']"""),
        RemoveElements("""//xpath[@expr="//tree[1]/field[@name='name']"]//field[@name='x_studio_dossier']"""),
        RemoveElements("""//xpath[@expr="//tree[1]/field[@name='name']"]//field[@name='x_studio_projet']"""),
    ],
    "studio_customization.odoo_studio_stock_pi_23425e3f-63b9-4da2-96fe-510b82b341a7": [
        RemoveElements("""//xpath[@expr="//tree[1]/field[@name='name']" and @position='after']"""),
    ],
    "studio_customization.odoo_studio_analytic_cc3e03f5-4fd3-490f-a393-2a7ceb94b4be": [
        RemoveElements("""//xpath[@expr="//field[@name='partner_id']" and @position='after']"""),
    ],
    "studio_customization.odoo_studio_sale_ord_afe808d4-86b2-4af9-95f4-23f64ad87726": [
        RemoveElements("""//xpath[@expr="//search[1]/field[@name='name']" and @position='before']"""),
        RemoveElements("""//xpath[@expr="//filter[@name='order_month']" and @position='after']"""),
    ],
    "studio_customization.odoo_studio_sale_ord_a8511b26-f83d-47d7-8942-0e286846f261": [
        RemoveElements("""//xpath[@expr="//tree[1]/field[@name='name']" and @position='after']"""),
    ],
    "studio_customization.odoo_studio_sale_ord_6cb82c6e-eeae-4811-bcb4-d0bbe9afa69e": [
        RemoveElements("""//xpath[@expr="//field[@name='date_order'][2]"]//field[@name='x_studio_projet']"""),
    ],
    "studio_customization.odoo_studio_sale_ord_9b1196b5-aab9-41f4-a169-3a0847b56eaa": [
        RemoveElements("""//xpath[@expr="//tree[1]/field[@name='name']" and @position='after']""")
    ],
    "studio_customization.odoo_studio_account__c8293bfc-b7b3-40e5-9b2c-88e41e98e388": [
        RemoveElements("""//xpath[@expr="//filter[@name='groupby_project']" and @position='after']""")
    ],
    "studio_customization.odoo_studio_report_p_b0ec6e1d-6549-4a78-ac9d-d2e96034eac8": [
        RemoveElements("""//xpath[@expr="/t/t/div/div[3]/div/span[1]" and @position='after']"""),
        RemoveElements("""//xpath[@expr="/t[1]/t[1]/div[1]/div[3]/div[1]/span[2]" and @position="attributes"]"""),
        RemoveElements("""//xpath[@expr="/t[1]/t[1]/div[1]/div[2]/div[3]/p[1]" and @position='attributes']"""),
        RemoveElements("""//xpath[@expr="/t/t/div/div[2]/div[2]/strong" and @position='replace']"""),
        RemoveElements("""//xpath[@expr="/t[1]/t[1]/div[1]/h2[3]/span[1]" and @position='attributes']"""),
        RemoveElements("""//xpath[@expr="/t/t/div/h2[3]/span" and @position='before']"""),
        RemoveElements("""//xpath[@expr="/t/t/div/h2[3]/span[1]" and @position='replace']"""),
        RemoveElements("""//xpath[@expr="/t[1]/t[1]/div[1]/h2[3]/span[2]" and @position='replace']"""),
        RemoveElements("""//xpath[@expr="/t[1]/t[1]/div[1]/h2[3]" and @position='replace']"""),
        RemoveElements("""//xpath[@expr="/t/t/div/div[7]/div/span" and @position='replace']"""),
        RemoveElements("""//xpath[@expr="/t[1]/t[1]/div[1]/div[5]/div[2]" and @position='replace']"""),
        RemoveElements("""//xpath[@expr="/t/t/div/div[3]/div/span[3]" and @position='replace']"""),
        RemoveElements("""//xpath[@expr="/t[1]/t[1]/div[1]/div[3]/div[1]/span[4]" and @position='attributes']"""),
        RemoveElements("""//xpath[@expr="/t[1]/t[1]/div[1]/div[6]/div[1]" and @position='replace']"""),
        AddElements("""//data""", """<xpath expr="/t[1]/t[1]/div[1]/div[8]/div[1]" position="replace"/>""", "inside"),
        AddElements(
            """//data""",
            """"<xpath expr="/t[1]/t[1]/div[1]/div[3]/div[1]/span[1]" position="replace"/>""",
            """inside""",
        ),
    ],
    "arch_survey.survey_survey_question_form_inherit": [],
}


def migrate(cr, version):
    field_user_ids = util.ref(cr, "project.field_project_task__user_ids")
    cr.execute(
        """
        UPDATE ir_server_object_lines L
           SET value = 'record.user_id.ids'
         WHERE col1 = %s;
        """,
        (field_user_ids,),
    )
    _logger.info("##### Fix disabled studio views #####")
    edit_views(cr, VIEW_OPERATIONS)
    activate_views(cr, xmlids=VIEW_OPERATIONS.keys())
    _logger.info("##### --------- Remove custom studio views -------- #####")
    remove_fields_from_models(cr)
    util.remove_view(cr, "studio_customization.odoo_studio_purchase_a3a18c2d-04da-4e25-a25d-62e35295a48d")
    util.remove_view(cr, "studio_customization.odoo_studio_request__d9f96d4e-46b3-4588-a445-79a41cee40ef")
    util.remove_view(cr, "studio_customization.odoo_studio_account__f2612280-bad7-4b18-bb1b-39538923586b")
    util.remove_view(cr, "studio_customization.odoo_studio_account__dc02227f-7014-4cbf-957f-ca2e6366e079")
    with util.edit_view(cr, "studio_customization.odoo_studio_crm_lead_07a764d6-0abb-483e-bed1-50261965e455") as arch:
        node = arch.xpath("""//xpath[@expr="//field[@name='activity_date_deadline_my']" and @position='attributes']""")[
            0
        ]
        node.getparent().remove(node)

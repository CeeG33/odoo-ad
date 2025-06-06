from odoo.upgrade.custom_util import AddElements, RemoveElements, UpdateAttributes, activate_views, edit_views


VIEW_OPERATIONS = {
    # Odoo Studio: crm.lead.kanban.lead customization
    "studio_customization.odoo_studio_crm_lead_7bbdc80c-075f-4db1-95c1-27ea8d383600": [
        UpdateAttributes(
            """//xpath[@expr="//kanban[1]/templates[1]/t[1]/div[1]/div[4]/div[1]/div[2]/field[@name='user_id']"]""",
            expr="//kanban[1]/templates[1]/t[2]/div[1]/div[3]/div[1]/div[2]/field[@name='user_id']",
        )
    ],
    # Odoo Studio: res.partner.form customization
    "studio_customization.odoo_studio_res_part_5ce89687-0a69-4ca5-8478-8e3783a21b93": [
        UpdateAttributes("""//xpath[@expr="/form[1]/div[5]"]""", expr="/form[1]//div[hasclass('oe_chatter')]")
    ],
    # Odoo Studio: project.task.form customization
    "studio_customization.odoo_studio_project__e8c9303c-7541-4c53-9d74-bc556c97d2d2": [
        UpdateAttributes(
            """//xpath[@expr="//form[1]/sheet[1]/notebook[1]/page[not(@name)][1]/field[@name='timesheet_ids']/tree[1]/field[@name='task_id']"]""",
            expr="//form[1]/sheet[1]/notebook[1]//field[@name='timesheet_ids']/tree[1]/field[@name='task_id']",
        )
    ],
    # Odoo Studio: res.partner.tree customization
    "studio_customization.odoo_studio_res_part_0d769669-e7de-4879-8c56-01f613608b53": [
        UpdateAttributes("""//field[@name='translated_display_name']""", name="complete_name")
    ],
    # Odoo Studio: crm.lead.form customization
    "studio_customization.odoo_studio_crm_lead_dcb69db9-3ade-4e90-8d1f-f5ff50da902a": [
        UpdateAttributes("""//field[@name="x_studio_lkn_account"]""", options=None),
        UpdateAttributes(
            """//xpath[@expr="/form[1]/sheet[1]/div[2]/h2[1]/div[4]"]""",
            expr="/form[1]/sheet[1]/div[2]/h2[1]//div[@id='probability']/..",
        ),
    ],
    # Odoo Studio: project.project.form customization
    "studio_customization.odoo_studio_project__98e9e8c9-9295-4a21-a1fe-4983d851f07a": [
        UpdateAttributes("//field[@name='is_closed']", name="state"),
        UpdateAttributes("//field[@name='date_deadline']", invisible="state == '1_done' or state == '1_canceled'"),
        RemoveElements("//field[@name='allow_subtasks']"),
        UpdateAttributes("//field[@name='subtask_effective_hours']", invisible=None),
        UpdateAttributes("//field[@name='total_hours_spent']", invisible=None),
        UpdateAttributes("//field[@name='planned_hours']", name="allocated_hours"),
        UpdateAttributes("//field[@name='kanban_state']", name="state"),
        AddElements(
            """//xpath[@expr="//page[@name='settings']"][@position="move"]""",
            """<field name="sale_line_id" invisible="1"/>""",
            position="before",
        ),
        UpdateAttributes("//field[@name='parent_id'][@groups='project.group_subtask_project']", groups=None),
    ],
    # Odoo Studio: project.project.select customization
    "studio_customization.odoo_studio_project__06985751-a03c-4663-95c9-bb346bfbb664": [
        UpdateAttributes("""//xpath[@expr="//filter[@name='Partner']"]""", expr="//filter[@name='company']")
    ],
    # Odoo Studio: project.project.tree customization
    "studio_customization.odoo_studio_project__c0ea6d5e-1da7-4b39-9682-84189e1852c5": [
        RemoveElements("""//xpath[@expr="//field[@name='analytic_account_id']"]"""),
        AddElements(
            """//xpath[@expr="//field[@name='date_start']"][@position='move']""",
            """<field name="analytic_account_id" optional="hide" can_create="true" can_write="true"/>""",
            position="before",
        ),
        AddElements(
            """//xpath[@expr="/tree[1]/field[1]"]""",
            """<xpath expr="//field[@name='create_date']" position="replace"/>""",
            position="before",
        ),
        RemoveElements("""//xpath[@expr="/tree[1]/field[1]"]/xpath[1]"""),
        AddElements(
            """//xpath[@expr="/tree[1]/field[1]"]""",
            """<field name="create_date" widget="date" optional="hide"/>""",
            position="inside",
        ),
        UpdateAttributes(
            """//xpath[@expr="//field[@name='privacy_visibility']"]""", expr="//field[@name='partner_id']"
        ),
    ],
    # Odoo Studio: res.company.form customization
    "studio_customization.odoo_studio_res_comp_620a9f8f-e242-4829-867f-9af2f2ce43e0": [
        UpdateAttributes("""//xpath[@expr="//field[@name='favicon']"]""", expr="//field[@name='color']")
    ],
    # Odoo Studio: utm.source.view.tree customization
    "studio_customization.odoo_studio_utm_sour_e6ad7387-03c2-4907-8519-66fb19e06fbd": [
        RemoveElements("""//field[@name="__last_update"]""")
    ],
    # Odoo Studio: stock.picking.form customization
    "studio_customization.odoo_studio_stock_pi_86039416-7310-458f-a486-8b6a735c66ca": [
        RemoveElements("""//field[@name="is_initial_demand_editable"]"""),
        UpdateAttributes(
            """//xpath[@expr="//field[@name='move_line_ids_without_package']"]/tree[1]""",
            {"decoration-danger": None, "decoration-success": None},
        ),
        UpdateAttributes(
            """//field[@name="reserved_uom_qty"]""",
            name="quantity",
            column_invisible="parent.picking_type_code == 'incoming'",
        ),
        RemoveElements("""//field[@name="qty_done"]"""),
        AddElements(
            """//xpath[@expr="//field[@name='move_line_ids_without_package']"]""",
            """
                        <xpath expr="//page[@name='operations']" position="before">
                                <page string="Detailed Operations" name="detailed_operations" invisible="not show_operations">
                                    <field name="show_reserved" invisible="1"/>
                                    <field name="show_operations" invisible="1"/>
                                    <field name="move_line_ids_without_package"
                                        readonly="(not show_operations or state == 'cancel') or (state == 'done' and is_locked)"
                                        invisible="not show_reserved"
                                        context="{'tree_view_ref': 'stock.view_stock_move_line_detailed_operation_tree', 'default_picking_id': id, 'default_location_id': location_id, 'default_location_dest_id': location_dest_id, 'default_company_id': company_id}"/>
                                    <field name="package_level_ids_details"
                                        readonly="state == 'done'" invisible="not picking_type_entire_packs or not show_operations"
                                        context="{'default_location_id': location_id, 'default_location_dest_id': location_dest_id, 'default_company_id': company_id}" />
                                    <button class="oe_highlight" name="action_put_in_pack" type="object" string="Put in Pack" invisible="state in ['draft', 'done', 'cancel']" groups="stock.group_tracking_lot" data-hotkey="shift+g"/>
                                </page>
                        </xpath>
                    """,
            position="before",
        ),
    ],
}


def migrate(cr, version):
    edit_views(cr, VIEW_OPERATIONS)
    activate_views(
        cr,
        xmlids=[
            # Odoo Studio: crm.lead.tree.opportunity customization
            "studio_customization.odoo_studio_crm_lead_07a764d6-0abb-483e-bed1-50261965e455",
            # Odoo Studio: crm.lead.tree.lead customization
            "studio_customization.odoo_studio_crm_lead_8ab58024-0c4d-48e4-888a-51cdfdf08dca",
        ],
    )

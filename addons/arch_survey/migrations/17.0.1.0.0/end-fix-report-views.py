from odoo.upgrade.custom_util import AddElements, RemoveElements, UpdateAttributes, edit_views


VIEW_OPERATIONS = {
    # Odoo Studio: report_invoice_document customization
    "studio_customization.odoo_studio_report_i_cf8e593c-886d-4a92-8fef-9820661e8393": [
        UpdateAttributes(
            """//xpath[@expr="/t[1]/t[1]/div[2]/div[1]/div[1]/div[4]"]""", expr="//div[@name='customer_code']"
        ),
        UpdateAttributes(
            """//xpath[@expr="/t/t/div[2]/div/div[3]"]""", expr="//div[@name='comment']", position="before"
        ),
        UpdateAttributes(
            """//xpath[@expr="/t[1]/t[1]/div[2]/div[1]/table[1]/tbody[1]/t[3]/tr[1]/t[1]/td[6]"]""",
            expr="//table[@name='invoice_line_table']/tbody[1]/t[@t-foreach='lines']/tr[1]/t[1]/td[6]",
        ),
        UpdateAttributes(
            """//xpath[@expr="/t[1]/t[1]/div[2]/div[1]/table[1]/thead[1]/tr[1]/th[6]"]""",
            expr="//table[@name='invoice_line_table']/thead[1]/tr[1]/th[6]",
        ),
        AddElements(
            """//data""",
            """
                    <xpath expr="//div[@id='informations']//span[@t-field='o.invoice_date']" position="replace">
                        <p t-field="o.invoice_date">2023-09-12</p>
                    </xpath>

                    <xpath expr="//div[@id='informations']//span[@t-field='o.invoice_date_due']" position="replace">
                        <p t-field="o.invoice_date_due">2023-10-31</p>
                    </xpath>

                    <xpath expr="//div[@id='informations']//span[@t-field='o.delivery_date']" position="replace">
                        <p t-field="o.delivery_date">2023-09-25</p>
                    </xpath>

                    <xpath expr="//div[@id='informations']//span[@t-field='o.invoice_origin']" position="replace">
                        <p t-field="o.invoice_origin">SO123</p>
                    </xpath>

                    <xpath expr="//div[@id='informations']//span[@t-field='o.ref']" position="replace">
                        <p t-field="o.ref">INV/2023/00001</p>
                    </xpath>
        """,
            position="inside",
        ),
    ],
    # Odoo Studio: report_saleorder_document customization
    "studio_customization.odoo_studio_report_s_5b537e1c-4ad4-47bc-bcb9-d24731cc81a4": [
        RemoveElements("""//xpath[@expr="/t[1]/t[1]/div[1]/div[3]/div[2]/p[1]"]"""),
        RemoveElements("""//xpath[@expr="/t/t/div/table/thead/tr/th[5]/span[1]"]"""),
        AddElements(
            """//data""",
            """
                    <xpath expr="//div[@id='informations']//span[@t-field='doc.client_order_ref']" position="replace">
                        <p class="m-0" t-field="doc.client_order_ref">SO0000</p>
                    </xpath>

                    <xpath expr="//div[@id='informations']//span[@t-field='doc.user_id']" position="replace">
                        <p class="m-0" t-field="doc.user_id">Mitchell Admin</p>
                    </xpath>
            """,
            position="inside",
        ),
    ],
}


def migrate(cr, version):
    edit_views(cr, VIEW_OPERATIONS)

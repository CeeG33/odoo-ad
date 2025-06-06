from odoo.upgrade.custom_util import AddElements, RemoveElements, edit_views


VIEW_OPERATIONS = {
    # Odoo Studio: sale.order.tree customization
    "studio_customization.odoo_studio_sale_ord_a8511b26-f83d-47d7-8942-0e286846f261": [
        RemoveElements("""//field[@name="margin"]"""),
        RemoveElements("""//field[@name="margin_percent"]"""),
        AddElements(
            """//data""",
            """
                    <xpath expr="//field[@name='margin']" position="attributes">
                        <attribute name="string">Marge prévue</attribute>
                        <attribute name="optional">hide</attribute>
                    </xpath>
                    <xpath expr="//field[@name='margin_percent']" position="attributes">
                        <attribute name="string">Marge prévue (%)</attribute>
                        <attribute name="optional">hide</attribute>
                        <attribute name="widget">percentage</attribute>
                    </xpath>
                    """,
        ),
    ]
}


def migrate(cr, version):
    edit_views(cr, VIEW_OPERATIONS)

from odoo.upgrade import util


def migrate(cr, version):
    env = util.env(cr)

    # Création écritures analytiques
    server_action = env.ref("studio_customization.creation_ecritures_a_88a5040c-91f6-497e-aeeb-6c99edb5cef1")
    server_action.code = server_action.code.replace("qty_done", "quantity")

    # Création écritures analytiques
    server_action = env.ref("studio_customization.creation_ecritures_a_03b0e4d6-1116-4002-885a-6f631c436870")
    server_action.code = server_action.code.replace("qty_done", "quantity")

    # Modification de l'alias sur changement du nom du projet
    # Was on_update
    ref = env.ref("studio_customization.creation_de_la_refer_c02e9f71-62b8-4081-9f09-5967f54ce995")
    ref.trigger = "on_create_or_write"
    # restrict filter to avoid the action getting triggered on on_update
    ref.filter_pre_domain = """[["name", "=", False]]"""
    ref.filter_domain = """["&", ("partner_id", "!=", False), ("company_id", "!=", False)]"""
    ref.action_unarchive()

    # Valeur du score
    # Was on_update
    ref = env.ref("studio_customization.valeur_du_score_f36eaea2-a3fa-4545-8fd3-6e98b76e7df4")
    ref.trigger = "on_create_or_write"
    ref.action_unarchive()

    # Contract date
    # Was on_update
    ref = env.ref("studio_customization.contract_date_fe053878-0e1c-4d51-9641-dfad422aef63")
    ref.trigger = "on_create_or_write"
    # restrict filter to avoid the action getting triggered on on_create
    ref.filter_pre_domain = """[]"""
    ref.filter_domain = """[("x_studio_handover_date","!=",False)]"""
    ref.action_unarchive()

    # Mise à jour du repas
    # Was on_create
    ref = env.ref("studio_customization.mise_a_jour_du_repas_9dabec27-9b01-4a46-b796-7cea035a37b1")
    ref.trigger = "on_create_or_write"
    # restrict filter to avoid the action getting triggered on on_update
    ref.filter_pre_domain = """[["x_name", "=", False]]"""
    ref.filter_domain = """[["x_studio_user_id","=",False]]"""
    ref.action_unarchive()

    # Création des tâches
    # Was on_create
    ref = env.ref("studio_customization.creation_de_tache_av_c4c9b033-7f4e-492d-aa9e-2d9d86b6f85c")
    ref.trigger = "on_create_or_write"
    # restrict filter to avoid the action getting triggered on on_update
    ref.filter_pre_domain = """[("name", "=", "")]"""
    ref.filter_domain = """[["partner_id","!=",False]]"""
    child_ids = ref.action_server_ids.child_ids
    child_ids[0].code = child_ids[0].code.replace("env['ir.attachment'].browse(5630)", "5630")
    child_ids[1].code = child_ids[1].code.replace("env['ir.attachment'].browse(5632)", "5632")
    child_ids[2].code = child_ids[2].code.replace("env['ir.attachment'].browse(5631)", "5631")
    child_ids[3].code = child_ids[3].code.replace("env['ir.attachment'].browse(5634)", "5634")
    child_ids[4].code = child_ids[4].code.replace("env['ir.attachment'].browse(5633)", "5633")

    ref.action_unarchive()

    # Création de la référence projet
    # Was on_create
    ref = env.ref("studio_customization.donner_nom_au_projet_15d784a6-53e5-4064-ae2d-7f655c90946a")
    ref.trigger = "on_create_or_write"
    # restrict filter to avoid the action getting triggered on on_update
    ref.filter_pre_domain = """[["name", "=", False]]"""
    ref.filter_domain = """["&", ["partner_id","!=",False], ["x_studio_abrege", "!=", False]]"""
    # In v17 company_id for a project is no longer a required field, we add this to make sure the server action doesn't fail
    ref.action_server_ids.code = ref.action_server_ids.code.replace(
        "record.company_id.name[:1]", "(record.company_id.name[:1] if record.company_id else '')"
    )
    ref.action_unarchive()

    # Relier message à compte
    # Was on_create
    ref = env.ref("studio_customization.relier_message_a_com_46ec381b-7cf1-4cd9-a341-785f927398e3")
    ref.trigger = "on_create_or_write"
    ref.trigger_field_ids = env.ref("mail.field_mail_message__res_id")
    # restrict filter to avoid the action getting triggered on on_update
    ref.filter_pre_domain = """[["message_type", "=", False]]"""
    ref.filter_domain = """["&", ("model", "=", "res.partner"), ("res_id", "!=", False)]"""
    ref.action_unarchive()

    # Relier message à l'opportunité
    # Was on_create
    ref = env.ref("studio_customization.relier_message_a_l_o_7e2304b6-05f5-4e1c-9d9c-980686a16252")
    ref.trigger = "on_create_or_write"
    # restrict filter to avoid the action getting triggered on on_update
    ref.filter_pre_domain = """[["message_type", "=", False]]"""
    ref.filter_domain = """["&", ("model", "=", "crm.lead"), ("res_id", "!=", False)]"""
    ref.action_unarchive()

    # Stage update for leads
    # Was on_create
    ref = env.ref("studio_customization.stage_update_341817ad-642b-470b-9d54-9a2724025ed8")
    ref.trigger = "on_create_or_write"
    # restrict filter to avoid the action getting triggered on on_update
    ref.filter_pre_domain = """[["name", "=", False]]"""
    ref.action_unarchive()

    # Relier activité à l'opportunité
    # Was on_create
    ref = env.ref("studio_customization.relier_activite_a_l__9bcc7ae3-1ffa-4ba0-bc68-41fb7f6575ad")
    ref.trigger = "on_create_or_write"
    # restrict filter to avoid the action getting triggered on on_update
    ref.filter_pre_domain = """[["res_model_id", "=", False]]"""
    ref.filter_domain = """["&", ("res_model", "=", "crm.lead"), ("res_id", "!=", False)]"""
    ref.action_unarchive()

    # Changement du descriptif
    # Was on_update
    ref = env.ref("studio_customization.changement_du_descri_b0f3ba2c-7bc6-477f-b624-99f10f7bf1bb")
    ref.trigger = "on_create_or_write"
    # restrict filter to avoid the action getting triggered on on_create
    ref.filter_pre_domain = """[["name", "!=", False]]"""

    # Changement du descriptif sous-projet
    # Was on_update
    ref = env.ref("studio_customization.changement_du_descri_ac120f9d-ea35-47b8-a706-029d4cbe779d")
    ref.trigger = "on_create_or_write"
    # restrict filter to avoid the action getting triggered on on_create
    ref.filter_pre_domain = """[["name", "!=", False]]"""

    # Relier activité à compte
    # Was on_create
    ref = env.ref("studio_customization.relier_activite_a_co_cfd2da6d-5285-4247-95b7-356a175cf1ac")
    ref.trigger = "on_create_or_write"
    # restrict filter to avoid the action getting triggered on on_update
    ref.filter_pre_domain = """[["res_model_id", "=", False]]"""
    ref.filter_domain = """["&", ("res_model", "=", "res.partner"), ("res_id", "!=", False)]"""
    ref.action_unarchive()

    # Création du projet sur ARCH.DESIGN
    # Was on_create
    ref = env.ref("studio_customization.creation_du_projet_s_cb75f38f-6d0b-424e-b4bf-ccef45ada5fe")
    ref.trigger = "on_create_or_write"
    # restrict filter to avoid the action getting triggered on on_update
    ref.filter_pre_domain = """[["name", "=", False]]"""
    ref.filter_domain = (
        """["&","&",["x_studio_projet_doublon","=",False],["company_id","=","ORANGELO"],["partner_id","!=",False]]"""
    )

    # Création du projet sur ORANGELO
    # Was on_create
    ref = env.ref("studio_customization.creation_du_projet_s_250fef91-aaf3-4ca0-9bcb-942c4aca0336")
    ref.trigger = "on_create_or_write"
    # restrict filter to avoid the action getting triggered on on_update
    ref.filter_pre_domain = """[["name", "=", False]]"""
    ref.filter_domain = (
        """["&","&",["x_studio_projet_doublon","=",False],["company_id","=","ARCH.DESIGN"],["partner_id","!=",False]]"""
    )

    # Création de la référence projet sur doublon
    # Was on_create
    ref = env.ref("studio_customization.creation_de_la_refer_65ab248d-ab5e-4009-8976-85c9bafc79cf")
    ref.trigger = "on_create_or_write"
    # restrict filter to avoid the action getting triggered on on_update
    ref.filter_pre_domain = """[["name", "=", False]]"""
    ref.filter_domain = """["&",["x_studio_projet_doublon","!=",False],["partner_id","!=",False]]"""

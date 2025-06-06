/** @odoo-module **/

odoo.define('arch_chatter_inheritance.ChatterToggleButton', function (require) {
    'use strict';

    const Chatter = require('mail.Chatter');
    const { patch } = require('web.utils');

    patch(Chatter.prototype, 'arch_chatter_inheritance.ChatterToggleButton', {
        async _onToggleMessagesVisibility(ev) {
            ev.preventDefault();
            ev.stopPropagation();

            // Appel à la méthode backend pour basculer la visibilité des messages
            await this._rpc({
                model: this.'mail.thread',
                method: 'action_toggle_message_by_subtype',
            });

            // Forcer le rafraîchissement du Chatter pour refléter les changements
            this._reload();
        },
    });
});

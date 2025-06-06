/** @odoo-module **/

odoo.define('arch_chatter_inheritance.ChatterHideButton', function (require) {
    'use strict';

    const Chatter = require('mail.Chatter');
    const rpc = require('web.rpc');

    Chatter.include({
        renderButtons: function () {
            this._super.apply(this, arguments);

            if (this.$buttons) {
                const $btn = $('<button/>', {
                    text: 'Masquer Messages',
                    class: 'btn btn-primary',
                    click: this._onHideMessages.bind(this),
                });

                this.$buttons.append($btn);
            }
        },

        _onHideMessages: function () {
            const self = this;

            // Appel serveur pour masquer les messages
            rpc.query({
                model: 'mail.message',
                method: 'action_hide_messages',
            }).then(function () {
                // Recharge la vue pour ne plus afficher les messages masqués
                self.trigger_up('reload');
            });
        },
    });
});



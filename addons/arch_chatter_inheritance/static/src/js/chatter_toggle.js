/** @odoo-module **/
import { Chatter } from "@mail/core/web/chatter";
import { Thread } from '@mail/core/common/thread';
import { patch } from "@web/core/utils/patch";
import { useState, onWillStart } from "@odoo/owl";

patch(Chatter.prototype ,{
    setup(...args) {
        super.setup(...args);

        // Set default settings
        this.arch_chatter_settings = useState({
            show_secondary_messages: true, 
        });

        // Get settings from localstorage if exists
        onWillStart(async () => {
            Object.assign(this.arch_chatter_settings, JSON.parse(localStorage.getItem('odoo_arch_chatter_settings'))??this.arch_chatter_settings)
        });


        // Update Localstorage
        this.updateArchSettings = (setting, value) => {
            var new_arch_chatter_settings = this.arch_chatter_settings
            new_arch_chatter_settings[setting] = value
            Object.assign(this.arch_chatter_settings, {...new_arch_chatter_settings})
            localStorage.setItem('odoo_arch_chatter_settings',JSON.stringify(this.arch_chatter_settings))
        }
    },
});

patch(Thread, {
    props: [
        ...Thread.props,
        "hideSecondary?"
    ],
    defaultProps: {
        ...Thread.defaultProps,
        hideSecondary : false,
    },
});


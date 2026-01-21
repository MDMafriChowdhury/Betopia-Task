/** @odoo-module **/

import { registry } from "@web/core/registry";
import { _t } from "@web/core/l10n/translation";

// We access the standard user_menuitems registry
const userMenuRegistry = registry.category("user_menuitems");

function changePasswordItem(env) {
    return {
        type: "item",
        id: "change_password",
        description: _t("Change Password"),
        callback: async () => {
            // Trigger the action to open the Wizard
            const action = {
                type: "ir.actions.act_window",
                res_model: "user.change.password.wizard", // Updated Model Name
                view_mode: "form",
                views: [[false, "form"]],
                target: "new",
                name: _t("Change Password"),
            };
            await env.services.action.doAction(action);
        },
        sequence: 50,
    };
}

// Add our item to the registry
userMenuRegistry.add("change_password", changePasswordItem);
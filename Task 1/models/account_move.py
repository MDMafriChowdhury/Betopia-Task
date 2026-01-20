import re
from odoo import models, api, _

class AccountMove(models.Model):
    _inherit = 'account.move'

    def _post(self, soft=True):
        """
        Override _post to trigger auto-reconciliation after the move is posted.
        This covers Journal Entries and Bank Statement Lines (which generate moves).
        """
        # Call super to perform the standard posting logic
        posted = super(AccountMove, self)._post(soft=soft)

        # Iterate through the posted moves to perform our custom logic
        for move in self:
            self._attempt_so_reconciliation(move)

        return posted
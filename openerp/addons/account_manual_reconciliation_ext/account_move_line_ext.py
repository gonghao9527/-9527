# -*- coding: utf-8 -*-
from openerp.osv import fields
from openerp.osv import osv
from openerp import models, SUPERUSER_ID
from openerp.tools.translate import _

class account_move_line(osv.osv):
    _inherit = "account.move.line"
    '''
        反核销操作后去修改res.partner的最后核销时间
    '''
    def _remove_move_reconcile(self, cr, uid, move_ids=None, opening_reconciliation=False, context=None):
        super(account_move_line, self)._remove_move_reconcile(cr, uid, move_ids=move_ids,
                                                                    opening_reconciliation=opening_reconciliation,
                                                                    context=None)
        for account_move_line_objs in self.browse(cr, uid, move_ids, context=context):
            obj_res_partner = self.pool.get('res.partner')
            obj_res_partner.mark_last_reconciliation_date_when_unreconciled(cr, uid, account_move_line_objs.partner_id.id, context=None)
        return True

class res_partner(osv.osv):
    _inherit = 'res.partner'
    '''
        标记反核销操作后,res.partner的最后核销时间
    '''
    def mark_last_reconciliation_date_when_unreconciled(self, cr, uid, partner_id, context=None):
        cr.execute("""
                UPDATE res_partner SET last_reconciliation_date = TEMP .last_reconciliation_date FROM
                  (
                    SELECT MAX(write_date) AS last_reconciliation_date
                        FROM account_move_line
                        WHERE reconcile_id IS NOT NULL AND partner_id = %s
                  ) AS TEMP
                WHERE ID = %s
               """, (partner_id,partner_id))
        return True
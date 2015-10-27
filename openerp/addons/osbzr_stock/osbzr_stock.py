# -*- coding: utf-8-*- 

from openerp import models,api,_
from openerp.osv import osv

class stock_transfer_details(osv.TransientModel):
    _inherit = 'stock.transfer_details'
    @api.one
    def do_detailed_transfer(self):
        '''
                    移动时检查输入的产品、库位、批次、包装、数量是否足够
        '''
        plan_qty={}  #移库单上的产品数量
        tran_qty={}  #transfer上的产品数量
        res={}       #查出要出库的产品的列表和数量。
        
        for line in self.picking_id.move_lines:
            if plan_qty.has_key(line.product_id.id):
                plan_qty[line.product_id.id]+=line.product_uom_qty
            else:
                plan_qty.update({line.product_id.id:line.product_uom_qty})
                
        for item in self.item_ids:
            if self.picking_id.picking_type_code=="incoming":
                continue       #只考虑出库单的情况
            if item.product_id.id not in plan_qty.keys():
                raise osv.except_osv(_('错误'), _('移动的产品 <%s> 不在移库单上！' % item.product_id.name))
            
            if tran_qty.has_key(item.product_id.id):
                tran_qty[item.product_id.id]+=item.quantity
            else:
                tran_qty.update({item.product_id.id:item.quantity})
                
            new_key = (item.product_id.id,item.sourceloc_id.id,item.lot_id.id,item.package_id.id)
            if res.has_key(new_key):
                res[new_key] += item.quantity
            else:
                res.update({new_key:item.quantity})
                
        for key in tran_qty.keys():
            if tran_qty[key] > plan_qty[key]:
                raise osv.except_osv(_('错误'), _('移动的产品 <%s> 数量不能大于该产品移库单上的数量！' % self.env['product.product'].browse(key).name))
                      
        for key in res.keys():
            all_number=0
            #循环得出stock.quant中包含（产品，库位，批次，包装）的列表
            for quant in self.env['stock.quant'].search([('product_id','=',key[0]),('location_id','=',key[1]),('lot_id','=',key[2]),('package_id','=',key[3])]):
                all_number += quant.qty                   
                    
            #检查产品数量是否正确
            if all_number < res[key]:
                raise osv.except_osv(_('错误'), _('移动的产品 <%s> 数量不能大于该产品的库存数量！' % self.env['product.product'].browse(key[0]).name))
        return super(stock_transfer_details,self).do_detailed_transfer()
    
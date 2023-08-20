from odoo import api, fields, models
from odoo.exceptions import ValidationError
                                  
class Material(models.Model):
    _name = 'master.material'
    _description = 'Master Material'

    @api.constrains('price')
    def _check_something(self):
        for record in self:
            if record.price < 100:
                raise ValidationError('Price cannot below $100')

    code = fields.Char(
        string='Material Code',
        required=True
    )

    name = fields.Char(
        string='Material Name',
        required=True
    )
    
    type = fields.Selection(
        [('Fabric', 'Fabric'), ('Jeans', 'Jeans'), ('Cotton', 'Cotton')],
        string='Type',
        required=True
    )
    
    price = fields.Integer(
        string='Price',
        required=True
    )
    
    supplier = fields.Char(
        string='Supplier',
        required=True
    )

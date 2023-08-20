# -*- coding: utf-8 -*-
import json
from odoo import http
from odoo.http import request, Response


class MaterialApp(http.Controller):
    @http.route('/material_app/material_app/', auth='public', methods=['GET'], csrf=False)
    def index(self, **kw):
        # return "Hello, world"
        try:
            result = http.request.env['master.material'].search([])
        except:
            return '<h1>Access Denied</h1>'
        
        temp = '<ul>'
        for row in result:
            temp += '<li>' + row['name'] + '</li>'

        temp = '</ul>'
        return temp


    @http.route('/material_app/material_app/objects/', auth='public')
    def list(self, **kw):
        return http.request.render('material_app.list', {
            'root': '/material_app/material_app',
            'objects': http.request.env['master.material'].search([]),
        })

    @http.route('/material_app/material_app/objects/<model("material_app.material_app"):obj>/', auth='public')
    def object(self, obj, **kw):
        return http.request.render('material_app.object', {
            'object': obj
        })
    
    @http.route('/api/material', auth='public', methods=['GET'])
    def get_list_event(self):
        data = []
        event = request.env['master.material'].sudo().search([])
        headers_json = {'Content-Type': 'application/json'}    
        for eve in event:
            data.append({
                'code': eve.code,
                'name': eve.name,
                'type': eve.type,
                'price': eve.price,
                'supplier': eve.supplier
            })
        result = {
            'data': data,
            'errors': {},
            'meta': {}
        }
        return Response(json.dumps(result), headers=headers_json)

    @http.route('/api/material/insert', auth='public', type='json')
    def create_material(self, **rec):
        if request.jsonrequest:
            if (rec['code'] and rec['name'] and rec['type'] and rec['price'] and rec['supplier']):
                if (rec['price'] >= 100):
                    if (rec['type'] == 'Fabric' or rec['type'] == 'Jeans' or rec['type'] == 'Cotton'):
                        vals = {
                            'code': rec['code'],
                            'name': rec['name'],
                            'type': rec['type'],
                            'price': rec['price'],
                            'supplier': rec['supplier']
                        }
                        
                        new_material = request.env['master.material'].sudo().create(vals)
                        args = {'sucess': True, 'message': 'Success', 'id': new_material.id}
                    else:
                        args = {'sucess': False, 'message': 'Material Type should between Fabric, Jeans, or Cotton'}
                else:
                    args = {'sucess': False, 'message': 'Price cannot below $100'}
            else:
                args = {'sucess': False, 'message': 'Failed'}
        return args

    @http.route('/api/material/update', auth='public', type='json')
    def update_material(self, **rec):
        if request.jsonrequest:
            if (rec['code'] and rec['name'] and rec['type'] and rec['price'] and rec['supplier']):
                if (rec['price'] >= 100):
                    if (rec['type'] == 'Fabric' or rec['type'] == 'Jeans' or rec['type'] == 'Cotton'):
                        old_material = request.env['master.material'].sudo().search([('id', '=', rec['id'])])
                        # old_material = request.env['master.material'].sudo().browse(rec['id'])
                        old_material.write({
                            'code': rec['code'],
                            'name': rec['name'],
                            'type': rec['type'],
                            'price': rec['price'],
                            'supplier': rec['supplier']
                        })

                        args = {'sucess': True, 'message': 'Success', 'id': old_material.id}
                    else:
                        args = {'sucess': False, 'message': 'Material Type should between Fabric, Jeans, or Cotton'}
                else:
                    args = {'sucess': False, 'message': 'Price cannot below $100'}
            else:
                args = {'sucess': False, 'message': 'Failed'}
        return args
    
    @http.route('/api/material/delete', auth='public', type='json')
    def delete_material(self, **rec):
        if request.jsonrequest:
            if (rec['id']):
                old_material = request.env['master.material'].sudo().search([('id', '=', rec['id'])]).unlink()
                args = {'sucess': True, 'message': 'Success'}
            else:
                args = {'sucess': False, 'message': 'Failed'}
        return args
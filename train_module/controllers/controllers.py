# -*- coding: utf-8 -*-
# from odoo import http


# class TrainModule(http.Controller):
#     @http.route('/train_module/train_module/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/train_module/train_module/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('train_module.listing', {
#             'root': '/train_module/train_module',
#             'objects': http.request.env['train_module.train_module'].search([]),
#         })

#     @http.route('/train_module/train_module/objects/<model("train_module.train_module"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('train_module.object', {
#             'object': obj
#         })

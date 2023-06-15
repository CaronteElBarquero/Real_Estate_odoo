{

    'name': 'Real Estate',
    'version': '1.0.0',
    'author': 'Miguel',
    'license': 'LGPL-3',
    'sequence': 5,
    'depends': [
         'base',
         'project',
         'mail'
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/estate_property_security.xml',

        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',

        'views/estate_property_type_views.xml',
        
        'views/estate_property_tag_views.xml',
        'views/estate_property_kanban_views.xml',
        'views/estate_menus.xml',
        'views/res_user_inherit.xml',
    ],
    'application': True
    
}


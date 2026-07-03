{
    'name': 'Library Tracker',
    'version': '1.0',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/library_book_views.xml',
        'views/library_member_views.xml',
        'views/library_borrow_record_views.xml',
        'views/library_category_views.xml',
        'views/library_book_tag_views.xml',
        'views/res_users_views.xml',
        'views/library_author_views.xml',
        'views/library_menus.xml'
    ],
    'installable': True,
    'application': True,
}

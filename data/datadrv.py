''' DO NOT EDIT HERE '''
def pytest_generate_tests(metafunc):
    idlist = []
    argvalues = []
    for scenario in metafunc.cls.scenarios:
        idlist.append(scenario[0])
        items = scenario[1].items()
        argnames = [x[0] for x in items]
        argvalues.append(([x[1] for x in items]))
    metafunc.parametrize(argnames, argvalues, ids=idlist)
''' EDIT BELOW '''

scenario1 = ('ACME_Manage_Keys', { 'org': 'ACME_Corporation', 
                                   'perm_name': 'ManageAcmeCorp', 
                                   'resource': 'activation_keys',
                                   'verb': 'manage_all'})
scenario2 = ('Global_Read_Only', { 'org': 'Global Permissions', 
                                   'perm_name': 'ReadOnlyGlobal', 
                                   'resource': 'organizations', 
                                   'verb': 'read'})


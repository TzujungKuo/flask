user = {
    'name': '123',
    'gender' : '123',
}
query = []
for key, value in user.items():
    if value ! None:
        query.append(key + ' =' + " '{}' ".format(value))
query = ",".join(query)

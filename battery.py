

# TODO implement
@app.route('/battery/add', methods=['POST'])
def battery_add():
    return "true"

# TODO implement
@app.route('/battery/<int:battery_id>', methods=['GET'])
def battery_get_current_status(battery_id):
    return "true"

def battery_get_capacity():
    return "65355"


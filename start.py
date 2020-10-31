from flask import Flask, render_template, redirect, request, jsonify

import trees

app = Flask(__name__)

# Global objects and variables
current_button = [""]
tree_db = trees.TreeDB()
tree_current = trees.Tree(tree_db.get_max())

# Web server part


# Main page
@app.route("/", methods=['GET'])
def hello_world():
    # It isn't good bacause whole page reloads every time when we cahne something in data.
    # Maybe I will fix it later
    # Return main page
    return render_template('index.html', tree_db=tree_db.matrix, tree_cur=tree_current.matrix,
                           current_item_db=tree_db.current_item, current_item=tree_current.current_item,
                           roots=tree_current.roots)


# If we select element in DB tree we will have to save it
@app.route("/db/<int:item>", methods=['GET'])
def select_item_db(item):
    tree_db.set_current(int(item))
    # Call "hello_world()"
    return redirect("/")


# If we select element in Cache tree we will have to save it too
@app.route("/cur/<int:item>", methods=['GET'])
def select_item(item):
    tree_current.set_current(int(item))
    # Call "hello_world()"
    return redirect("/")


# If we push "copy" button we will have to copy element from DB tree to Cache tree
@app.route("/copy", methods=['POST'])
def copy_element():
    # Get current element from DB tree
    element = tree_db.get_element(tree_db.current_item)
    # Insert element to Cache tree
    tree_current.insert_element(element, tree_db.current_item)
    # Call "hello_world()"
    return redirect("/")


# If we push "Del" button we will have to mark it as deleted
@app.route("/del", methods=['POST'])
def delete_element():
    tree_current.del_element()
    # Call "hello_world()"
    return redirect("/")


# If we push "Edit" button we will have to change value
@app.route("/edit", methods=['POST'])
def edit_element():
    # Get new value from page
    value = request.form['value']
    # If value is not empty we will have to save it
    if value != "":
        tree_current.set_value(value)
    # Call "hello_world()"
    return redirect("/")


# If we push "Add" button we will have to add new element in Cache tree
@app.route('/add', methods=['POST'])
def add_element():
    # Get new value from page
    if tree_current.is_current_deleted():
        return jsonify(
            message="Success",
            warning="Current element is deleted! It is not good to add child to him!",
            status=200)
    else:
        print(request.json['value']
              )
        # If value is not empty we will have to add new element
        # if value != "":
        #     # Increase count of elements in our tree
        #     tree_current.inc_max()
        #     # Crete new element
        #     element = {'del': 0, 'children': [], 'value': value, 'root': 0}
        #     # Add it in Cache tree
        #     tree_current.add_element(element, tree_current.max)
    # Call "hello_world()"
    return jsonify(
                   message="Success",
                   status=200)
    #return redirect("/")


# If we push "Reset" button we will have to reset both trees to initially state
@app.route('/reset', methods=['POST'])
def reset_db():
    # Reset DB tree
    tree_db.reset()
    # Reset Cache tree
    tree_current.reset(tree_db.max)
    # Call "hello_world()"
    return redirect("/")


# If we push "Apply" button we will have to save changes from Cache tree to DB tree
@app.route('/apply', methods=['POST'])
def apply_changes():
    # Let's do it
    tree_db.apply(tree_current.matrix)
    # Call "hello_world()"
    return redirect("/")

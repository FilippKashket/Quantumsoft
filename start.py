from typing import Dict, List, Any, Union

from flask import Flask, render_template, redirect, request

import trees

app = Flask(__name__)

current_button = [""]
tree_db = trees.TreeDB()
tree_current = trees.Tree(tree_db.get_max())


@app.route("/", methods=['GET'])
def hello_world():
    print('hello')
    return render_template('index.html', button=current_button[0], tree_db=tree_db.matrix, tree_cur=tree_current.matrix,
                           current_item_db=tree_db.current_item, current_item=tree_current.current_item,
                           roots=tree_current.roots)


@app.route("/db/<int:item>", methods=['GET'])
def select_item_db(item):
    tree_db.set_current(int(item))
    return redirect("/")


@app.route("/cur/<int:item>", methods=['GET'])
def select_item(item):
    tree_current.set_current(int(item))
    return redirect("/")


@app.route("/copy", methods=['POST'])
def copy_element():
    element = tree_db.get_element(tree_db.current_item)
    tree_current.insert_element(element, tree_db.current_item)
    return redirect("/")


@app.route("/del", methods=['POST'])
def delete_element():
    tree_current.del_element()
    return redirect("/")


@app.route("/edit", methods=['POST'])
def edit_element():
    value = request.form['value']
    if value != "":
        tree_current.set_value(value)
    return redirect("/")


@app.route('/add', methods=['POST'])
def add_element():
    value = request.form['value']
    if value != "":
        tree_current.inc_max()
        element = {'del': 0, 'children': [], 'value': value, 'root': 0}
        tree_current.add_element(element, tree_current.max)
    return redirect("/")


@app.route('/reset', methods=['POST'])
def reset_db():
    tree_db.reset()
    tree_current.reset(tree_db.max)
    return redirect("/")


@app.route('/apply', methods=['POST'])
def apply_changes():
    current_button[0] = tree_db.apply(tree_current.matrix)
    return redirect("/")

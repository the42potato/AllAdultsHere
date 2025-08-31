from flask import Blueprint, render_template, current_app

fixed_bp = Blueprint("Fixed Pages", __name__)

@fixed_bp.route('/password_strength')
def password_strength():
    return render_template('/sections/fixed/password_strength.html')

@fixed_bp.route('/styling')
def styling_preview():
    return render_template('/sections/fixed/styling.html')
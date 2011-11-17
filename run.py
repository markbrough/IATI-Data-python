from flask import Flask, render_template, flash, request, Markup
from flaskext.sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, UnicodeText, Date, Float
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///iatidata_new.sqlite'
db = SQLAlchemy(app)

class Activity(db.Model):
    id = db.Column(Integer, primary_key=True)
    package_id = db.Column(UnicodeText)
    source_file = db.Column(UnicodeText)
    activity_lang = db.Column(UnicodeText)
    default_currency = db.Column(UnicodeText)
    hierarchy = db.Column(UnicodeText)
    last_updated = db.Column(UnicodeText)
    reporting_org = db.Column(UnicodeText)
    reporting_org_ref = db.Column(UnicodeText)
    reporting_org_type = db.Column(UnicodeText)
    funding_org = db.Column(UnicodeText)
    funding_org_ref = db.Column(UnicodeText)
    funding_org_type = db.Column(UnicodeText)
    extending_org = db.Column(UnicodeText)
    extending_org_ref = db.Column(UnicodeText)
    extending_org_type = db.Column(UnicodeText)
    implementing_org = db.Column(UnicodeText)
    implementing_org_ref = db.Column(UnicodeText)
    implementing_org_type = db.Column(UnicodeText)
    recipient_region = db.Column(UnicodeText)
    recipient_region_code = db.Column(UnicodeText)
    recipient_country = db.Column(UnicodeText)
    recipient_country_code = db.Column(UnicodeText)
    collaboration_type = db.Column(UnicodeText)
    collaboration_type_code = db.Column(UnicodeText)
    flow_type = db.Column(UnicodeText)
    flow_type_code = db.Column(UnicodeText)
    aid_type = db.Column(UnicodeText)
    aid_type_code = db.Column(UnicodeText)
    finance_type = db.Column(UnicodeText)
    finance_type_code = db.Column(UnicodeText)
    iati_identifier = db.Column(UnicodeText)
    title = db.Column(UnicodeText)
    description = db.Column(UnicodeText)
    date_start_actual = db.Column(UnicodeText)
    date_start_planned = db.Column(UnicodeText)
    date_end_actual = db.Column(UnicodeText)
    date_end_planned = db.Column(UnicodeText)
    status_code = db.Column(UnicodeText)
    status = db.Column(UnicodeText)
    contact_organisation = db.Column(UnicodeText)
    contact_telephone = db.Column(UnicodeText)
    contact_email = db.Column(UnicodeText)
    contact_mailing_address = db.Column(UnicodeText)
    tied_status = db.Column(UnicodeText)
    tied_status_code = db.Column(UnicodeText)
    activity_website = db.Column(UnicodeText)
    
    def __init__(self, title, description):
        self.title = title
        self.description = description

    def __repr__(self):
        return self.title, self.id

class ATransaction(db.Model):
    id = db.Column(Integer, primary_key=True)
    activity_id = db.Column(UnicodeText)
    value = db.Column(Float)
    iati_identifier = db.Column(UnicodeText)
    value_date = db.Column(UnicodeText)
    value_currency = db.Column(UnicodeText)
    transaction_type = db.Column(UnicodeText)
    transaction_type_code = db.Column(UnicodeText)
    provider_org = db.Column(UnicodeText)
    provider_org_ref = db.Column(UnicodeText)
    provider_org_type = db.Column(UnicodeText)
    receiver_org = db.Column(UnicodeText)
    receiver_org_ref = db.Column(UnicodeText)
    receiver_org_type = db.Column(UnicodeText)
    description = db.Column(UnicodeText)
    transaction_date = db.Column(UnicodeText)
    transaction_date_iso = db.Column(UnicodeText)
    flow_type = db.Column(UnicodeText)
    flow_type_code = db.Column(UnicodeText)
    aid_type = db.Column(UnicodeText)
    aid_type_code = db.Column(UnicodeText)
    finance_type = db.Column(UnicodeText)
    finance_type_code = db.Column(UnicodeText)
    tied_status_code = db.Column(UnicodeText)
    disbursement_channel_code = db.Column(UnicodeText)
    
    def __init__(self, value, activity_id):
        self.value = value
        self.activity_id = activity_id

    def __repr__(self):
        return '<Transaction value %r>' % self.value
 
class Sector(db.Model):
    id = db.Column(Integer, primary_key=True)   
    activity_iati_identifier = db.Column(UnicodeText)
    name = db.Column(UnicodeText)
    vocabulary = db.Column(UnicodeText)
    code = db.Column(UnicodeText)
    percentage = db.Column(Integer)
    
    def __init__(self, name, code):
        self.name = name
        self.code = code

    def __repr__(self):
        return '<Sector name %r>' % self.name

class RelatedActivity(db.Model):
    id = db.Column(Integer, primary_key=True)
    activity_id = db.Column(UnicodeText)
    reltext = db.Column(UnicodeText)
    relref = db.Column(UnicodeText)
    reltype = db.Column(UnicodeText)

@app.route("/")
@app.route("/activities/")
@app.route("/activities/<int:activity_id>")
def activities(activity_id=None):
    if activity_id:
        p = Activity.query.filter_by(id=activity_id).first()
        return render_template('activity.html', project=p)
    else:
        c = Activity.query.count()
        if request.args.getlist('page'):
            thispage = int((request.args.getlist('page'))[0])
        else:
            thispage = 1
        firstresult = thispage * 10
        lastresult = firstresult + 10
        maxpages = (c/10)
        pages = 'Page: '
        for x in range (1, maxpages):
            pages += ' <a href="?page=' + str(x) + '">' + str(x) + '</a>'
        p  = Activity.query.order_by(Activity.id)[firstresult:lastresult]
        return render_template('activities.html', projects=p, count=c, pages=Markup(pages), page=thispage)

if __name__ == "__main__":
    app.run(debug=True)

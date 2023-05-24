import frappe
import requests
import json
from erpnext.utilities.transaction_base import TransactionBase
from erpnext.crm.utils import (
    CRMNote,
)


def non_match_elements(list_a, list_b):
    non_match = []
    for i in list_a:
        ia = i['id']
        if ia not in list_b:
            non_match.append(i)
    return non_match

def match_cl_no_supplier(cl_no1):
    i1=cl_no1[3:]
    print(i1)
    # print("hello this is function to match the cl_no")
    print("This is Supplier Capturing Process")
    b=frappe.db.sql(f"""select name from `tabSupplier` where whatsapp_no='{i1}' or phone_no='{i1}' or mobile_number='{i1}';""",as_list=True)
    # this is to check whether we have Lead or no? 
    # return b
    if len(b)>0:
        print("This is Equipment Process")
        a=(b[0][0])
        return a       
    else:
        print("None")
        return

def match_cl_no_cus(cl_no1):
    i1 = cl_no1[3:]
    # print("hello this is function to match the cl_no")
    print("This is Customer Capturing Process")
    c = frappe.db.sql(
        f"""select name from `tabCustomer` where whatsapp_no='{i1}' or phone='{i1}' or mobile='{i1}' or phone_ext='{i1}'""", as_list=True)
    # this is to check whether we have customer or no?
    if len(c) > 0:
        print("This is Customer Opportunity Capturing Process")
        oc = frappe.db.sql(
            f"""select name from `tabOpportunity` where opportunity_from='Customer' and whatsapp = '{i1}';""", as_list=True)
        if oc == []:
            ac = (c[0][0])
            return ac
        olc = []
        for i in oc:
            oi = (i[0])
            olc.append(oi)
        oc1 = (oc[0][0])
        ac = (c[0][0])
        return ac, oc1, olc
    else:
        print("None")
        return


def match_cl_no(cl_no1):
    i1 = cl_no1[3:]
    # print("hello this is function to match the cl_no")
    print("This is lead Capturing Process")
    b = frappe.db.sql(
        f"""select name from `tabLead` where whatsapp_no='{i1}' or phone='{i1}' or mobile_no='{i1}' or phone_ext='{i1}';""", as_list=True)
    # this is to check whether we have Lead or no?
    if len(b) > 0:
        print("This is Lead Opportunity Capturing Process")
        o = frappe.db.sql(
            f"""select name from `tabOpportunity` where whatsapp='{i1}' or phone='{i1}' or contact_mobile='{i1}' or phone_ext='{i1}';""", as_list=True)
        if o == []:
            a = (b[0][0])
            return a
        ol = []
        for i in o:
            oi = (i[0])
            ol.append(oi)
        o1 = (o[0][0])
        a = (b[0][0])
        return a, o1, ol
    else:
        print("None")
        return

# working model


def Convert(result):
    res_dct = {result[i]: result[i + 1] for i in range(0, len(result), 2)}
    return res_dct

# this  are four icons as per call


def call_miss_outgoing_icon(a, b,agent_name):
    content = f"<link href='https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200' rel='stylesheet'> <div><span class='material-symbols-outlined' id='missed' style='color: red;'>call_made</span>   &nbsp;<b>Date: {a} </b> &nbsp; <b>Time: {b}</b> &nbsp; <b>Agent_Name: {agent_name}</b></div>"
    return content


def call_ans_outgoing_icon(a, b, c, d, agent_name):
    content = f"<link href='https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200' rel='stylesheet'> <div><span class='material-symbols-outlined' id='answered' style='color: green;'>call_made</span>   &nbsp;<b>Date: {a} </b> &nbsp; <b>Time: {b} &nbsp; &nbsp; <b>Agent_Name: {agent_name}</b> &nbsp; <b>Call Duration: {d}Sec &nbsp; <b>Recording: <a href={c} style='color: blue;'>Click Here!!</a></b></div>"
    return content


def call_miss_incoming_icon(a, b, agent_name):
    content = f"<link href='https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200' rel='stylesheet'> <div><span class='material-symbols-outlined' id='missed' style='color: red;'>call_received</span>   &nbsp;<b>Date: {a} </b> &nbsp; <b>Time: {b}</b> &nbsp; <b>Agent_Name: {agent_name}</b></div>"
    return content


def call_ans_incoming_icon(a, b, c, d, agent_name):
    content = f"<link href='https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200' rel='stylesheet'> <div><span class='material-symbols-outlined' id='answered' style='color: green;'>call_received</span>   &nbsp;<b>Date: {a} </b> &nbsp; <b>Time: {b} &nbsp; &nbsp; <b>Agent_Name: {agent_name}</b> &nbsp; <b>Call Duration: {d}Sec &nbsp; <b>Recording: <a href={c} style='color: blue;'>Click Here!!</a></b></div>"
    return content


def call_log():
    # this is simple code to bring the data from the tata database 
    # url = "https://api-smartflo.tatateleservices.com/v1/call/records?limit=90"
    url = "https://api-smartflo.tatateleservices.com/v1/call/records?limit=100"
    headers = {
    "accept": "application/json",
    "Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjMxMjU2MiwiaXNzIjoiaHR0cHM6XC9cL2Nsb3VkcGhvbmUudGF0YXRlbGVzZXJ2aWNlcy5jb21cL3Rva2VuXC9nZW5lcmF0ZSIsImlhdCI6MTY2NTQwMDM4MiwiZXhwIjoxOTY1NDAwMzgyLCJuYmYiOjE2NjU0MDAzODIsImp0aSI6IlRLZGJLV2tuV1lNQmcxRXUifQ.ne6SKA5wm4P_L9zFzXnCxfxCb-IzNQ9C1h6hLkT0Ozk"
    }
    response =requests.get(url, headers=headers)
    y=response.text
    x=json.loads(y)
    result=[]
    list=[]
    for x2 in x['results']:
        if 'id' in x2:
            result.append("id")
            result.append(x2['id'])
        if 'call_id' in x2:
            result.append("call_id")
            result.append(x2['call_id'])
        if 'status' in x2:
            result.append("status")
            result.append(x2['status'])
        if 'time' in x2:
            result.append("time")
            result.append(x2['time'])
        if 'service' in x2:
            result.append("service")
            result.append(x2['service'])
        if 'date' in x2:
            result.append("date")
            result.append(x2['date'])
        if 'call_duration' in x2:
            result.append("call_duration")
            result.append(x2['call_duration'])
        if 'department_name' in x2:
            result.append("department_name")
            result.append(x2['department_name'])
        if 'agent_name' in x2:
            result.append("agent_name")
            result.append(x2['agent_name'])
        if 'agent_number' in x2:
            result.append("agent_number")
            result.append(x2['agent_number'])
        if 'did_number' in x2:
            result.append("did_number")
            result.append(x2['did_number'])
        if 'client_number' in x2:
            result.append("client_number")
            result.append(x2['client_number'])
        if 'recording_url' in x2:
            result.append("recording_url")
            result.append(x2['recording_url'])
        if 'call_hint' in x2:
            result.append("call_hint")
            result.append(x2['call_hint'])
        if 'description' in x2:
            result.append("description")
            result.append(x2['description'])
        list.append(Convert(result))
    a=list
    # print(len(a))
    b=frappe.db.sql("""select id from `tabCall Logs`;""")
    c=[]
    for i in b:
        for i1 in i:
            c.append(i1)

    non_match = non_match_elements(a, c)

    if len(non_match)>0:
        # print(len(non_match))
        print ("The lists a and c are not the same")
        # print("No match elements: ", non_match)
        for i in non_match:
            print("This is client number fetch field")
            # print(i)
            a=i['date']
            b=i['time']
            c=i['recording_url']
            d=i['call_duration']
            agent_name=i['agent_name']
            cl_no1=i["client_number"]
            get_cust=match_cl_no_cus(cl_no1)
            get_lead=match_cl_no(cl_no1)
            get_supp=match_cl_no_supplier(cl_no1)

            if get_cust==None:
            # working model
                if get_lead==None:
                    if get_supp==None:
                        print("hello None lead, none opportunity, none customer, none supplier")
                        frappe.get_doc(({"doctype" : "Call Logs", "id": i['id'], "call_id": i['call_id'], "service": i['service'], "date": i['date'], "call_duration": i['call_duration']
                        , "department_name": i['department_name'], "agent_name": i['agent_name'], "agent_number": i['agent_number'], "status": i['status'], "time": i['time'], "did_number": i['did_number'], "client_number": i['client_number']
                        , "recording_url": i['recording_url'], "description": i['description'], "call_hint": i['call_hint'] })).insert()
                    else:
                        print("this is the if-else for Only Supplier ")
                        frappe.get_doc(({"doctype" : "Call Logs", "id": i['id'], "call_id": i['call_id'], "service": i['service'], "date": i['date'], "call_duration": i['call_duration']
                        , "department_name": i['department_name'], "status": i['status'], "agent_name": i['agent_name'], "agent_number": i['agent_number'], "status": i['status'], "time": i['time'], "did_number": i['did_number'], "client_number": i['client_number']
                        , "recording_url": i['recording_url'], "supplier": get_supp, "description": i['description'], "call_hint": i['call_hint'] })).insert()
                        if i['status']=="missed":
                            if i['call_hint']=="clicktocall":
                                content=call_miss_outgoing_icon(a, b, agent_name)
                            else:
                                content=call_miss_incoming_icon(a, b, agent_name)
                        else:
                            if i['call_hint']=="clicktocall":
                                content=call_ans_outgoing_icon(a, b, c, d, agent_name)
                            else:
                                content=call_ans_incoming_icon(a, b, c, d, agent_name)
                        activity = frappe.get_doc(
                                    {"doctype": "Comment", "comment_type": "Label","comment_email": "Administrator",
                                    "reference_doctype": "Supplier", "reference_name": get_supp,
                                    "content": content})
                        activity.insert()
                else:
                    print("This is true lead function")
                    # print(len(get_lead))
                    if len(get_lead)==19:
                        print("this is the if-else for CRM-Only-Lead ")
                        frappe.get_doc(({"doctype" : "Call Logs", "id": i['id'], "call_id": i['call_id'], "service": i['service'], "date": i['date'], "call_duration": i['call_duration']
                        , "department_name": i['department_name'], "status": i['status'], "agent_name": i['agent_name'], "agent_number": i['agent_number'], "status": i['status'], "time": i['time'], "did_number": i['did_number'], "client_number": i['client_number']
                        , "recording_url": i['recording_url'], "lead": get_lead, "description": i['description'], "call_hint": i['call_hint'] })).insert()  
                        if i['status']=="missed":
                            if i['call_hint']=="clicktocall":
                                content=call_miss_outgoing_icon(a, b, agent_name)
                            else:
                                content=call_miss_incoming_icon(a, b, agent_name)
                        else:
                            if i['call_hint']=="clicktocall":
                                content=call_ans_outgoing_icon(a, b, c, d, agent_name)
                            else:
                                content=call_ans_incoming_icon(a, b, c, d, agent_name)
                        activity = frappe.get_doc(
                            {"doctype": "Comment", "comment_type": "Label","comment_email": "Administrator",
                            "reference_doctype": "Lead", "reference_name": get_lead,
                            "content": content})
                        activity.insert()
                    else:
                        print("this is the if-else for Lead-Opportunity ")
                        doc4=frappe.get_doc(({"doctype" : "Call Logs", "id": i['id'], "call_id": i['call_id'], "service": i['service'], "date": i['date'], "call_duration": i['call_duration']
                        , "department_name": i['department_name'], "status": i['status'], "agent_name": i['agent_name'], "agent_number": i['agent_number'], "status": i['status'], "time": i['time'], "did_number": i['did_number'], "client_number": i['client_number']
                        , "recording_url": i['recording_url'], "lead": get_lead[0], "description": i['description'], "call_hint": i['call_hint'] }))
                        if i['status']=="missed":
                            if i['call_hint']=="clicktocall":
                                content=call_miss_outgoing_icon(a, b, agent_name)
                            else:
                                content=call_miss_incoming_icon(a, b, agent_name)
                        else:
                            if i['call_hint']=="clicktocall":
                                content=call_ans_outgoing_icon(a, b, c, d, agent_name)
                            else:
                                content=call_ans_incoming_icon(a, b, c, d, agent_name)
                        activity = frappe.get_doc(
                            {"doctype": "Comment", "comment_type": "Label","comment_email": "Administrator",
                            "reference_doctype": "Lead", "reference_name": get_lead[0],
                            "content": content})
                        activity.insert()
                        opo=get_lead[2]
                        for i in opo:
                            activity = frappe.get_doc(
                            {"doctype": "Comment", "comment_type": "Label","comment_email": "Administrator",
                            "reference_doctype": "Opportunity", "reference_name": i,
                            "content": content})
                            activity.insert()
                            doc4.append('opportunity_child',{'opportunity':i})         
                        doc4.insert()
            else:
                if len(get_cust)==3:
                        print("this is the if-else for Opportunity-Customer ")
                        doc3=frappe.get_doc(({"doctype" : "Call Logs", "id": i['id'], "call_id": i['call_id'], "service": i['service'], "date": i['date'], "call_duration": i['call_duration']
                        , "department_name": i['department_name'], "status": i['status'], "agent_name": i['agent_name'], "agent_number": i['agent_number'], "status": i['status'], "time": i['time'], "did_number": i['did_number'], "client_number": i['client_number']
                        , "recording_url": i['recording_url'], "customer": get_cust[0], "description": i['description'], "call_hint": i['call_hint'] }))
                        if i['status']=="missed":
                            if i['call_hint']=="clicktocall":
                                content=call_miss_outgoing_icon(a, b, agent_name)
                            else:
                                content=call_miss_incoming_icon(a, b, agent_name)
                        else:
                            if i['call_hint']=="clicktocall":
                                content=call_ans_outgoing_icon(a, b, c, d, agent_name)
                            else:
                                content=call_ans_incoming_icon(a, b, c, d, agent_name)
                        activity = frappe.get_doc(
                            {"doctype": "Comment", "comment_type": "Label","comment_email": "Administrator",
                            "reference_doctype": "Customer", "reference_name": get_cust[0],
                            "content": content})
                        activity.insert()
                        opo=get_cust[2]
                        for i in opo:  
                            activity = frappe.get_doc(
                            {"doctype": "Comment", "comment_type": "Label","comment_email": "Administrator",
                            "reference_doctype": "Opportunity", "reference_name": i,
                            "content": content})
                            activity.insert()
                            doc3.append('opportunity_child',{'opportunity':i})
                        doc3.insert()        
                    
                else:
                        print("this is the if-else for CRM-Only-Customer ")
                        frappe.get_doc(({"doctype" : "Call Logs", "id": i['id'], "call_id": i['call_id'], "service": i['service'], "date": i['date'], "call_duration": i['call_duration']
                        , "department_name": i['department_name'], "status": i['status'], "agent_name": i['agent_name'], "agent_number": i['agent_number'], "status": i['status'], "time": i['time'], "did_number": i['did_number'], "client_number": i['client_number']
                        , "recording_url": i['recording_url'], "customer": get_cust, "description": i['description'], "call_hint": i['call_hint'] })).insert()
                        if i['status']=="missed":
                            if i['call_hint']=="clicktocall":
                                content=call_miss_outgoing_icon(a, b, agent_name)
                            else:
                                content=call_miss_incoming_icon(a, b, agent_name)
                        else:
                            if i['call_hint']=="clicktocall":
                                content=call_ans_outgoing_icon(a, b, c, d, agent_name)
                            else:
                                content=call_ans_incoming_icon(a, b, c, d, agent_name)
                        activity = frappe.get_doc(
                            {"doctype": "Comment", "comment_type": "Label","comment_email": "Administrator",
                            "reference_doctype": "Customer", "reference_name": get_cust,
                            "content": content})
                        activity.insert()
            frappe.db.commit()
            print("End Note")
    else:
        print ("The lists a and c are the same")
        
@frappe.whitelist()
def click_to_call(agent_number,destination_number):
	url = "https://api-smartflo.tatateleservices.com/v1/click_to_call"
	payload = {
		"agent_number": agent_number,
		"destination_number": destination_number
	}
	headers = {
		"accept": "application/json",
		"Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjMxMjU2MiwiaXNzIjoiaHR0cHM6XC9cL2Nsb3VkcGhvbmUudGF0YXRlbGVzZXJ2aWNlcy5jb21cL3Rva2VuXC9nZW5lcmF0ZSIsImlhdCI6MTY2NTQwMDM4MiwiZXhwIjoxOTY1NDAwMzgyLCJuYmYiOjE2NjU0MDAzODIsImp0aSI6IlRLZGJLV2tuV1lNQmcxRXUifQ.ne6SKA5wm4P_L9zFzXnCxfxCb-IzNQ9C1h6hLkT0Ozk",
		"content-type": "application/json"
	}
	response = requests.post(url, json=payload, headers=headers)
	print(response.text)

# @frappe.whitelist()
# def fetch_api_rc(vehicle_no):
#     # print(vehicle_no)
#     # print(name1)
#     url = "https://api.emptra.com/vehicleSearchLite2"

#     payload = {
#         "vehicleNumber": vehicle_no
#     }
#     headers = {
#         "Content-Type": "application/json",
#         "clientId": "f8d5a944621c40166802c96fe33e8e6f:2d832ad2e5cd0f0eb6529b0ec33dbc49",
#         "secretKey": "9rEi2MMRJVn58TDMOjWVxdK1scfu7vv2nKIOW4kpYWgcN1PcZClcEZm0Uk1vwD4DB"
#     }

#     response = requests.post(url, json=payload, headers=headers)
#     print(response.status_code)
#     offical=response.json()
#     # print(offical)
#     # print(type(offical))
#     # print(len(offical))
#     if offical['code']==103:
#         print("Wrong Vehicle Number Please Check and Type Again....")
#         return "error"
#     else:
#         license=offical['result']['license']
#         registration_date=offical['result']['registration_date']
#         fuel_type=offical['result']['fuel_type']
#         present_address=offical['result']['present_address']
#         vehicle_color=offical['result']['vehicle_color']
#         full_chassis=offical['result']['full_chassis']
#         owner_name=offical['result']['owner']
#         engine=offical['result']['engine']
#         vehicle_class=offical['result']['vehicle_class']
#         maker_model=offical['result']['maker_model']
#         owner_count=offical['result']['owner_count']
#         insurance_date=offical['result']['insurance_date']
#         insurer_name=offical['result']['insurer_name']
#         insurance_policy_no=offical['result']['insurance_policy_no']
#         pollution=offical['result']['pollution']
#         fitness_dt_no_format=offical['result']['fitness_dt']
#         is_blacklisted=offical['result']['is_blacklisted']
#         model=offical['result']['model']
#         financier_name=offical['result']['financier_name']
#         manufacturing_date=offical['result']['manufacturing_date']
#         registration_authority=offical['result']['registration_authority']
#         vehicle_weight=offical['result']['vehicle_weight']
#         seating_capacity=offical['result']['seating_capacity']
#         permanent_address=offical['result']['permanent_address']
#         norms_type=offical['result']['norms_type']
#         return license, registration_date, fuel_type, present_address, vehicle_color, full_chassis, owner_name, engine, vehicle_class, maker_model, owner_count, insurance_date, insurer_name, insurance_policy_no, pollution, fitness_dt_no_format, is_blacklisted, model, financier_name, manufacturing_date, registration_authority, vehicle_weight, seating_capacity,permanent_address, norms_type
        

class Opportunity(TransactionBase, CRMNote):
	def disable_lead(self):
		if self.opportunity_from == "Lead":
			frappe.db.set_value("Lead", self.party_name, {"disabled": 0, "docstatus": 1})
                        

@frappe.whitelist()
def login1(user):
    d=frappe.db.get_value('User',user,'role_profile_name')
    # d1=frappe.db.get_value('Supplier', filters={"email":user})
    frappe.response["role"]=d
    # frappe.response["supplier"]=d1
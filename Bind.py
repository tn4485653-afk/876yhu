from flask import Flask, request, jsonify
import requests
import time
from os import system

app = Flask(__name__)

# ---------------- GLOBAL ----------------
GLOBAL_MAKER = "JNL"
GLOBAL_CHANNEL = "@TEAM_JENIL"

# ---------------- UTILITY ----------------
def convert(s):
    try:
        s = int(s)
        d, h = divmod(s, 86400)
        h, m = divmod(h, 3600)
        m, s = divmod(m, 60)
        return f"{d} Day {h} Hour {m} Min {s} Sec"
    except:
        return "0 Day 0 Hour 0 Min 0 Sec"

def is_success(rsp):
    if rsp.status_code != 200:
        return False
    try:
        rj = rsp.json()
        if not rj.get("success"):
            return False
        data = rj.get("data", {})
        if isinstance(data, dict):
            if data.get("error"): 
                return False
            g_resp = data.get("garena_response", {})
            if isinstance(g_resp, dict) and g_resp.get("error"):
                return False
        err_node = rj.get("error")
        if err_node:
            return False
        return True
    except:
        return False

def show_res_json(rsp_json):
    error_msg = None
    try:
        err_node = rsp_json.get('error')
        data_node = rsp_json.get('data', {})

        if isinstance(err_node, dict):
            g_resp = err_node.get('garena_response', {})
            if isinstance(g_resp, dict) and g_resp.get('error'):
                error_msg = g_resp.get('error')
            elif err_node.get('error'):
                error_msg = err_node.get('error')
            elif err_node.get('message'):
                error_msg = err_node.get('message')
            else:
                error_msg = str(err_node)
        elif isinstance(err_node, str):
            error_msg = err_node

        if not error_msg and isinstance(data_node, dict):
            if data_node.get('error'):
                error_msg = data_node.get('error')
            elif isinstance(data_node.get('garena_response'), dict) and data_node['garena_response'].get('error'):
                error_msg = data_node['garena_response']['error']

        if not error_msg and not rsp_json.get('success'):
            error_msg = rsp_json.get('message') or "Unknown Error"

    except:
        error_msg = "Invalid Response"

    return {
        "success": error_msg is None,
        "error": error_msg,
        "developer": GLOBAL_MAKER,
        "channel": GLOBAL_CHANNEL,
        "raw": rsp_json
    }

def fetch_api_credits():
    global GLOBAL_MAKER, GLOBAL_CHANNEL
    try:
        url = "https://chngeforgotcrownx72.vercel.app/otp"
        rsp = requests.get(url)
        data = rsp.json()
        credit = data.get("credit", {})
        if credit:
            GLOBAL_MAKER = "JNL"
            GLOBAL_CHANNEL = "@TEAM_JENIL"
    except:
        pass 

# ---------------- FUNCTION FLOWS ----------------
def ChanGE_BinD_WiTh_Sec(access, email, otp, sec):
    url_v = "https://chngemailcode48.vercel.app/verify_otp"
    rsp_v = requests.get(url_v, params={'access_token': access, 'email': email, 'otp': otp})
    if not is_success(rsp_v):
        return show_res_json(rsp_v.json())
    auth = rsp_v.json().get("verifier_token") or rsp_v.json().get("data", {}).get("verifier_token")

    url_i = "https://chngemailcode48.vercel.app/verify_identity"
    rsp_i = requests.get(url_i, params={'access_token': access, 'code': sec})
    if not is_success(rsp_i):
        return show_res_json(rsp_i.json())
    iden = rsp_i.json().get("identity_token") or rsp_i.json().get("data", {}).get("identity_token")

    url_c = "https://chngemailcode48.vercel.app/create_rebind"
    rsp_c = requests.get(url_c, params={'access_token': access, 'email': email, 'identity_token': iden, 'verifier_token': auth})
    return show_res_json(rsp_c.json())

def ChanGE_BinD_No_Sec(access, current_email, new_email, otp1, otp2):
    url1 = "https://chngeforgotcrownx72.vercel.app/otp"
    rsp1 = requests.get(url1, params={'access_token': access, 'current_email': current_email})
    if not is_success(rsp1):
        return show_res_json(rsp1.json())

    url2 = "https://chngeforgotcrownx72.vercel.app/verify"
    rsp2 = requests.get(url2, params={'access_token': access, 'current_email': current_email, 'otp': otp1})
    if not is_success(rsp2):
        return show_res_json(rsp2.json())

    iden = rsp2.json().get("identity_token") or rsp2.json().get("data", {}).get("identity_token")

    url3 = "https://chngeforgotcrownx72.vercel.app/newotp"
    rsp3 = requests.get(url3, params={'access_token': access, 'new_email': new_email})
    if not is_success(rsp3):
        return show_res_json(rsp3.json())

    url4 = "https://chngeforgotcrownx72.vercel.app/newverify"
    rsp4 = requests.get(url4, params={'access_token': access, 'new_email': new_email, 'otp': otp2})
    if not is_success(rsp4):
        return show_res_json(rsp4.json())

    auth = rsp4.json().get("verifier_token") or rsp4.json().get("data", {}).get("verifier_token")

    url5 = "https://chngeforgotcrownx72.vercel.app/change"
    rsp5 = requests.get(url5, params={'access_token': access, 'new_email': new_email, 'identity_token': iden, 'verifier_token': auth})
    return show_res_json(rsp5.json())

def UnBinD_WiTh_Sec(access, sec):
    url = "https://crownxnewkey10010.vercel.app/securityunbind"
    rsp = requests.get(url, params={'access_token': access, 'security_code': sec})
    return show_res_json(rsp.json() if is_success(rsp) else {"error": f"HTTP {rsp.status_code}"})

def UnBinD_No_Sec(access, current_email, otp):
    url1 = "https://chngeforgotcrownx72.vercel.app/otp"
    rsp1 = requests.get(url1, params={'access_token': access, 'current_email': current_email})
    if not is_success(rsp1):
        return show_res_json(rsp1.json())

    url2 = "https://chngeforgotcrownx72.vercel.app/verify"
    rsp2 = requests.get(url2, params={'access_token': access, 'current_email': current_email, 'otp': otp})
    if not is_success(rsp2):
        return show_res_json(rsp2.json())

    iden = rsp2.json().get("identity_token") or rsp2.json().get("data", {}).get("identity_token")
    url3 = "https://crownxforgotremove23.vercel.app/forgotunbind"
    rsp3 = requests.get(url3, params={'access_token': access, 'identity_token': iden})
    return show_res_json(rsp3.json())

def ChK(access):
    url = "https://bindinfocrownx612.vercel.app/check"
    rsp = requests.get(url, params={'access_token': access})
    if not is_success(rsp):
        return show_res_json(rsp.json() if rsp.text else {"error": f"HTTP {rsp.status_code}"})
    data = rsp.json()
    return data

def CancEL(access):
    url = "https://bindcnclcrownx34.vercel.app/cancelbind"
    rsp = requests.get(url, params={'access_token': access})
    return show_res_json(rsp.json())

def BinD_NEw(email, access, otp, sec):
    url = "https://bindcnclcrownx34.vercel.app/bind"
    rsp = requests.get(url, params={'access_token': access, 'email': email})
    if not is_success(rsp):
        return show_res_json(rsp.json())
    url_c = "https://bindcnclcrownx34.vercel.app/confirmbind"
    rsp_c = requests.get(url_c, params={'access_token': access, 'email': email, 'otp': otp, 'security_code': sec})
    return show_res_json(rsp_c.json())

def GeT_PLaFTroms(access):
    r = requests.get("https://100067.connect.garena.com/bind/app/platform/info/get",
                     params={'access_token': access},
                     headers={'User-Agent': "GarenaMSDK/4.0.19P9(Redmi Note 5 ;Android 9;en;US;)","Connection":"Keep-Alive","Accept-Encoding":"gzip"})
    if r.status_code not in [200,201]:
        return {"error": "Failed to fetch platforms"}
    j = r.json()
    return j

def Revoke_Token(access):
    url = "https://crownxrevoker73.vercel.app/revoke"
    rsp = requests.get(url, params={'access_token': access})
    return show_res_json(rsp.json())

# ---------------- API ENDPOINT ----------------
@app.route('/api', methods=['GET'])
def api_main():
    fetch_api_credits()
    action = request.args.get("action", "").lower()
    access = request.args.get("access_token")
    email = request.args.get("email")
    otp = request.args.get("otp")
    sec = request.args.get("sec")
    current_email = request.args.get("current_email")
    new_email = request.args.get("new_email")
    otp2 = request.args.get("otp2")

    if action == "bind_change_with_sec":
        return ChanGE_BinD_WiTh_Sec(access, email, otp, sec)
    elif action == "bind_change_no_sec":
        return ChanGE_BinD_No_Sec(access, current_email, new_email, otp, otp2)
    elif action == "unbind_with_sec":
        return UnBinD_WiTh_Sec(access, sec)
    elif action == "unbind_no_sec":
        return UnBinD_No_Sec(access, current_email, otp)
    elif action == "check_bind":
        return ChK(access)
    elif action == "cancel_bind":
        return CancEL(access)
    elif action == "bind_new":
        return BinD_NEw(email, access, otp, sec)
    elif action == "check_links":
        return GeT_PLaFTroms(access)
    elif action == "revoke":
        return Revoke_Token(access)
    else:
        return jsonify({"error": "Action not found"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
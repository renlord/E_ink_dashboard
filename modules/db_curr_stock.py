
"""Show stock values and currency conversion rates."""

import datetime
from modules import d_functions as d_f


def get_currency(C_1_URL, C_1_API, LOCAL_CUR, C_CHECK, color):
    """Retrieve currency conversion rates."""

    C_URL_1 = str(C_1_URL) + '/api/v7/convert?q=' + \
        str(C_CHECK) + '_' + str(LOCAL_CUR) + '&compact=ultra&apiKey=' + str(C_1_API)
    # print(C_URL_1)

    cur_exch = ''
    response_c_1 = d_f.url_content(C_URL_1, 'currency_1', {}, color)
    if response_c_1:
        # print('Connection to Currencyconverterapi successful.')

        c_1_data = response_c_1.json()
        cur_exch = "{:.4f}".format(float(c_1_data[str(C_CHECK) + '_'+str(LOCAL_CUR)]))

    return cur_exch


def get_btc_eth(C_3_URL, C_4_URL, LOCAL_CUR,  color):
    """Retrieve Bitcoin and Etherium exchange rates."""

    C_URL_3 = C_3_URL + str(LOCAL_CUR) + '.json'
    C_URL_4 = C_4_URL + str(LOCAL_CUR).lower()
    # print(C_URL_3)
    # print(C_URL_4)

    bitcoin_exchange = ""
    eth_exchange = ""
    response_c_3 = d_f.url_content(C_URL_3, 'currency_3', {}, color)
    response_c_4 = d_f.url_content(C_URL_4, 'currency_4', {}, color)
    if response_c_3 and response_c_4:
        # print('Connection to Crypto successful.')

        c_3_data = response_c_3.json()
        c_4_data = response_c_4.json()

        bitcoin_exchange = "1 BTC: " + \
            str("{:.2f}".format(float(c_3_data['bpi'][str(LOCAL_CUR)]['rate_float'])))
        eth_exchange = "1 ETH: " + \
            str("{:.2f}".format(float(c_4_data['ethereum'][str(LOCAL_CUR).lower()])))

    return bitcoin_exchange, eth_exchange


def get_year():
    """Return year-month-day, making sure day is 2 digits."""

    datetime_object = datetime.datetime.now()
    if int(datetime_object.day) < 10:
        str_day = "0"+str(datetime_object.day)
    else:
        str_day = str(datetime_object.day)
    year_str = (str(datetime_object.year) + "-" +
                str(datetime_object.month) + "-" + str(str_day))
    return year_str


def get_stock_week(ST_URL, ST_API, ST_C, st_base, LOCAL_CUR, color):
    """Currently unused - see get_stock_weekend which is used unconditionally."""

    st_date = get_year()
    URL_ST = ST_URL + ST_C + "/" + str(st_date) + "?apiKey=" + str(ST_API)
    # print(URL_ST)

    stocks = []
    response_st = d_f.url_content(str(URL_ST), 'currency_stock_week', {}, color)
    if response_st:
        # print('Connection to Stock successful.')
        st_data = response_st.json()
        st_open = st_data["open"]
        st_symbol = st_data["symbol"]
        st_close = st_data["close"]
        stocks.append("-" + st_symbol + ":")
        stocks.append(
            "O: " + str("{:.2f}".format((float(st_open)*float(st_base)))))
        stocks.append(
            "C: " + str("{:.2f}".format((float(st_close)*float(st_base)))))

    return stocks


def get_stock_weekend(ST_URL, ST_API, ST_C, st_base, LOCAL_CUR, color):
    """Request most recent? stock values."""

    URL_ST = ST_URL + ST_C + "/prev?apiKey=" + str(ST_API)
    # print(URL_ST)

    stocks = []
    response_st = d_f.url_content(str(URL_ST), 'currency_stock_weekend', {}, color)
    if response_st:
        # print('Connection to Stock successful.')
        st_data = response_st.json()
        st_open = st_data["results"][0]["o"]
        st_symbol = st_data["results"][0]["T"]
        st_close = st_data["results"][0]["c"]
        stocks.append("-" + st_symbol + ":")
        stocks.append(
            "O: " + str("{:.2f}".format((float(st_open)*float(st_base)))))
        stocks.append(
            "C: " + str("{:.2f}".format((float(st_close)*float(st_base)))))

    return stocks


def run_st_cur_info(C_1_URL, C_3_URL, C_4_URL, LOCAL_CUR, CURR_CHECK, C_1_API,  ST_WE_URL, ST_W_URL, ST_API, ST_C, color):
    """Retrieve currency and stock info."""

    st_i = []
    curr_exch = []
    for cur in CURR_CHECK:
        curr_exch.append("1 " + str(cur) + ": " +
                         str(get_currency(C_1_URL, C_1_API, LOCAL_CUR, cur,  color)))

    btc, eth = get_btc_eth(C_3_URL, C_4_URL, LOCAL_CUR,  color)
    curr_exch.append(btc)
    curr_exch.append(eth)

    if LOCAL_CUR != "USD":
        st_base = get_currency(C_1_URL, C_1_API, LOCAL_CUR, "USD",  color)
    else:
        st_base = 1

    for x_stock in ST_C:
        st_i.append(get_stock_weekend(ST_WE_URL, ST_API, x_stock, st_base, LOCAL_CUR, color))

    return curr_exch, st_i


def draw_cs_mod(t_s_x, t_s_y, draw, curr_exch, stock_item, LOCAL_CUR, color):
    """Place currency/stock on the canvas."""

    draw.text((t_s_x, t_s_y), "Stocks:                            Currency:",
              font=d_f.font_size(22), fill=color)
    t_s_y = t_s_y+30
    t_s_y_0 = t_s_y
    for i in range(len(stock_item)):
        draw.text((t_s_x, t_s_y), str(stock_item[i][0]), font=d_f.font_size(18), fill=color)
        draw.text((t_s_x+75, t_s_y),  str(stock_item[i][1]), font=d_f.font_size(18), fill=color)
        t_s_y = t_s_y + 20
        draw.text((t_s_x+75, t_s_y), str(stock_item[i][2]), font=d_f.font_size(18), fill=color)
        t_s_y = t_s_y + 22
    t_s_y = t_s_y_0
    for j in range(len(curr_exch)):
        draw.text((t_s_x+190, t_s_y),  '-' +
                  str(curr_exch[j]), font=d_f.font_size(18), fill=color)
        t_s_y = t_s_y + 25
    draw.text((t_s_x+195, 230),  'PRICES IN ' +
              str(LOCAL_CUR), font=d_f.font_size(20), fill=color)
    draw.line((615, 0, 615, 260), fill=0, width=2)
    draw.line((615, 220, 900, 220), fill=0, width=2)

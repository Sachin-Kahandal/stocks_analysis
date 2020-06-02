from morningstar import graham_data, dcf_data
from math import sqrt
import time


# Benjamin Graham's way of evaluating stocks
def graham_no(script_code):
    data = graham_data(script_code)
    book_value = data['book_value']
    eps =  data['eps']
    no = sqrt(15 * 1.5 * float(book_value) * float(eps))
    no = round(no, 2)
    return no   

# Adjusted to inflation (Where EPS is 25 and PE ratio is 3)
def adjusted_graham_no(script_code):
    data = graham_data(script_code)
    book_value = data['book_value']
    eps =  data['eps']
    no = sqrt(25 * 3 * float(book_value) * float(eps))
    no = round(no, 2)
    return no

# Kelly Formula
def kelly_bet():
    outcomes = int(input("Enter the total no of possible outcomes of your investment: "))
    prob, returns, value = list(), list(), list()
    # Calculating Edge
    print("probablities should all sum up to 100")
    for i in range(outcomes):
        a = float(input("Enter the probablity of event: "))
        a = a/100
        prob.append(a)
        b = float(input("Enter the returns you get on event: "))
        returns.append(b)

    # data = dict(zip(prob, returns))

    for i in range(outcomes):
        c = (prob[i] * returns[i])
        value.append(c)
    edge = round(sum(value),2)
    print(edge)
    # Odds - The max. you can make on this bet
    d = sorted(returns,reverse=True)
    odds = d[0]
    # How much of your bankroll you shoult bet
    bet = (edge/odds) * 100
    # print("You can bet", bet,"%")
    return bet


def dcf(script_code):
    data = dcf_data(script_code)
    year = data[1]
    dcfdata = data[0]
    # Averaging cashflows
    dcf_year = 5  
    no = 10 - int(dcf_year)    
    if dcf_year > 8:
        b = float(dcfdata[year[no+1]])
        # print("1b is ",b)
        c = float(dcfdata[year[no+2]])
        # print("1c is ",c)
        avg_first = round((b + c)/2, 2)
    else:
        a = float(dcfdata[year[no]])
        # print("1a is ",a)
        b = float(dcfdata[year[no-1]])
        # print("1b is ",b)
        c = float(dcfdata[year[no-2]])
        # print("1c is ",c)
        avg_first = round((a + b + c)/2, 2)

    # print("avg_first is ", avg_first)
    a = float(dcfdata[year[9]])
    # print("2a is ",a)
    b = float(dcfdata[year[8]])
    # print("2b is ",b)
    c = float(dcfdata[year[7]])
    # print("2c is ",c)
    avg_last = round((a + b +c)/2, 2)
    # print("avg_last is ", avg_last)
    
    # 1. Calculating CAGR
    CAGR = ((avg_last - avg_first + abs(avg_first)) / abs(avg_first))**(1/dcf_year)-1
    CAGR = round(CAGR, 2)
    print("CAGR is", CAGR*100)

    # it is very imp to comeup with realistic CAGR, typically should be lower than 20.
    # considering high CAGR can mess up assumptions drastically
    s = str(input("Do you want to change CAGR? Enter 'yes', else anything: "))
    if s == "yes":
        CAGR = float(input("Enter the CAGR: "))
        CAGR = CAGR/100
    else:
        pass
    
    # 2. Calculating Future Cashflows
    # future_year1 = (last_number x 1.(growth_rate x ^estimateyear_no)
    fcf = list()
    for i in range(1, dcf_year+1):
        a = round((avg_last * ((1+CAGR)**i)), 2)
        fcf.append(a)
    
    # 3. Calculate Discounted cashflow
    # Discounted cash flows = (CF1/DR**1) + (CF2/DR**2) + (CF3/DR**3)
    # dr = discounted rate
    dr = 0.10
    no = len(fcf)
    dcf_list = list()
    for i in range(no):
        a = (fcf[i]/((1+dr)**(i+1)))
        dcf_list.append(a)
    dcf = round(sum(dcf_list),2)
    # print("dcf is ", dcf)

    # 4. Calculate terminal value
    # TV (Terminal Value) = (CF(last_estimated_year) * (1+IG)) / (DR — IG)
    # ig = infinite growth_rate
    ig = 0.03
    tv = round((fcf[no-1] * (1 + ig)) / (dr-ig), 2)
    # print("tv is ", tv)

    # 5. Adding tv(Terminal Value) and dcf(Discounted Cashflow)
    value = tv + dcf
    # print("value is ", value)

    # 6. Calculating Intrinsic value
    # Fair/Intrinsic value = (TV + discounted cash flows) / (discount rate**dcf_year)
    intrinsic_value = round(((value)/(1+dr)**dcf_year), 2)

    return intrinsic_value



def calculate_dcf():
    dcf_year = int(input("Enter the no of years you want to calculate dcf for: "))
    print("Make sure you avg the cashflows, as companies can easily manipulate them")
    avg_first = float(input("Enter the free cashflow for first year of estimate: "))
    avg_last = float(input("Enter the free cashflow for last year of estimate: "))

    # 1. Calculating CAGR
    CAGR = ((avg_last - avg_first + abs(avg_first)) / abs(avg_first))**(1/dcf_year)-1
    CAGR = round(CAGR, 2)
    print("CAGR is ", CAGR*100,"%")
    s = str(input("Do you want to change CAGR? Enter 'yes', else anything: "))
    if s == "yes":
        CAGR = float(input("Enter the CAGR: "))
        CAGR = CAGR/100
    else:
        pass
        
    time.sleep(1)

    # 2. Calculating Future Cashflows
    print("Calculating future cashfolw: ")
    fcf = list()
    for i in range(1, dcf_year+1):
        a = round((avg_last * ((1+CAGR)**i)), 2)
        time.sleep(0.5)
        print("dcf for year ", i ,":", a)
        fcf.append(a)
    time.sleep(1)

    # 3. Calculate Discounted cashflow 
    print("Calculating discounted cashflow")
    print("Discount rate we use here is 8%")
    a = str(input("To use your own discount rate? Enter 'yes', else anything: "))
    if a == "yes":
        dr = int(input("Enter the discount rate: "))
    else:
        dr = 8
    dr = dr/100
    no = len(fcf)
    dcf_list = list()
    for i in range(no):
        a = (fcf[i]/((1+dr)**(i+1)))
        dcf_list.append(a)
    dcf = round(sum(dcf_list),2)
    time.sleep(2)
    print("Total sum of DCF is ", dcf)
    time.sleep(1)

    # 4. Calculate terminal value
    print("Calculating terminal value")
    print("Infinite growth rate we use here is 3%")
    b = str(input("To use your own Infinite growth rate? Enter yes, else anything: "))
    if b == "yes":
        ig = int(input("Enter the discount rate in %: "))
    else:
        ig = 3
    ig = ig/100
    tv = (fcf[no-1] * (1 + ig)) / (dr-ig)
    tv = round(tv, 2)
    time.sleep(2)
    print("Terminal Value is ", tv)
    time.sleep(1)

    # 5. Adding tv(Terminal Value) and dcf(Discounted Cashflow)
    print("Adding terminal value and discountd cash flow")
    value = tv + dcf
    print("Value is ", value)
    time.sleep(2)

    # 6. Calculating Intrinsic value
    print("Calculating final intrinsic value: ")
    time.sleep(2)
    intrinsic_value = round(((value)/(1+dr)**dcf_year), 2)
    print("Intrinsic value is ", intrinsic_value )

    # 7. Calculating Margin of safety for best buy
    time.sleep(1)
    print("We consider margin of safety of 25%")
    a = str(input("To use your own discount rate? Enter 'yes', else anything: "))
    if a == "yes":
        mos = int(input("Enter the margin of safety in %: "))
    else:
        mos = 25
    mos = mos/100
    sub = intrinsic_value * mos
    best_buy = intrinsic_value - sub
    print("Best buy with ", mos*100, "% " "is ", best_buy)

print(graham_no(509243))
print(dcf(509243))
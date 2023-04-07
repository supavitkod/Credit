def risk_assess(x):
    target = ''
    if x in (1,2,3,4,5) :
       target = 1 #risky
    else:
        target = 0  #not risky

    return target
# Date: 6/5/2020
# Name: Citlali

# Part A: House Hunting
def monthsToSave():
    annual_salary = int(input('Enter your annual salary: '))
    portion_saved = float(
        input('Enter the percent of your salary to save, as a decimal: '))
    total_cost = int(input('Enter the cost of your dream home: '))
    total_months = 0
    portion_down_payment = .25*total_cost
    current_savings = 0  # but we will add to it
    while current_savings < portion_down_payment:
        total_months += 1
        current_savings += current_savings*.04/12 + annual_salary/12*portion_saved
    print('Number of months: ', total_months)
    return total_months

# print(monthsToSave())


# Part B: Saving, With a Raise
def monthsToSavewithRaise():
    annual_salary = int(input('Enter your annual salary: '))
    portion_saved = float(
        input('Enter the percent of your salary to save, as a decimal: '))
    total_cost = int(input('Enter the cost of your dream home: '))
    semi_annual_raise = float(
        input('Enter the semi-annual raise, as a decimal: '))
    total_months = 0
    portion_down_payment = .25*total_cost
    current_savings = 0  # but we will add to it
    while current_savings < portion_down_payment:
        if total_months % 6 == 0 and total_months != 0:
            annual_salary *= (1+semi_annual_raise)
        total_months += 1
        current_savings += current_savings*.04/12 + annual_salary/12*portion_saved
    return total_months

# print(monthsToSavewithRaise())

# Part C: Finding the Right Amount to Save Away
def fullySavingPlanFails(salary, portion_down_payment):
    fully_saving_savings = 0 
    for i in range(0, 36):
            if i % 6 == 0 and i != 0: salary *= (1+.07)
            fully_saving_savings += fully_saving_savings*.04/12 + salary/12
    if fully_saving_savings < portion_down_payment-100: return True 
    return False

def rightToSaveAway():
    annual_salary = float(input('Enter the starting salary: '))
    total_cost = 1000000
    portion_down_payment = .25*total_cost
    top = 10000
    bottom = 0
    steps = 0
    if fullySavingPlanFails(annual_salary, portion_down_payment): 
        return print('It is not possible to pay the down payment in three years.')
    while True:
        steps += 1
        savings_rate = float(top+bottom)/20000.00
        current_savings = 0
        anny_sal = annual_salary
        for i in range(0, 36):
            if i % 6 == 0 and i != 0: anny_sal *= (1+.07)
            current_savings += current_savings*.04/12 + anny_sal/12*savings_rate
        if current_savings < portion_down_payment-100:  # too little => save more
            bottom = (top + bottom)/2.0
        elif current_savings > portion_down_payment+100:  # too much => save less
            top = (top + bottom)/2.0 
        else:
            print('Best savings rate: ', savings_rate)
            return print('Steps in bisection search: ', steps)
            
# print(rightToSaveAway())

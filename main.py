"""
 Andrey Lototskiy

 This is a script for 1619 Up-a-creek Robotics finance department

 The purpose of this script is to convert Stripe files into an appropriate CSV format
 How this script works:

 1. for each line in the Stripe file, create two lines in the QB file,
 (1) for the payment & (2) for the fee

2. Date from column B

3. Payment amount column E

4. Fee is -1 * columns F

5. Description from column F
"""

# ---------------------------------------------------------------------------------------

import pandas as pd
import numpy as np

# Get the data from the CSV
inputCSV = pd.read_csv("Itemized_balance_change_from_activity_charge_USD_2022-05-01_to_2022-05-31_America-Denver -"
                       " Itemized_balance_change_from_activity_charge_USD_2022-05-01_to_2022-05-31_America-Denver.csv")
# Make a new pandas dataframe with the correct columns, but no data
data = {'Date': [], 'Description': [], 'Amount': []}
QBfile = pd.DataFrame(data=data)

# Loop through all the columns of the original dataframe
numRows = inputCSV.shape[0]
for i in range(numRows):
    # Here we can get every row of the original CSV, and extract the data that we need into a new dataframe

    # gross: number of dollars received
    gross = "{:.2f}".format(inputCSV.iloc[i]['gross'])
    # print(gross)
    customerName = inputCSV.iloc[i]['customer_name']
    # print(customerName)
    paymentDate = inputCSV.iloc[i]['created']
    paymentDate = paymentDate[0:paymentDate.find(' ')]
    paymentDate = str(int(paymentDate[5:7])) + '/' + str(int(paymentDate[8:10])) + '/' + str(int(paymentDate[0:4]))
    # print(paymentDate)
    fee = "{:.2f}".format(float(inputCSV.iloc[i]['fee']) * -1)
    stripe = 'Stripe'

    layer = pd.DataFrame([[paymentDate, customerName, gross], [paymentDate, stripe, fee]],
                         columns=['Date', 'Description', 'Amount'])

    QBfile = pd.concat([QBfile, layer], axis=0)

# Converting the DataFrame to csv
QBfile.to_csv("./qbfile.csv", index=False)

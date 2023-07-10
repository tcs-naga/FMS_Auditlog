import pandas as pd

audit_record_excel = pd.read_excel('Testdata.xlsx',sheet_name='queryserach',engine='openpyxl',)
audit_record_dataframe = pd.DataFrame(audit_record_excel)

year = audit_record_dataframe.loc[0][0]
month= audit_record_dataframe.loc[0][1]
event = audit_record_dataframe.loc[0][2]
asset = audit_record_dataframe.loc[0][3]
user = audit_record_dataframe.loc[0][4]
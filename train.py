import pandas as pd
from function import function
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
from sklearn.feature_extraction import DictVectorizer
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier
from function import assess_risk
from function import convert_day
from sklearn.metrics import confusion_matrix,classification_report,roc_auc_score


raw_credit = pd.read_csv('credit_record.csv')
raw_application = pd.read_csv('application_record.csv')

df = raw_application.merge(raw_credit, on='ID', how='inner')
df['FLAG_MOBIL'] = df['FLAG_MOBIL'].astype('category')
df['FLAG_WORK_PHONE'] = df['FLAG_WORK_PHONE'].astype('category')
df['FLAG_PHONE'] = df['FLAG_PHONE'].astype('category')
df['FLAG_EMAIL'] = df['FLAG_EMAIL'].astype('category')
df['OCCUPATION_TYPE'].fillna('Others',inplace=True)

df = df.rename(columns={'CODE_GENDER': 'Gender', 'FLAG_OWN_CAR': 'Own_car', 
                               'FLAG_OWN_REALTY':'Own_property','CNT_CHILDREN':'Nbchildren',
                               'AMT_INCOME_TOTAL':'Total_income_per_year','NAME_INCOME_TYPE':'Income_type',
                               'NAME_EDUCATION_TYPE':'Education_level','NAME_FAMILY_STATUS':'Marital_status',
                               'NAME_HOUSING_TYPE':'Way_of_living','FLAG_WORK_PHONE':'Workphone',
                               'FLAG_PHONE':'Phone','FLAG_EMAIL':'Email','FLAG_MOBIL':'mobile','OCCUPATION_TYPE':'Occupation',
                               'CNT_FAM_MEMBERS':'Nbfamily_member'})

### Deal with the outlier
number_Children_outlier = df['Nbchildren'].quantile(0.999)
df = df[df['Nbchildren'] <= number_Children_outlier]
Total_income_per_year_outlier = df['Total_income_per_year'].quantile(0.999)
df = df[df['Total_income_per_year'] <= Total_income_per_year_outlier]

grouped=df.groupby('ID')['STATUS'].value_counts()
grouped

credit_grouped=pd.get_dummies(data=df,columns=['STATUS'],
                              prefix='',prefix_sep='').groupby('ID')[sorted(df['STATUS'].unique().tolist())].sum()

credit_grouped=credit_grouped.rename(columns=
                      {'0':'pastdue_1_29',
                       '1':'pastdue_30_59',
                       '2':'overdue_60_89',
                       '3':'overdue_90_119',
                       '4':'overdue_120_149',
                       '5':'overdue_over_150',
                       'C':'paid_off',
                        'X':'no_loan'})

overall_pastdue=['pastdue_1_29','pastdue_30_59',	'overdue_60_89',	'overdue_90_119'	,'overdue_120_149',	'overdue_over_150']
credit_grouped['Total_months_credit_registered']=df.groupby('ID')['MONTHS_BALANCE'].count()
credit_grouped['Delinquent_accounts']=credit_grouped[['pastdue_30_59','overdue_60_89','overdue_90_119'	,'overdue_120_149'	,'overdue_over_150']].sum(axis=1)
credit_grouped['Ordinary_accounts']=credit_grouped[['pastdue_1_29']].sum(axis=1)
credit_grouped['overall_pastdue']=credit_grouped[overall_pastdue].sum(axis=1)
credit_grouped.head()

target =[]
for index,row in credit_grouped.iterrows() :
  if row ['no_loan']==row['Total_months_credit_registered']:
    target.append(0)
  elif row['overall_pastdue'] == row['Ordinary_accounts']:
    target.append(0)
  elif row['paid_off'] >= 12 & row['Delinquent_accounts'] <= 2: 
    target.append(0)
  elif row['no_loan'] >= 12 & row['Delinquent_accounts'] <=2:
    target.append(0)
  elif row['Delinquent_accounts'] <= 0:
    target.append(0)
  else: 
    target.append(1)

credit_grouped['good_or_bad']=target

df = function.select_first_month(df)
df['STATUS'].replace({'C':0}, inplace=True)
df['STATUS'] = df['STATUS'].astype('int')
df['STATUS']  = df['STATUS'].apply(assess_risk.risk_assess)

features=['no_loan','Total_months_credit_registered',	'Delinquent_accounts',	'Ordinary_accounts',	'overall_pastdue','good_or_bad']
columns_credit= credit_grouped.loc[:,features]
df = pd.merge(df,columns_credit,on='ID')

risk=[]
for index,row in df.iterrows() :
  if row['STATUS'] == 0  and row['good_or_bad'] == 0 :
    risk.append(0)
  else:
    risk.append(1)

df['Risk']=risk
df['Age'] = df['DAYS_BIRTH'].apply(convert_day.convert_day_to_year)
df['Age'] = df['Age'].astype(int)
df['Experience'] = df['DAYS_EMPLOYED'].apply(convert_day.convert_day_to_year)
df['Total_income_lifetime_employed'] = df['Experience'] * df['Total_income_per_year']
df.drop('DAYS_BIRTH',axis=1,inplace=True)
df.drop('DAYS_EMPLOYED',axis=1,inplace=True)

def employment_status(date):
    # Determine the employment status based on the duration
    if date < 0:
        return "Unemployed"
    else:
        return "Employment"

df['Employment_status'] = df['Experience'].apply(employment_status)
df.set_index('ID',inplace=True)
df.drop(columns=['MONTHS_BALANCE','mobile','STATUS','good_or_bad','no_loan','Delinquent_accounts','Ordinary_accounts','overall_pastdue'],axis=1,inplace=True)


X = df.drop(['Risk'],axis=1)
y = df['Risk']

print("start train test split")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25,stratify=y,random_state=365)

print("start dictvectorizer")
encoded = DictVectorizer(sparse=False)
X_train_dict = encoded.fit_transform(X_train.to_dict('records'))
X_test_dict  = encoded.transform(X_test.to_dict('records'))

oversample = SMOTE(random_state=365)
X_train_balanced,y_train_balanced = oversample.fit_resample(X_train_dict,y_train)

scaler= StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_balanced)
X_test_scaled = scaler.transform(X_test_dict)


y_train_balanced = y_train_balanced.astype('int')
y_test = y_test.astype('int')
XGB_model  =XGBClassifier(use_label_encoder=False,objective='binary:logistic',eval_metric= 'error')

XGB_model.fit(X_train_scaled, y_train_balanced)

print('Xg Boost Model Accuracy : ', XGB_model.score(X_test_scaled, y_test)*100, '%')

prediction = XGB_model.predict(X_test_scaled)
print('\nConfusion matrix :')
print(confusion_matrix(y_test, prediction))
      
print('\nClassification report:')      
print(classification_report(y_test, prediction))

print('\ROC_AUC_SCORE report:')
print(roc_auc_score(y_test,prediction))
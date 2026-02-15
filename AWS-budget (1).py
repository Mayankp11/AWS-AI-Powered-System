#!/usr/bin/env python
# coding: utf-8

# In[26]:


get_ipython().system('pip install pandas matplotlib google-generativeai')


# In[27]:


import pandas as pd


# In[28]:


import matplotlib.pyplot as plt
import numpy as np


# In[29]:


file_path = r"C:\Users\mayan\Downloads\Enterprise_AWS_Cost_Usage_Report.csv"


# In[30]:


df = pd.read_csv(file_path)


# In[31]:


df.head()


# In[32]:


df['UsageDate'] = pd.to_datetime(df['UsageDate'], dayfirst=True)
df['UnblendedCost'] = pd.to_numeric(df['UnblendedCost'], errors='coerce')

df = df.dropna(subset=['UnblendedCost'])

df.info()


# In[33]:


service_summary = (
    df.groupby("Service")["UnblendedCost"]
    .sum()
    .reset_index()
    .sort_values(by="UnblendedCost", ascending=False)
)

service_summary


# In[34]:


account_summary = (
    df.groupby("LinkedAccount")["UnblendedCost"]
    .sum()
    .reset_index()
    .sort_values(by="UnblendedCost", ascending=False)
)

account_summary


# In[35]:


daily_cost = (
    df.groupby("UsageDate")["UnblendedCost"]
    .sum()
    .reset_index()
)

plt.figure()
plt.plot(daily_cost["UsageDate"], daily_cost["UnblendedCost"])
plt.xticks(rotation=45)
plt.title("Daily AWS Cost Trend")
plt.xlabel("Date")
plt.ylabel("Total Cost")
plt.show()


# In[36]:


mean_cost = daily_cost["UnblendedCost"].mean()
std_cost = daily_cost["UnblendedCost"].std()

threshold = mean_cost + 2 * std_cost

daily_cost["Anomaly"] = daily_cost["UnblendedCost"] > threshold

anomalies = daily_cost[daily_cost["Anomaly"] == True]

anomalies


# In[37]:


if not anomalies.empty:
    anomaly_dates = anomalies["UsageDate"]
    
    anomaly_data = df[df["UsageDate"].isin(anomaly_dates)]
    
    anomaly_service_summary = (
        anomaly_data.groupby("Service")["UnblendedCost"]
        .sum()
        .reset_index()
        .sort_values(by="UnblendedCost", ascending=False)
    )
    
    anomaly_service_summary


# In[38]:


print("Anomalies detected:")
print(anomalies)


# In[39]:


if not anomalies.empty:
    anomaly_dates = anomalies["UsageDate"]
    anomaly_data = df[df["UsageDate"].isin(anomaly_dates)]
    
    anomaly_service_summary = (
        anomaly_data.groupby("Service")["UnblendedCost"]
        .sum()
        .reset_index()
        .sort_values(by="UnblendedCost", ascending=False)
    )
    
    print(anomaly_service_summary)


# In[40]:


import os


# In[41]:


import google.generativeai as genai


# In[42]:


api_key = os.getenv("GEMINI_API_KEY")


# In[43]:


genai.configure(api_key=api_key)


# In[44]:


for model in genai.list_models():
    print(model.name)


# In[45]:


model = genai.GenerativeModel("gemini-2.5-flash")

response = model.generate_content("Explain AWS cost optimization in 3 lines.")

print(response.text)


# In[46]:


import sys
print(sys.version)


# In[47]:


import sys
print(sys.executable)


# In[49]:


import google.generativeai as genai

genai.configure(api_key="AIzaSyCR0aZ4UISa73lfjQjeG9u_i8nsA9rETXo")


# In[50]:


for m in genai.list_models():
    print(m.name)


# In[51]:


model = genai.GenerativeModel("gemini-pro-latest")


# In[52]:


cost_text = service_summary.to_string()


# In[53]:


service_summary = df.groupby("Service")["UnblendedCost"].sum().sort_values(ascending=False)

service_summary.head()


# In[54]:


import pandas as pd


# In[55]:


import matplotlib.pyplot as plt
import numpy as np


# In[56]:


file_path = r"C:\Users\mayan\Downloads\Enterprise_AWS_Cost_Usage_Report.csv"


# In[57]:


df = pd.read_csv(file_path)

df.head()


# In[58]:


service_summary = df.groupby("Service")["UnblendedCost"].sum().sort_values(ascending=False)

service_summary.head()


# In[59]:


service_summary = df.groupby("Service")["UnblendedCost"].sum().sort_values(ascending=False)

service_summary.head()


# In[60]:


service_summary = (
    df.groupby("Service")["UnblendedCost"]
    .sum()
    .sort_values(ascending=False)
)

service_summary


# In[61]:


cost_text = service_summary.to_string()
print(cost_text)


# In[62]:


model = genai.GenerativeModel("gemini-2.5-flash")


# In[63]:


prompt = f"""
You are a senior FinOps and Cloud Cost Optimization expert.

Below is the AWS monthly cost breakdown by service:

{cost_text}

Please provide:

1. Top 3 most expensive services.
2. Possible reasons for high cost.
3. Cost optimization strategies.
4. Governance recommendations.
5. Any unusual patterns.

Give structured response.
"""


# In[64]:


response = model.generate_content(prompt)

print(response.text)


# In[65]:


user_prompt = "Explain why EC2 costs might suddenly increase in an AWS account.Give me in 100 words"

response = model.generate_content(user_prompt)

print(response.text)


# In[66]:


# Daily total cost
daily_cost = df.groupby("UsageDate")["UnblendedCost"].sum()

daily_cost.plot(figsize=(10,5), title="Daily AWS Cost Trend")


# In[68]:


trend_text = daily_cost.to_string()

prompt = f"""
You are a FinOps expert.

Here is daily AWS total cost data:

{trend_text}

1. Identify increasing or decreasing trends.
2. Detect unusual spikes.
3. Suggest possible causes.
4. Recommend cost stabilization strategies.

keep it short and precise
"""

response = model.generate_content(prompt)
print(response.text)


# In[69]:


#Account-level breakdown

account_summary = (
    df.groupby("LinkedAccount")["UnblendedCost"]
    .sum()
    .sort_values(ascending=False)
)

account_summary


# In[71]:


account_text = account_summary.to_string()

prompt = f"""
Analyze AWS cost by account:

{account_text}

1. Which accounts are highest cost drivers?
2. Suggest governance policies.
3. Recommend tagging strategy improvements.

Keep it short and precise
"""

response = model.generate_content(prompt)
print(response.text)


# In[72]:


prompt = f"""
Give me visual representation of cost analysis by account and another one by services. the representation should easy to undersatnd for the manager 
"""

response = model.generate_content(prompt)
print(response.text)


# In[73]:


import matplotlib.pyplot as plt

account_summary = (
    df.groupby("LinkedAccount")["UnblendedCost"]
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(10,5))
account_summary.plot(kind="bar")

plt.title("AWS Cost by Account")
plt.ylabel("Total Cost ($)")
plt.xlabel("Account")
plt.xticks(rotation=45)
plt.tight_layout()

plt.show()


# In[74]:


service_summary = (
    df.groupby("Service")["UnblendedCost"]
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(10,5))
service_summary.plot(kind="bar")

plt.title("AWS Cost by Service")
plt.ylabel("Total Cost ($)")
plt.xlabel("Service")
plt.xticks(rotation=45)
plt.tight_layout()

plt.show()


# In[75]:


prompt = f"""
Summarize key insights from cost by account and cost by service.
Keep it short and executive-level.
"""

response = model.generate_content(prompt)
print(response.text)


# In[76]:


prompt = f"""
what more insights I should get using gemini and which library should I use to get more details and visual using python
Keep it short and executive-level.
"""

response = model.generate_content(prompt)
print(response.text)


# In[ ]:





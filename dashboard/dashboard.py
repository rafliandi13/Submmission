import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import seaborn as sns
import streamlit as st


sns.set(style='dark')

# Dataset
datetime_cols = ["order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date", "order_estimated_delivery_date", "order_purchase_timestamp", "shipping_limit_date"]
all_df = pd.read_csv("https://raw.githubusercontent.com/rafliandi13/Submmission/refs/heads/master/dashboard/all_data.csv")
all_df.sort_values(by="order_approved_at", inplace=True)
all_df.reset_index(inplace=True)

# Geolocation Dataset
geolocation = pd.read_csv('https://raw.githubusercontent.com/rafliandi13/Submmission/refs/heads/master/dashboard/geolocation.csv')
golocation_df = geolocation.drop_duplicates(subset='customer_unique_id')

data_order_payment = all_df.groupby("payment_type")["product_id"].count().reset_index()
data_order_payment = data_order_payment.rename(columns={"product_id": "products"})
data_order_payment = data_order_payment.sort_values(by="products", ascending=False)
data_order_payment = data_order_payment[data_order_payment['payment_type'] != 'not_defined']
data_order_payment = data_order_payment.head(10);

sum_order_items_df = all_df.groupby("product_category_name_english")["product_id"].count().reset_index()
sum_order_items_df = sum_order_items_df.rename(columns={"product_id": "products"})
sum_order_items_df = sum_order_items_df.sort_values(by="products", ascending=False)
sum_order_items_df = sum_order_items_df.head(10)

sales_by_city = golocation_df.groupby('geolocation_city').size().reset_index(name='total_sales')
sales_by_city['percentage'] = (sales_by_city['total_sales'] / sales_by_city['total_sales'].sum()) * 100
sales_by_city = sales_by_city.sort_values(by='percentage', ascending=False)
top_cities = sales_by_city.head(10)

# Submisison Data Visualization
st.header('E-Commerce Data Visualization')

#Show 
st.subheader("Top City Sales")

fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(top_cities['geolocation_city'], top_cities['percentage'], color='skyblue')

# Menambahkan detail pada plot
ax.set_title('Top 10 Cities by Sales Percentage', fontsize=14)
ax.set_xlabel('City', fontsize=12)
ax.set_ylabel('Percentage of Total Sales (%)', fontsize=12)
ax.set_xticklabels(top_cities['geolocation_city'], rotation=45, fontsize=10)
ax.grid(axis='y', linestyle='--', alpha=0.7)

# Menampilkan grafik dalam aplikasi Streamlit
st.pyplot(fig)

st.subheader("Top Category Sales")
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))

colors = ["#068DA9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x="products", y="product_category_name_english", data=sum_order_items_df.head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Produk paling banyak terjual", loc="center", fontsize=18)
ax[0].tick_params(axis ='y', labelsize=15)

sns.barplot(x="products", y="product_category_name_english", data=sum_order_items_df.sort_values(by="products", ascending=True).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Produk paling sedikit terjual", loc="center", fontsize=18)
ax[1].tick_params(axis='y', labelsize=15)
plt.xticks(rotation=45)
st.pyplot(fig)

st.subheader("Top Payment")
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))

colors = ["#068DA9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x="products", y="payment_type", data=data_order_payment.head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Tipe Pembayaran yang Sering digunakan", loc="center", fontsize=18)
ax[0].tick_params(axis ='y', labelsize=15)

sns.barplot(x="products", y="payment_type", data=data_order_payment.sort_values(by="products", ascending=True).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Tipe Pembayaran yang sedikit digunakan", loc="center", fontsize=18)
ax[1].tick_params(axis='y', labelsize=15)

plt.suptitle("Produk paling banyak dan paling sedikit terjual", fontsize=20)
st.pyplot(fig)

st.caption('Copyright © Rafliandi Ardana 2024')
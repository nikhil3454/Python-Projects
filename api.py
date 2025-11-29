
from flask import Flask, request,jsonify,render_template
from flask_mysqldb import MySQL
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"]='root'
app.config['MYSQL_PASSWORD']='Nikhil rocks@456'
app.config["MYSQL_DB"]='niyam_v2'
mysql=MySQL(app)
CORS(app)

@app.route('/')
def home():
    return  render_template('plot.html')


@app.route('/getsalesbyitem', methods=['GET'])
def top_sales():
    rank=request.args.get('rank')
    if rank:
        rank=int(rank)
    else:
        rank=0    
    cur=mysql.connection.cursor()
    query = "select * from salesindent inner join supplyorder on supplyorder.Supplyorder_idSupplyorder=salesindent.idSupplyorder inner join item on item.item_idItem=salesindent.idItem inner join company on company.idCompany= supplyorder.Company_idCompany;"
    cur.execute(query)
    data=cur.fetchall()
    result=pd.DataFrame(data)
    result.columns=['idIndent','Qty','Supplyorder_idSupplyorder','issuedQty','item_idItem','CreatedBy_idUsers','UnitCost','Linetotal','GST','Total','Supplyorder_idSupplyorder','ProjectName','PONumber','CreatedOn',"Targetdate",'SoCategoryTypes_idSoCategory','CreatedBy_idUsers','Status','Company_idCompany','IsApproved','item_idItem','Item','Stock','Critical','idCategory','ShelfNumber','RackNumber','Description','Blocked','NetStock','LowStockAlertCount','idUnits','IsAssembled','idPackage','manufacturer','hsncode','price','idCompany','Name','Address','PhoneNumber1','PhoneNumber2','ContactName','GSTNumber','EmailId','TranscationType','gstStateCodeId']
    result=result.T.drop_duplicates().T
    result=result[result['IsAssembled']!= 0]
    result["TotalIssuedQty"]=(result.groupby('item_idItem')['issuedQty'].sum().reset_index(drop=True))
    result['total money']=(result.groupby('item_idItem')['Total'].sum().reset_index(drop=True))
    result['Item name']=(result.groupby('item_idItem')['Item'].unique().apply(lambda x:','.join(set(x))).reset_index(drop=True)).astype(str)
    money=result['total money'].sum()
    result['Percentage of sales']=((result['total money']/money)*100).apply(lambda x: '{:,.2f}'.format(x))
    result=result.sort_values(['total money'],ascending=False).reset_index(drop=True)
    final_result= result[['Item name','TotalIssuedQty','total money','Percentage of sales']]
    final_result=final_result.dropna()
    final_result["itemName"]=final_result['Item name'].astype(str)
    final_result['totalIssuedQty']=final_result['TotalIssuedQty'].astype(int)
    final_result['totalMoney']=final_result['total money'].astype(int)
    final_result['itemSalesPercentage']=result['Percentage of sales'].astype(float)
    if rank > 0:
        return jsonify(final_result[['itemName','totalIssuedQty','totalMoney','itemSalesPercentage']].head(rank).to_dict(orient='records'))
    else:
        return jsonify(final_result[['itemName','totalIssuedQty','totalMoney','itemSalesPercentage']].to_dict(orient='records'))  
@app.route('/getsalesbycustomer',methods=['GET'])
def customer():
    cur=mysql.connection.cursor()
    query="select * from salesindent inner join supplyorder on supplyorder.Supplyorder_idSupplyorder=salesindent.idSupplyorder inner join item on item.item_idItem=salesindent.idItem inner join company on company.idCompany= supplyorder.Company_idCompany;"
    cur.execute(query)
    data=cur.fetchall()
    result=pd.DataFrame(data)
    result.columns=['idIndent','Qty','Supplyorder_idSupplyorder','issuedQty','item_idItem','CreatedBy_idUsers','UnitCost','Linetotal','GST','Total','Supplyorder_idSupplyorder','ProjectName','PONumber','CreatedOn',"Targetdate",'SoCategoryTypes_idSoCategory','CreatedBy_idUsers','Status','Company_idCompany','IsApproved','item_idItem','Item','Stock','Critical','idCategory','ShelfNumber','RackNumber','Description','Blocked','NetStock','LowStockAlertCount','idUnits','IsAssembled','idPackage','manufacturer','hsncode','price','idCompany','Name','Address','PhoneNumber1','PhoneNumber2','ContactName','GSTNumber','EmailId','TranscationType','gstStateCodeId']
    result=result.T.drop_duplicates().T
    result=result[result['IsAssembled']!= 0]
    grouped= result.groupby(['Company_idCompany','item_idItem'])
    result['Customer']=result.groupby("Company_idCompany")['Name'].apply(lambda x: ','.join(set(x))).reset_index(drop=True)
    result['customer']=grouped['Name'].apply(lambda x: ', '.join(set(x))).reset_index(drop=True).astype(str)
    result['itemIssuedToCustomer']=result.groupby('Company_idCompany')['Item'].apply(lambda x: ', '.join(set(x))).reset_index(drop=True)
    result['itemName']=grouped['Item'].unique().apply(lambda x: ', '.join(set(x))).reset_index(drop=True).astype(str)
    result['quantity'] = grouped['issuedQty'].sum().reset_index(drop=True)
    result['unitCost']=grouped['UnitCost'].sum().reset_index(drop=True)
    result['totalPrice']=grouped['Total'].sum().reset_index(drop=True)
    result['Total_price']=result.groupby('Company_idCompany')['Total'].sum().reset_index(drop=True)
    total_price=result['Total_price'].sum()
    result['percentage']=((result['Total_price']/total_price)*100).apply(lambda x: '{:,.2f}'.format(x)).astype(float)
    result['itemIssuedToCustomer']=result['itemIssuedToCustomer'].astype(str)
    result['itemName']=result['itemName'].astype(str)
    result=result.reset_index(drop=True)
    unique_customers = result['Customer'].unique().astype(str)
    customer_percentage_dict=result['percentage'].loc[0:49].astype(str).to_dict()
    customer_data = [
    {
        "customerName": customer,
        "items": result[result['customer'] == customer][['itemName', 'quantity','totalPrice']].to_dict('records'),
        "customerSalesPercentage": customer_percentage_dict.get(index,None)
    }
    
    for index,customer in enumerate(unique_customers)]

    output_dict = customer_data; #  {"getsalesbycustomer": customer_data}'''
    return jsonify(output_dict)
@app.route('/getsalesbymonth', methods=['GET'])
def monthly():
    start = request.args.get('start')
    end = request.args.get('end')

    # Validate input dates
    if not start or not end:
        return jsonify({'error': 'Please provide start and end dates'}), 400

    try:
        start = datetime.strptime(start, '%Y-%m-%d')
        end = datetime.strptime(end, '%Y-%m-%d')
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400

    # Connect to MySQL
    cur = mysql.connection.cursor()
    query = """ 
    SELECT * FROM salesindent 
    INNER JOIN supplyorder ON supplyorder.Supplyorder_idSupplyorder = salesindent.idSupplyorder 
    INNER JOIN item ON item.item_idItem = salesindent.idItem 
    INNER JOIN company ON company.idCompany = supplyorder.Company_idCompany 
    WHERE supplyorder.CreatedOn BETWEEN %s AND %s;
    """
    cur.execute(query, (start, end))
    data = cur.fetchall()

    # Check if data is empty
    if not data:
        return jsonify({'error': 'No sales data found for the given date range'}), 404

    # Convert to DataFrame
    result = pd.DataFrame(data)
    result.columns = ['idIndent', 'Qty', 'idSupplyorder', 'issuedQty', 'idItem', 'createdby_idUsers', 
                      'UnitCost', 'LineTotal', 'Gst', 'Total', 'Supplyorder_idSupplyorder', 'ProjectName', 
                      'PONumber', 'CreatedOn', 'TargetDate', 'SoCategoryTypes_idSoCategory', 'CreatedBy_idUsers', 
                      'Status', 'Company_idCompany', 'IsApproved', 'item_idItem', 'Item', 'Stock', 'Critical', 
                      'idCategory', 'ShelfNumber', 'RackNumber', 'Description', 'Blocked', 'NetStock', 
                      'LowStockAlertCount', 'idUnits', 'IsAssembled', 'idPackage', 'manufacturer', 'hsncode', 
                      'price', 'idCompany', 'Name', 'Address', 'PhoneNumber1', 'PhoneNumber2', 'ContactName', 
                      'GSTNumber', 'EmailId', 'TransactionType', 'gstStateCodeId']

    # Filter out non-assembled items
    result = result[result["IsAssembled"] != 0].reset_index(drop=True)

    # Convert 'CreatedOn' to datetime
    result['CreatedOn'] = pd.to_datetime(result['CreatedOn'])
    result['month'] = result['CreatedOn'].dt.strftime('%B')
    result['Year'] = result['CreatedOn'].dt.year

    # Aggregate sales data
    summary = result.groupby(['Year', 'month', 'item_idItem', 'Item']).agg({
        'issuedQty': 'sum',
        'Total': 'sum'
    }).reset_index()

    # Define month order
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                   'July', 'August', 'September', 'October', 'November', 'December']

    # Build JSON response
    result_json = []
    years = summary['Year'].unique()

    for year in years:
        year_data = {'Year': int(year), 'months': []}
        months = summary[summary['Year'] == year]['month'].unique()
        months = sorted(months, key=lambda x: month_order.index(x))

        for month in months:
            month_data = {'month': month, 'totalPrice': 0, 'totalMonthSales': [], 'percentage': 0}
            items = summary[(summary['Year'] == year) & (summary['month'] == month)]
            total_price = items['Total'].sum()

            # Prevent division by zero
            total_year_price = summary[summary['Year'] == year]['Total'].sum()
            percentage = (total_price / total_year_price) * 100 if total_year_price else 0

            month_data['totalPrice'] = int(total_price)
            month_data['percentage'] = float(percentage)

            for _, row in items.iterrows():
                month_data['totalMonthSales'].append({
                    'item': row['Item'],
                    'quantity': int(row['issuedQty']),
                    'price': int(row['Total'])
                })

            year_data['months'].append(month_data)
        result_json.append(year_data)

    return jsonify(result_json)

@app.route("/getsalesformonth",methods=['GET'])
def sales():
    year=request.args.get('year')
    month=request.args.get('month')
    if not year or not  month:
        return jsonify({'error':'please provide the year and month '}),400
    try:
        start_datetime = datetime.strptime(f'{year} {month}', '%Y %B')
    except ValueError:
        return jsonify({'error': 'Invalid year or month format. Use YYYY for year and full month name for month (e.g., 2025 February)'}), 400
    
    cur = mysql.connect.cursor()
    query = "SELECT * FROM salesindent INNER JOIN supplyorder ON supplyorder.Supplyorder_idSupplyorder = salesindent.idSupplyorder INNER JOIN item ON item.item_idItem = salesindent.idItem INNER JOIN company ON company.idCompany = supplyorder.Company_idCompany WHERE YEAR(supplyorder.CreatedOn) = %s AND MONTHNAME(supplyorder.CreatedOn) = %s ;"
    cur.execute(query,(year,month))
    data = cur.fetchall()
    cur.close()
    if len(data)==0:
        return jsonify({'error':'No data found for the given year and month'}),404

    result = pd.DataFrame(data)
    result.columns = ['idIndent', 'Qty', 'idSupplyorder', 'issuedQty', 'idItem', 'createdby_idUsers', 'UnitCost', 'LineTotal', 'Gst', 'Total', 'Supplyorder_idSupplyorder', 'ProjectName', 'PONumber', 'CreatedOn', 'TargetDate', 'SoCategoryTypes_idSoCategory', 'CreatedBy_idUsers', 'Status', 'Company_idCompany', 'IsApproved', 'item_idItem', 'Item', 'Stock', 'Critical', 'idCategory', 'ShelfNumber', 'RackNumber', 'Description', 'Blocked', 'NetStock', 'LowStockAlertCount', 'idUnits', 'IsAssembled', 'idPackage', 'manufacturer', 'hsncode', 'price', 'idCompany', 'Name', 'Address', 'PhoneNumber1', 'PhoneNumber2', 'ContactName', 'GSTNumber', 'EmailId', 'TransactionType', 'gstStateCodeId']
    result = result[result["IsAssembled"] != 0]
    result = result.reset_index(drop=True)
    result['CreatedOn'] = pd.to_datetime(result['CreatedOn'])
    result['month'] = result['CreatedOn'].dt.strftime('%B')
    result['Year'] = result['CreatedOn'].dt.year
    summary = result.groupby(['Year', 'month', 'item_idItem', 'Item']).agg({
        'issuedQty': 'sum',
        'Total': 'sum'
    }).reset_index()
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    # Create JSON structure
    result_json = []
    years = summary['Year'].unique()
    for year in years:
        year_data = {'Year': int(year),'month':month, 'salesInfo':[]}
        months = summary[summary['Year'] == year]['month'].unique()
        months = sorted(months, key=lambda x: month_order.index(x))
        for month in months:
            month_data = { 'totalPrice': 0, 'Items': []}
            items = summary[(summary['Year'] == year) & (summary['month'] == month)]
            total_price = items['Total'].sum()
            month_data['totalPrice'] = int(total_price)
            denominator = summary[summary['Year'] == year]['Total'].sum()  
            if denominator == 0:  
              percentage = 0  # or handle the error as needed  
            else:  
                percentage = (total_price / denominator) * 100 
            month_data['percentage'] = float(percentage)
            for _, row in items.iterrows():
                month_data['Items'].append({
                    'item': row['Item'],
                    'quantity': int(row['issuedQty']),
                    'price': int(row['Total'])
                })
            year_data['salesInfo'].append(month_data)
        result_json.append(year_data)

    return jsonify(result_json)  
@app.route('/getsalesbyitemid')
def itemId():
    year=request.args.get('year')
    itemId=request.args.get('itemId')
    if not year and not itemId:
        return jsonify({'error':'please provide the year and itemid '})
    try:
        year=datetime.strptime(year,'%Y')
        itemId=int(itemId)
    except ValueError:
            return jsonify({'error': 'Invalid year or item_id format. Use a valid integer for year and item_id'}), 400
    
    cur = mysql.connect.cursor()
    query = """
    SELECT *
    FROM salesindent
    INNER JOIN supplyorder ON supplyorder.Supplyorder_idSupplyorder = salesindent.idSupplyorder
    INNER JOIN item ON item.item_idItem = salesindent.idItem
    INNER JOIN company ON company.idCompany = supplyorder.Company_idCompany
    WHERE YEAR(supplyorder.CreatedOn) = %s
    AND item.item_idItem = %s;  """         
    cur.execute(query,(year,itemId)) 
    data=cur.fetchall()
    cur.close()
    if len(data)==0:
        return jsonify({'error':'No data found for the given year and item'}),400
    result=pd.DataFrame(data)
    result.columns = ['idIndent', 'Qty', 'idSupplyorder', 'issuedQty', 'idItem', 'createdby_idUsers', 'UnitCost', 'LineTotal', 'Gst', 'Total', 'Supplyorder_idSupplyorder', 'ProjectName', 'PONumber', 'CreatedOn', 'TargetDate', 'SoCategoryTypes_idSoCategory', 'CreatedBy_idUsers', 'Status', 'Company_idCompany', 'IsApproved', 'item_idItem', 'Item', 'Stock', 'Critical', 'idCategory', 'ShelfNumber', 'RackNumber', 'Description', 'Blocked', 'NetStock', 'LowStockAlertCount', 'idUnits', 'IsAssembled', 'idPackage', 'manufacturer', 'hsncode', 'price', 'idCompany', 'Name', 'Address', 'PhoneNumber1', 'PhoneNumber2', 'ContactName', 'GSTNumber', 'EmailId', 'TransactionType', 'gstStateCodeId']
    result = result[result["IsAssembled"] != 0]
    result['CreatedOn'] = pd.to_datetime(result['CreatedOn'])
    result['month'] = result['CreatedOn'].dt.strftime('%B')
    result['Year'] = result['CreatedOn'].dt.year
    result['CreatedOn']=result['CreatedOn'].dt.strftime('%Y-%m-%d')
    summary = result.groupby(['Year', 'month', 'item_idItem', 'Item','CreatedOn']).agg({
        'issuedQty': 'sum',
        'Total': 'sum'
    }).reset_index()
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    result_json=[]
    items=summary['item_idItem'].unique()
    for item in items:
         item_data = {
            'itemId': int(item),
            'Item': summary[summary['item_idItem'] == item]['Item'].values[0],
            'itemInfo': []
        }
    item_summary = summary[summary['item_idItem'] == item]
    months = item_summary['month'].unique()
    months = sorted(months, key=lambda x: month_order.index(x))
    for month in months:
            month_data = {
                'month':month,               
                'salesInfo': [],
            }
            month_summary = item_summary[item_summary['month'] == month]
            for _, row in month_summary.iterrows():
                detail_info = {
                    'Date': str(row['CreatedOn']),
                    'quantity': int(row['issuedQty']),
                    'totalPrice': int(row['Total'])
                }
                month_data['salesInfo'].append(detail_info)
            item_data['itemInfo'].append(month_data)
    result_json.append(item_data)
    return jsonify(result_json)
@app.route('/getyearlysalesforcustomer')
def company():
    year=request.args.get('year')
    customerId=request.args.get('customerId')
    if not year or not customerId:
        return jsonify({'error':'please provide the necessary details'})
    try:
        year=datetime.strptime(year,'%Y')  
        customerId=int(customerId)
    except ValueError:
        return jsonify({'error':'Invalid year or customerId format.Please provide the year in YYYY format and a valid integer for customerId '})     
    cur=mysql.connection.cursor()
    query="""
    SELECT *
    FROM salesindent
    INNER JOIN supplyorder ON supplyorder.Supplyorder_idSupplyorder = salesindent.idSupplyorder
    INNER JOIN item ON item.item_idItem = salesindent.idItem
    INNER JOIN company ON company.idCompany = supplyorder.Company_idCompany
    WHERE YEAR(supplyorder.CreatedOn) = %s
    AND company.idCompany = %s; """
    cur.execute(query,(year,customerId))
    data=cur.fetchall()
    cur.close()
    if len(data)==0:
        return jsonify({'error':'No data found for the given year and customerId'}),400
    result=pd.DataFrame(data)
    result.columns=['idIndent', 'Qty', 'idSupplyorder', 'issuedQty', 'idItem', 'createdby_idUsers', 'UnitCost', 'LineTotal', 'Gst', 'Total', 'Supplyorder_idSupplyorder', 'ProjectName', 'PONumber', 'CreatedOn', 'TargetDate', 'SoCategoryTypes_idSoCategory', 'CreatedBy_idUsers', 'Status', 'Company_idCompany', 'IsApproved', 'item_idItem', 'Item', 'Stock', 'Critical', 'idCategory', 'ShelfNumber', 'RackNumber', 'Description', 'Blocked', 'NetStock', 'LowStockAlertCount', 'idUnits', 'IsAssembled', 'idPackage', 'manufacturer', 'hsncode', 'price', 'idCompany', 'Name', 'Address', 'PhoneNumber1', 'PhoneNumber2', 'ContactName', 'GSTNumber', 'EmailId', 'TransactionType', 'gstStateCodeId']
    result=result[result['IsAssembled']!=0]
    result['CreatedOn'] = pd.to_datetime(result['CreatedOn'])
    result['month'] = result['CreatedOn'].dt.strftime('%B')
    result['Year'] = result['CreatedOn'].dt.year
    result['CreatedOn'] = result['CreatedOn'].dt.strftime('%Y-%m-%d')
    
    summary = result.groupby(['Year', 'month', 'idCompany', 'Name', 'item_idItem', 'Item', 'CreatedOn']).agg({
        'issuedQty': 'sum',
        'Total': 'sum'
    }).reset_index()
    
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    
    result_json = []
    customers = summary['idCompany'].unique()
    for customer in customers:
        customer_data = {
            'customer': summary[summary['idCompany'] == customer]['Name'].values[0],
            'salesInfo': []
        }
        customer_summary = summary[summary['idCompany'] == customer]
        months = customer_summary['month'].unique()
        months = sorted(months, key=lambda x: month_order.index(x))
        
        for month in months:
            month_data = {
                'month': month,
                'itemInfo': []
            }
            month_summary = customer_summary[customer_summary['month'] == month]
            
            for _, row in month_summary.iterrows():
                detail_info = {
                    'item': row['Item'],
                    'Date': str(row['CreatedOn']),
                    'quantity': int(row['issuedQty']),
                    'totalPrice': int(row['Total'])
                }
                month_data['itemInfo'].append(detail_info)
            customer_data['salesInfo'].append(month_data)
        result_json.append(customer_data)
    
    return jsonify(result_json) 
@app.route("/getPurchaseByItem")
def purchase():
    year = request.args.get('year')
    itemId = request.args.get('itemId')

    if not year and not itemId:
        return jsonify({'error':'please provide the year and itemId '}), 400
    try:
        year = datetime.strptime(year, '%Y')
        itemId = int(itemId)
    except ValueError:
        return jsonify({'error': 'Invalid year or item_id format. Use a valid integer for year and item_id'}), 400

    cur = mysql.connect.cursor()
    query = """
    SELECT *
    FROM purchaseindent
    INNER JOIN poitems ON poitems.PI_idPurchaseIndent = purchaseindent.idPurchaseIndent
    INNER JOIN item ON item.item_idItem = purchaseindent.item_idItem
    INNER JOIN purchaseorder ON purchaseorder.idPurchaseOrder = poitems.PO_idPurchaseOrder
    WHERE YEAR(purchaseindent.Date) = %s 
    AND purchaseindent.item_idItem = %s;
    """
    cur.execute(query, (year.year, itemId))
    data = cur.fetchall()
    cur.close()
    
    if len(data) == 0:
        return jsonify({'error':'No data found for the given year and itemId'}), 400
    
    purchase = pd.DataFrame(data)
    purchase.columns = ['idPurchaseIndent', 'Qty', 'Date', 'item_idItem', 'IndentRaisedBy', 'IndentApprovedBy', 'Status', 'Remarks', 
                        'idPoItems', 'PO_idPurchaseOrder', 'PI_idPurchaseIndent', 'Qty_POItems', 'UnitCost', 'LineTotal', 'Gst', 'TotalCost', 
                        'item_idItem_poitems', 'QtyReceived', 'item_idItem_item', 'Partnumber', 'Stock', 'Critical', 'idCategory', 
                        'ShelfNumber', 'RackNumber', 'Description', 'Blocked', 'NetStock', 'LowStockAlertCount', 'idUnits', 'IsAssembled', 
                        'idPackage', 'manufacturer', 'hsncode', 'price', 'idPurchaseOrder', 'DateofIssue', 'IssuedBy', 'PoIssuedTo_idCompany', 'PoNumber', 'Status', 'Remarks', 'IsApproved']
    
    purchase['Date'] = pd.to_datetime(purchase['Date'])
    purchase['month'] = purchase['Date'].dt.strftime('%B')
    purchase['Year'] = purchase['Date'].dt.year
    purchase['Date'] = purchase['Date'].dt.strftime('%Y-%m-%d')
    
    summary = purchase.groupby(['Year', 'month', 'item_idItem', 'Partnumber', 'Date']).agg({
        'Qty': 'sum',
        'TotalCost': 'sum'
    }).reset_index()
    
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    result_json = []
    items = summary['item_idItem'].unique()
    
    for item in items:
        item_data = {
            'itemId': int(item),
            'Partnumber': summary[summary['item_idItem'] == item]['Partnumber'].values[0],
            'itemInfo': []
        }
        
        item_summary = summary[summary['item_idItem'] == item]
        months = item_summary['month'].unique()
        months = sorted(months, key=lambda x: month_order.index(x))
        
        for month in months:
            month_data = {
                'month': month,
                'purchaseInfo': []
            }
            
            month_summary = item_summary[item_summary['month'] == month]
            
            for _, row in month_summary.iterrows():
                detail_info = {
                    'Date': str(row['Date']),
                    'quantity': int(row['Qty']),
                    'totalPrice': float(row['TotalCost'])
                }
                month_data['purchaseInfo'].append(detail_info)
            
            item_data['itemInfo'].append(month_data)
        
        result_json.append(item_data)
    
    return jsonify(result_json)

@app.route('/getMonthlyPurchase')
def monthlytPurchase():
    start=request.args.get('start')
    end=request.args.get('end')
    if not start or not end:
        return jsonify({'error':'Please Provide the required dates for dashboard'}),400
    try:
        start=datetime.strptime(start,'%Y-%m-%d')
        end=datetime.strptime(end,'%Y-%m-%d' )
    except ValueError:
        return jsonify({'error':'invalid format of dates for input.Please provide the input date-range in the format of YYYY-MM-DD'})        
    cur=mysql.connection.cursor()
    query='select * from purchaseindent inner join poitems on poitems.PI_idPurchaseIndent=purchaseindent.idPurchaseindent inner join item on item.item_idItem=purchaseindent.item_idItem inner join purchaseorder on purchaseorder.idPurchaseOrder=poitems.PO_idPurchaseOrder where date(purchaseindent.Date) between %s and %s ;'
    cur.execute(query,(start,end))
    data=cur.fetchall()
    cur.close
    if len(data)==0:
        return jsonify({'error':'No data found for the given Date-Range'})
    purchase=pd.DataFrame(data)
    purchase.columns = ['idPurchaseIndent', 'Qty', 'Date', 'item_idItem', 'IndentRaisedBy', 'IndentApprovedBy', 'Status', 'Remarks', 
                        'idPoItems', 'PO_idPurchaseOrder', 'PI_idPurchaseIndent', 'Qty_POItems', 'UnitCost', 'LineTotal', 'Gst', 'TotalCost', 
                        'item_idItem_poitems', 'QtyReceived', 'item_idItem_item', 'Partnumber', 'Stock', 'Critical', 'idCategory', 
                        'ShelfNumber', 'RackNumber', 'Description', 'Blocked', 'NetStock', 'LowStockAlertCount', 'idUnits', 'IsAssembled', 
                        'idPackage', 'manufacturer', 'hsncode', 'price','idPurchaseOrder','DateofIssue','IssuedBy','PoIssuedTo_idCompany','PoNumber','Status','Remarks','IsApproved']
    # Convert 'Date' to datetime
    purchase['Date'] = pd.to_datetime(purchase['Date'])
    purchase['month'] = purchase['Date'].dt.strftime('%B')
    purchase['Year'] = purchase['Date'].dt.year

    # Aggregate purchase data
    summary = purchase.groupby(['Year', 'month', 'item_idItem', 'Partnumber']).agg({
        'Qty_POItems': 'sum',
        'TotalCost': 'sum'
    }).reset_index()

    # Define month order
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                   'July', 'August', 'September', 'October', 'November', 'December']

    # Build JSON response
    result_json = []
    years = summary['Year'].unique()

    for year in years:
        year_data = {'Year': int(year), 'months': []}
        months = summary[summary['Year'] == year]['month'].unique()
        months = sorted(months, key=lambda x: month_order.index(x))

        for month in months:
            month_data = {'month': month, 'totalCost': 0, 'totalMonthPurchases': [], 'percentage': 0}
            items = summary[(summary['Year'] == year) & (summary['month'] == month)]
            total_cost = items['TotalCost'].sum()

            # Prevent division by zero
            total_year_cost = summary[summary['Year'] == year]['TotalCost'].sum()
            percentage = (total_cost / total_year_cost) * 100 if total_year_cost else 0

            month_data['totalCost'] = int(total_cost)
            month_data['percentage'] = float(percentage)

            for _, row in items.iterrows():
                month_data['totalMonthPurchases'].append({
                    'item': row['Partnumber'],
                    'quantity': int(row['Qty_POItems']),
                    'cost': int(row['TotalCost'])
                })

            year_data['months'].append(month_data)
        result_json.append(year_data)

    return jsonify(result_json) 
@app.route('/getPurchaseOfCustomer')
def Id():
    year=request.args.get('year')
    customerId=request.args.get('customerId')
    if not year or not customerId:
        return({'error':'Please Provide the required year and customerId'}),400
    try:
        year=datetime.strptime(year,"%Y")
        customerId=int(customerId)
    except ValueError:
        return jsonify({'error':'Invalid year or customerId format. Use YYYY 00 format'}), 400
    cur=mysql.connection.cursor()
    query='select * from purchaseindent inner join poitems on poitems.PI_idPurchaseIndent=purchaseindent.idPurchaseindent inner join item on item.item_idItem=purchaseindent.item_idItem inner join purchaseorder on purchaseorder.idPurchaseOrder=poitems.PO_idPurchaseOrder inner join company on company.idCompany=purchaseorder.PoIssuedTo_idCompany where year(purchaseindent.Date)=%s and purchaseorder.PoIssuedTo_idCompany=%s;'
    cur.execute(query,(year,customerId))
    data=cur.fetchall()
    if len(data)==0:
        return({'error':'No data found for the given year and customerId'})
    purchase=pd.DataFrame(data)
    purchase.columns=['idPurchaseIndent', 'Qty', 'Date', 'item_idItem', 'IndentRaisedBy', 'IndentApprovedBy', 'Status', 'Remarks', 
                        'idPoItems', 'PO_idPurchaseOrder', 'PI_idPurchaseIndent', 'Qty_POItems', 'UnitCost', 'LineTotal', 'Gst', 'TotalCost', 
                        'item_idItem_poitems', 'QtyReceived', 'item_idItem_item', 'Partnumber', 'Stock', 'Critical', 'idCategory', 
                        'ShelfNumber', 'RackNumber', 'Description', 'Blocked', 'NetStock', 'LowStockAlertCount', 'idUnits', 'IsAssembled', 
                        'idPackage', 'manufacturer', 'hsncode', 'price','idPurchaseOrder','DateofIssue','IssuedBy','PoIssuedTo_idCompany','PoNumber','Status','Remarks','IsApproved','idCompany','Name','Address','Phonenumber1','PhoneNumber2','ContactName','GSTNumber','EmailId','TransactionType','gstStateCodeId']
    purchase['Date'] = pd.to_datetime(purchase['Date'])
    purchase['month'] = purchase['Date'].dt.strftime('%B')
    purchase['Year'] = purchase['Date'].dt.year
    purchase['Date'] = purchase['Date'].dt.strftime('%Y-%m-%d')

    # Aggregate purchase data
    summary = purchase.groupby(['Year', 'month', 'idCompany', 'Name', 'item_idItem', 'Partnumber', 'Date']).agg({
        'Qty_POItems': 'sum',
        'TotalCost': 'sum'
    }).reset_index()

    # Define month order
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    # Construct JSON response
    result_json = []
    customers = summary['idCompany'].unique()

    for customer in customers:
        customer_data = {
            'customer': summary.loc[summary['idCompany'] == customer, 'Name'].values[0],
            'purchaseInfo': []
        }
        customer_summary = summary[summary['idCompany'] == customer]
        months = sorted(customer_summary['month'].unique(), key=lambda x: month_order.index(x))

        for month in months:
            month_data = {
                'month': month,
                'itemInfo': []
            }
            month_summary = customer_summary[customer_summary['month'] == month]

            for _, row in month_summary.iterrows():
                month_data['itemInfo'].append({
                    'item': row['Partnumber'],
                    'Date': row['Date'],
                    'quantity': int(row['Qty_POItems']),
                    'totalPrice': float(row['TotalCost'])
                })

            customer_data['purchaseInfo'].append(month_data)

        result_json.append(customer_data)

    return jsonify(result_json)
'''@app.route('/getMonthlySupplier')
def supplier():
    start_date=request.args.get('StartDate')
    end_date=request.args.get('EndDate')
    if not start_date or not end_date:
        return jsonify({'error':'Please Provide the required dates for dashboard'}),400
    try:
        start_date=datetime.strptime(start_date,'%Y-%m-%d')
        end_date=datetime.strptime(end_date,'%Y-%m-%d')
    except ValueError:
        return jsonify({'error':'invalid format of dates for input.Please provide the input date-range in the format of YYYY-MM-DD'})
    cur=mysql.connection.cursor()
    query=''
    cur.execute(query,(start_date,end_date))    
    data=cur.execute(query,(start_date,end_date))
    if len(data)==0:'''


if __name__ == '__main__':
    app.run(debug=True)

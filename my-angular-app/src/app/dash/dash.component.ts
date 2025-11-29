import { Component, OnInit, ViewChild, AfterViewInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { MatDatepicker } from '@angular/material/datepicker';
import * as moment from 'moment';
import { EChartsOption } from 'echarts';
import { MatTableDataSource } from '@angular/material/table';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import { FormControl } from '@angular/forms';

@Component({
    selector: 'app-dash',
    templateUrl: './dash.component.html',
    styleUrls: ['./dash.component.css']
})
export class DashComponent implements OnInit, AfterViewInit {
    startDate1: Date | null = null;
    endDate1: Date | null = null;
    startDate2: Date | null = null;
    endDate2: Date | null = null;
    chartOptions1: EChartsOption = {};
    chartOptions2: EChartsOption = {};// Initialized with empty object
    chartOptions3: EChartsOption = {};
    barChartOptions1: EChartsOption = {};
    barChartOptions2: EChartsOption = {}; // Initialized with empty object
    pieChartOptions1: EChartsOption = {};
    pieChartOptions2: EChartsOption = {} // Initialized with empty object
    totalSales1: number = 0;
    totalPurchase: number = 0;
    totalRevenue: number = 0;
    monthlyAverageSales: number = 0;
    monthlyAveragePurchase: number = 0;
    displayedColumns1: string[] = ['month', 'item', 'quantity', 'price'];
    dataSource1 = new MatTableDataSource<any>([]);
    displayedColumns2: string[] = ['month', 'item', 'price', 'quantity'];
    dataSource2 = new MatTableDataSource<any>([]);
    displayedColumns3: string[] = ['month', 'item', 'price', 'quantity'];
    dataSource3 = new MatTableDataSource<any>([]);


    @ViewChild('paginator1') paginator1!: MatPaginator;
    @ViewChild(MatSort) sort1!: MatSort;
    @ViewChild('paginator2') paginator2!: MatPaginator;
    @ViewChild(MatSort) sort2!: MatSort;
    @ViewChild('paginator3') paginator3!: MatPaginator;
    @ViewChild(MatSort) sort3!: MatSort;

    // Second Dashboard Variables
    yearControl = new FormControl('');
    selectedYear: string = '';
    selectedKeyControl = new FormControl();
    selectedValue: any = null;

    predefinedData: { [key: string]: any } = {
        "Instrutel Systems Pvt. Ltd.": 1,
        "Zetatek Technologies Private Limited": 11,
        "SAMBHAV ELECTRONIC": 12,
        "Voltrio Solutions": 13,
        "N K Square Solutions India Pvt Ltd": 14,
        "Powertest Global Pvt. Ltd.": 15,
        "ABN Electree": 16,
        "HDL-iV": 31,
        "Gold Pharam Pvt Ltd": 32,
        "Icon Devices": 33,
        "Alfa Electronic Components": 34,
        "Shreya Ex-Tech Pvt Ltd": 35,
        "MS Technologies": 36,
        "Element14": 37,
        "Wurth Electronics Services India Pvt Ltd": 38,
        "Sunrom Electronics": 39,
        "HIMMEL TECHNOLOGIES PRIVATE LIMITED": 40,
        "Harsh Automation": 41,
        "RAPID TECHNOLOGIES": 42,
        "ONYX COMPONENTS & SYSTEMS PVT LTD": 43,
        "Kiran Electronics": 44,
        "EdgeFx Technologies Pvt Ltd": 45,
        "STABILITY AUTOMATION": 46,
        "Hindys Lab Private Limited": 47,
        "Aver Electrotech": 48,
        "Jayadeep Enterprises": 49,
        "Laxmi Marketing": 50,
        "Sri Sitarameshwar industries": 51,
        "Naaz Industrial Components": 52,
        "Shikhara Pvt. Ltd.": 53,
        "GU IMPEX": 54,
        "LIBRA COMPUTERS": 55,
        "BALAJI ACTION BUILDWELL PVT LTD": 56,
        "EMATION": 57,
        "GAJJAR ENTERPRISE": 58,
        "Xpress Digital Labels": 59,
        "Fuel Instruments and Engineers Pvt Ltd": 61,
        "Hetero Drugs Unit-1": 62,
        "Controlytics AI Private Limited": 63,
        "Prasad Electronics": 64,
        "Niharad Solutions": 65,
        "Advance Engineers India Pvt. ltd": 66,
        "MJ Homes": 67,
        "V-AXIS Automation Solutions": 68,
        "Digital Curve IT Solution": 69,
        "Exide Industries": 70,
        "Varun Industries": 71,
        "V3NOVUS PVT LTD": 72,
        "Harihi Ohm Electronics": 73,
        "Skylark Embedded Systems": 74,
        "Autosys Engineering and Services": 75,
        "AP Vibration Analysis & Engineering Services": 76,
        "Amzon Fulfilment Center": 77,
        "SMART ELECTRONICS": 78,
        "Orbit Technologies Pvt Ltd": 79,
        "Aqtronics Technologies":80,
        "APEX METER & CONTROLS": 81,
        "Exide Industries Limited": 83,
        "Krishna Sticker Palace": 84,
        "NK Square Solution": 85,
        "Shyam Electronics Wire Centre": 86,
        "515 Army Base": 87,
        "Leadcog Engineering Systems": 88,
        "Advika Enterprises": 89,
        "Robu.in": 91,
        "METRIX AUTOMATIONS INDIA PRIVATE LIMITED": 92,
        "ESS GEE Electronics": 93,
        "V3 Novus Pvt Ltd": 94,
        "Keynote Engineering Solutions": 95,
        "San Telequip Private Limited": 96,
        "Jydin Enetrprises": 97,
        "SRFS Teleinfra": 98,
        "RMES India Pvt Ltd": 99,
        "Kemptronix": 100,
        "Surbhi Kable & Green Energy": 101,
        "Sree Sreenidhi Engineering": 102,
        "TOOLFIT": 103,
        "Nitin Kumar": 104,
        "54 Armoured Regiment": 105,
        "Shahima Plastics": 106,
        "511 AD REGTT": 107,
        "Ashok Enterprise": 108,
        "Well Contacts Co": 109,
        "KRISHNA PRASAD VENKAT ALURI": 110,
        "MVS ACMEI TECHNOLOGIES PVT. LTD.": 111,
        "Maakrupa Scientific Industries Pvt Ltd": 112,
        "Shanmukha Enterprises": 113,
        "Antara Technologies": 114,
        "SUN STAR TECHNOLOGIES": 115,
        "Robokits India": 116,
        "Structural Solutions Private Limited": 117,
        "Roland Electronics": 119,
        "ARS Engineering": 120,
        "VGCON SYSTEMS PVT LTD": 122,
        "ENVOYS ELECTRONICS PVT LTD": 123,
        "Sylab Private Limited": 124,
        "Mouser Electronics": 125,
        "Hikimi Enterprises": 126
    };
    predefinedKeys = Object.keys(this.predefinedData)

    constructor(private http: HttpClient
    ) { }
    ngOnInit(): void {
    }

    ngAfterViewInit() {
        this.dataSource1.paginator = this.paginator1;
        this.dataSource1.sort = this.sort1;
        this.dataSource2.paginator = this.paginator2;
        this.dataSource2.sort = this.sort2;
        this.dataSource3.paginator = this.paginator3;
        this.dataSource3.sort = this.sort3;

    }

    chosenYearHandler1(normalizedYear: moment.Moment) {
        const ctrlValue = moment();
        ctrlValue.year(normalizedYear.year());
        this.startDate1 = ctrlValue.startOf('year').toDate();
    }

    chosenMonthHandler1(normalizedMonth: moment.Moment, datepicker: MatDatepicker<any>) {
        const ctrlValue = moment();
        ctrlValue.year(this.startDate1!.getFullYear());
        ctrlValue.month(normalizedMonth.month());
        this.startDate1 = ctrlValue.startOf('month').toDate();
        this.endDate1 = ctrlValue.endOf('month').toDate();
        datepicker.close();
        this.fetchData();
    }

    fetchData() {
        if (!this.startDate1 || !this.endDate1) {
            alert('Please select a date range for Chart 1');
            return;
        }
        const params = {
            start: this.startDate1.toISOString().split('T')[0],
            end: this.endDate1.toISOString().split('T')[0],
        };
        this.http.get('http://127.0.0.1:5000/getsalesbymonth', { params }).subscribe(
            (data: any) => {
                this.updateChart(data);
                this.updateBarChart(data);
                this.updatePieChart(data);
                this.calculateTotalSales(data);
                this.calculateMonthlyAverageSales(data);
                this.populateDataTable(data);// New method to populate the data table
            },
            (error) => {
                console.error('Error fetching data from API', error);
                if (error.status === 404) {
                    alert('No data found for the selected date range.');
                } else {
                    alert('Error fetching data, please try again later.');
                }
            }
        );

    }
    populateDataTable(data: any) {
        const tableData1: { month: string; item: string; price: number; quantity: number }[] = [];
        data.forEach((yearData: any) => {
            yearData.months.forEach((monthData: any) => {
                monthData.totalMonthSales.forEach((sale: any) => {
                    tableData1.push({
                        month: `${monthData.month} ${yearData.Year}`,
                        item: sale.item,
                        price: sale.price,
                        quantity: sale.quantity
                    });
                });
            });
        });
        this.dataSource1.data = tableData1;
        this.dataSource1.paginator = this.paginator1;
        this.dataSource1.sort = this.sort1;
    }
    updateChart(data: any) {
        const monthOrder = [
            'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
            'September', 'October', 'November', 'December'
        ];
        let labels: string[] = [];
        let values: number[] = [];
        data.forEach((yearData: any) => {
            yearData.months.forEach((monthData: any) => {
                labels.push(`${monthData.month} ${yearData.Year}`);
                values.push(monthData.totalPrice);
            });
        });
        const sortedData = labels.map((label, index) => ({ label, value: values[index] }))
            .sort((a, b) => {
                const [monthA, yearA] = a.label.split(' ');
                const [monthB, yearB] = b.label.split(' ');
                const yearDiff = parseInt(yearA) - parseInt(yearB);
                if (yearDiff !== 0) return yearDiff;
                return monthOrder.indexOf(monthA) - monthOrder.indexOf(monthB);
            });
        labels = sortedData.map(d => d.label);
        values = sortedData.map(d => d.value);
        this.chartOptions1 = {
            title: { text: 'Monthly Sales Data' },
            tooltip: { trigger: 'axis' },
            xAxis: { type: 'category', data: labels },
            yAxis: { type: 'value', name: 'Total Sales' },
            series: [{ type: 'line', areaStyle: {}, smooth: true, data: values }]
        };
    }

    updateBarChart(data: any) {
        let itemQuantities: { [key: string]: number } = {};
        data.forEach((yearData: any) => {
            yearData.months.forEach((monthData: any) => {
                monthData.totalMonthSales.forEach((sale: any) => {
                    if (itemQuantities[sale.item]) {
                        itemQuantities[sale.item] += sale.price;
                    } else {
                        itemQuantities[sale.item] = sale.price;
                    }
                });
            });
        });
        const labels = Object.keys(itemQuantities);
        const values = Object.values(itemQuantities);
        this.barChartOptions1 = {
            title: { text: 'Item Quantity Data' },
            tooltip: { trigger: 'axis' },
            xAxis: { type: 'category', data: labels },
            yAxis: { type: 'value', name: 'Total Quantity' },
            series: [{ type: 'bar', data: values }]
        };
    }

    updatePieChart(data: any) {
        let itemQuantities: { [key: string]: number } = {};
        data.forEach((yearData: any) => {
            yearData.months.forEach((monthData: any) => {
                monthData.totalMonthSales.forEach((sale: any) => {
                    if (itemQuantities[sale.item]) {
                        itemQuantities[sale.item] += sale.quantity;
                    } else {
                        itemQuantities[sale.item] = sale.quantity;
                    }
                });
            });
        });
        const labels = Object.keys(itemQuantities);
        const values = Object.values(itemQuantities);
        const totalQuantity = values.reduce((sum, value) => sum + value, 0);
        const pieData = labels.map((label, index) => ({
            value: values[index],
            name: `${label} (${((values[index] / totalQuantity) * 100).toFixed(2)}%)`
        }));

        this.pieChartOptions1 = {
            title: { text: 'Item Quantity Distribution' },
            tooltip: { trigger: 'item' },
            series: [{
                type: 'pie',
                radius: '50%',
                data: pieData,
                emphasis: {
                    itemStyle: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }]
        };
    }

    calculateTotalSales(data: any): void {
        let totalRevenue = 0;
        data.forEach((yearData: any) => {
            yearData.months.forEach((monthData: any) => {
                totalRevenue += monthData.totalPrice;
            });
        });
        this.totalSales1 = totalRevenue;
    }

    calculateMonthlyAverageSales(data: any): void {
        let totalSales = 0;
        let monthCount = 0;
        data.forEach((yearData: any) => {
            yearData.months.forEach((monthData: any) => {
                totalSales += monthData.totalPrice;
                monthCount++;
            });
        });
        this.monthlyAverageSales = monthCount > 0 ? totalSales / monthCount : 0;
    }
    // Second Dashboard Handlers
    // Function to handle year selection
    chosenYearHandler(normalizedYear: moment.Moment, datepicker: MatDatepicker<any>) {
        const selectedYear = moment(normalizedYear).year(); // Get selected year
        this.yearControl.setValue(moment([selectedYear]).toDate()); // Store only the year
        datepicker.close(); // Close datepicker after selection
    }
    onSelectionChange(event: any) {
        const selectedKey = event.value;
        this.selectedValue = this.predefinedData[selectedKey]; // Get the mapped value
        console.log(`Selected Key: ${selectedKey}, Corresponding Value: ${this.selectedValue}`);
    }

    // Fetch Data Based on Selection
    fetchData2() {
        const selectedYear = moment(this.yearControl.value).format('YYYY');
        const selectedCustomerId = this.selectedValue; // Get mapped value from selection

        if (!selectedYear || !selectedCustomerId) {
            alert('Please select both a year and a customer.');
            return;
        }
        const params = {
            year: selectedYear,
            customerId: selectedCustomerId
        };
        this.http.get('http://127.0.0.1:5000/getyearlysalesforcustomer', { params }).subscribe(
            (data: any) => {
                console.log('Data for selected year and customer:', data);
                this.updateChart2(data);
                this.populateDataTable2(data);
                this.CalculateTotalRevenue(data);
            },
            (error) => {
                console.error('Error fetching data from API', error);
                if (error.status === 404) {
                    alert('No data found for the selected year and customer.');
                } else {
                    alert('Error fetching data, please try again later.');
                }
            }
        );
    }

    updateChart2(data: any) {
        let labels: string[] = [];
        let values: number[] = [];
        const dateSalesMap: {
            [key: string]: {
                totalPrice: number;
                items: string[];
                quantities: number[]
            }
        } = {};

        data.forEach((customerData: any) => {
            customerData.salesInfo.forEach((salesData: any) => {
                salesData.itemInfo.forEach((item: any) => {
                    if (dateSalesMap[item.Date]) {
                        dateSalesMap[item.Date].totalPrice += item.totalPrice;
                        dateSalesMap[item.Date].items.push(item.item);
                        dateSalesMap[item.Date].quantities.push(item.quantity);
                    } else {
                        dateSalesMap[item.Date] = {
                            totalPrice: item.totalPrice,
                            items: [item.item],
                            quantities: [item.quantity]
                        };
                    }
                });
            });
        });

        // Sort dates in ascending order
        const sortedDates = Object.keys(dateSalesMap).sort((a, b) => new Date(a).getTime() - new Date(b).getTime());

        labels = sortedDates;
        values = sortedDates.map(date => dateSalesMap[date].totalPrice);

        this.chartOptions2 = {
            title: { text: 'Sales Data Over Time' },
            tooltip: {
                trigger: 'axis',
                formatter: (params: any) => {
                    let dataIndex = params[0].dataIndex;
                    let date = labels[dataIndex];
                    let items = dateSalesMap[date].items.map((item, index) => `${item} (Qty: ${dateSalesMap[date].quantities[index]})`).join('<br/>');
                    let total = dateSalesMap[date].totalPrice;
                    return `Date: ${date}<br/>${items}<br/>Total Sales: ${total}`;
                }
            },
            xAxis: { type: 'category', data: labels, name: 'Date' },
            yAxis: { type: 'value', name: 'Total Sales' },
            series: [{ type: 'line', areaStyle: {}, smooth: true, data: values }]
        };
    }
    populateDataTable2(data: any) {
        const tableData2: { month: string; item: string; price: number; quantity: number }[] = [];
        data.forEach((customerData: any) => {
            customerData.salesInfo.forEach((salesData: any) => {
                salesData.itemInfo.forEach((sale: any) => {
                    tableData2.push({
                        month: `${salesData.month}`,
                        item: sale.item,
                        price: sale.totalPrice,
                        quantity: sale.quantity
                    });
                });
            });
        });

        this.dataSource2.data = tableData2;
        this.dataSource2.paginator = this.paginator2;
        this.dataSource2.sort = this.sort2;
    }
    CalculateTotalRevenue(data: any) {
        let totalRevenue = 0;
        data.forEach((customerData: any) => {
            customerData.salesInfo.forEach((salesData: any) => {
                salesData.itemInfo.forEach((item: any) => {
                    totalRevenue += item.totalPrice;
                });
            });
        });
        this.totalRevenue = totalRevenue; // Update component variable
    }
    // third dashboard controls
    chosenYearHandler2(normalizedYear: moment.Moment) {    
      const ctrlValue = moment();
      ctrlValue.year(normalizedYear.year());
      this.startDate2 = ctrlValue.startOf('year').toDate();
    }
  chosenMonthHandler2(normalizedMonth: moment.Moment, datepicker: MatDatepicker<any>) {
      const ctrlValue = moment();
      ctrlValue.year(this.startDate1!.getFullYear());
      ctrlValue.month(normalizedMonth.month());
      this.startDate2 = ctrlValue.startOf('month').toDate();
      this.endDate2 = ctrlValue.endOf('month').toDate();
      datepicker.close();
      this.fetchData3();  // Call fetchData3 instead of fetchData
  }
  fetchData3() {
      if (!this.startDate2 || !this.endDate2) {
          alert('Please select a date range for Chart 3');
          return;
      }
      const params = {
          start: this.startDate2.toISOString().split('T')[0],
          end: this.endDate2.toISOString().split('T')[0],
      };
      this.http.get('http://127.0.0.1:5000/getMonthlyPurchase', { params }).subscribe(
          (data: any) => {
              this.updateChart3(data);
              this.updateBarChart2(data);
              this.updatePieChart2(data);
              this.calculateTotalPurchase(data);
              this.calculateMonthlyAveragePurchase(data);
              this.populateDataTable3(data);
          },
          (error) => {
              console.error('Error fetching data from API', error);
              if (error.status === 404) {
                  alert('No data found for the selected date range.');
              } else {
                  alert('Error fetching data, please try again later.');
              }
          }
      );
  }
  
  updateChart3(data: any) {
      const monthOrder = [
          'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
          'September', 'October', 'November', 'December'
      ];
      let labels: string[] = [];
      let values: number[] = [];
      data.forEach((yearData: any) => {
          yearData.months.forEach((monthData: any) => {
              labels.push(`${monthData.month} ${yearData.Year}`);
              values.push(monthData.totalCost); // Changed from totalPrice to totalCost
          });
      });
      const sortedData = labels.map((label, index) => ({ label, value: values[index] }))
          .sort((a, b) => {
              const [monthA, yearA] = a.label.split(' ');
              const [monthB, yearB] = b.label.split(' ');
              const yearDiff = parseInt(yearA) - parseInt(yearB);
              if (yearDiff !== 0) return yearDiff;
              return monthOrder.indexOf(monthA) - monthOrder.indexOf(monthB);
          });
      labels = sortedData.map(d => d.label);
      values = sortedData.map(d => d.value);
      this.chartOptions3 = {
          title: { text: 'Monthly Purchase Data' },
          tooltip: { trigger: 'axis' },
          xAxis: { type: 'category', data: labels },
          yAxis: { type: 'value', name: 'Total Purchases' },
          series: [{ type: 'line', areaStyle: {}, smooth: true, data: values }]
      };
  }
  
  updateBarChart2(data: any) {
      let itemQuantities: { [key: string]: number } = {};
      data.forEach((yearData: any) => {
          yearData.months.forEach((monthData: any) => {
              monthData.totalMonthPurchases.forEach((purchase: any) => {
                  if (itemQuantities[purchase.item]) {
                      itemQuantities[purchase.item] += purchase.cost;
                  } else {
                      itemQuantities[purchase.item] = purchase.cost;
                  }
              });
          });
      });
      const labels = Object.keys(itemQuantities);
      const values = Object.values(itemQuantities);
      this.barChartOptions2 = {
          title: { text: 'Item Quantity Data' },
          tooltip: { trigger: 'axis' },
          xAxis: { type: 'category', data: labels },
          yAxis: { type: 'value', name: 'Total Quantity' },
          series: [{ type: 'bar', data: values }]
      };
  }
  
  updatePieChart2(data: any) {
      let itemQuantities: { [key: string]: number } = {};
      data.forEach((yearData: any) => {
          yearData.months.forEach((monthData: any) => {
              monthData.totalMonthPurchases.forEach((purchase: any) => {
                  if (itemQuantities[purchase.item]) {
                      itemQuantities[purchase.item] += purchase.quantity;
                  } else {
                      itemQuantities[purchase.item] = purchase.quantity;
                  }
              });
          });
      });
      const labels = Object.keys(itemQuantities);
      const values = Object.values(itemQuantities);
      const totalQuantity = values.reduce((sum, value) => sum + value, 0);
      const pieData = labels.map((label, index) => ({
          value: values[index],
          name: `${label} (${((values[index] / totalQuantity) * 100).toFixed(2)}%)`
      }));
  
      this.pieChartOptions2 = {
          tooltip: { trigger: 'item' },
          series: [{
              type: 'pie',
              radius: '50%',
              data: pieData,
              emphasis: {
                  itemStyle: {
                      shadowBlur: 10,
                      shadowOffsetX: 0,
                      shadowColor: 'rgba(0, 0, 0, 0.5)'
                  }
              }
          }]
      };
  }
  
  calculateTotalPurchase(data: any): void {
      let totalPurchase = 0;
      data.forEach((yearData: any) => {
          yearData.months.forEach((monthData: any) => {
              totalPurchase += monthData.totalCost; // Changed from totalPrice to totalCost
          });
      });
      this.totalPurchase = totalPurchase;
  }
  
  calculateMonthlyAveragePurchase(data: any): void {
      let totalPurchase = 0;
      let monthCount = 0;
      data.forEach((yearData: any) => {
          yearData.months.forEach((monthData: any) => {
              totalPurchase += monthData.totalCost; // Changed from totalPrice to totalCost
              monthCount++;
          });
      });
      this.monthlyAveragePurchase = monthCount > 0 ? totalPurchase / monthCount : 0;
  }
  
  populateDataTable3(data: any) {
      const tableData3: { month: string; item: string; price: number; quantity: number }[] = [];
      data.forEach((yearData: any) => {
          yearData.months.forEach((monthData: any) => {
              monthData.totalMonthPurchases.forEach((purchase: any) => {
                  tableData3.push({
                      month: `${monthData.month} ${yearData.Year}`,
                      item: purchase.item,
                      price: purchase.cost, // Changed from price to cost
                      quantity: purchase.quantity
                  });
              });
          });
      });
      this.dataSource3.data = tableData3;
      this.dataSource3.paginator = this.paginator3;
      this.dataSource3.sort = this.sort3;
  }
  
}

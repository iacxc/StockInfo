﻿using System;
using System.Collections;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Text;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Media.Animation;
using System.Windows.Navigation;
using System.Windows.Shapes;
using System.Data.SQLite;


namespace Stock_fund
{
    using FundList = ObservableCollection<StockFund>;

    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainPage : Page
    {
        private const string DBPATH = "C:/caiche/Github/StockInfo/stock_fund.db";
        private SQLiteConnection db = null;
        private Hashtable hashFunds = new Hashtable();
        private List<StockCode> codeList;

        public MainPage()
        {
            InitializeComponent();

            db = new SQLiteConnection("Data Source=" + DBPATH);

            codeList = GetCodes();
            lstCode.ItemsSource = codeList;
        }

        private List<StockCode> GetCodes()
        {
            String qrystr = "select code, market_share, name from code";
            db.Open();
            SQLiteCommand command = new SQLiteCommand(qrystr, db);
            SQLiteDataReader reader = command.ExecuteReader();

            List<StockCode> codes = new List<StockCode>();
            while (reader.Read())
            {
                codes.Add(new StockCode()
                {
                    Code = (string)reader["code"],
                    MarketShare = (Int64)reader["market_share"],
                    Name = (string)reader["name"]
                });
            }

            db.Close();

            return codes;
        }

        private FundList GetFundList(StockCode stockCode)
        {
            FundList funds = new FundList();

            String tablename = "T" + stockCode.Code;
            string qrystr = "SELECT date, fund_in, fund_out, fund_net, fund_net / (price * " + 
                             stockCode.MarketShare + ") as percent" +
                             " FROM " + tablename + " ORDER BY date DESC LIMIT 50";

            db.Open();
            SQLiteCommand command = new SQLiteCommand(qrystr, db);
            SQLiteDataReader reader = command.ExecuteReader();

            double totalFunds = 0, totalPer = 0;
            while (reader.Read())
            {
                funds.Insert(0, new StockFund()
                {
                    FundDate = (string)reader["date"],
                    FundIn = (double)reader["fund_in"],
                    FundOut = (double)reader["fund_out"],
                    FundNet = (double)reader["fund_net"],
                    FundPercent = (double)reader["percent"]
                });

                totalFunds += (double)reader["fund_net"];
                totalPer += (double)reader["percent"];
            }
            db.Close();

            if (funds.Count() > 0)
            {
                funds.Add(new StockFund() 
                { 
                    FundDate = "Total",  
                    FundNet = totalFunds, 
                    FundPercent = totalPer 
                });
            }

            return funds;
        }

        private void lstCode_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            StockCode code = (StockCode)lstCode.SelectedItem;

            if (!hashFunds.Contains(code.Code))
            {
                FundList fundList = GetFundList(code);

                hashFunds.Add(code.Code, fundList);
            }

            gridFund.ItemsSource = (FundList)hashFunds[code.Code];
           
        }

        
    }
}

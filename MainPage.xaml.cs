using System;
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
using System.Globalization;

namespace Stock_fund
{
    using FundList = ObservableCollection<StockFund>;

    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainPage : Window
    {
        private const string DBPATH = "C:/caiche/Github/StockInfo/stock_fund.db";
        private SQLiteConnection db = null;
        private Hashtable hashFunds = new Hashtable();
        private List<StockCode> codeList;

        Cursor m_Cursor;

        public MainPage()
        {
            //Properties.Resources.Culture = new CultureInfo("zh-CN");
            InitializeComponent();

            db = new SQLiteConnection("Data Source=" + DBPATH);

            codeList = GetCodes();
            lstCode.ItemsSource = codeList;
        }

        private List<StockCode> GetCodes()
        {
            var qrystr = "select code, name from code";
            db.Open();
            var command = new SQLiteCommand(qrystr, db);
            var reader = command.ExecuteReader();

            var codes = new List<StockCode>();
            while (reader.Read())
            {
                codes.Add(new StockCode()
                {
                    Code = (string)reader["code"],
                    Name = (string)reader["name"]
                });
            }

            db.Close();

            return codes;
        }

        private FundList GetFundList(StockCode stockCode)
        {
            var funds = new FundList();

            var tablename = "funds";
            var qrystr = "SELECT date, fund_in, fund_out, fund_net" +
                                   ", fund_per / 100 as fund_per" + 
                                   ", fund_net / value as percent" +
                             " FROM " + tablename + 
                             " WHERE code = '" + stockCode.Code + "'" +
                             " ORDER BY date DESC LIMIT 50";

            db.Open();
            var command = new SQLiteCommand(qrystr, db);
            var reader = command.ExecuteReader();

            double totalFunds = 0, totalPer = 0;
            while (reader.Read())
            {
                funds.Insert(0, new StockFund()
                {
                    FundDate = (string)reader["date"],
                    FundIn = (double)reader["fund_in"],
                    FundOut = (double)reader["fund_out"],
                    FundNet = (double)reader["fund_net"],
                    TotalPercent = (double)reader["percent"],
                    CurrentPercent=(double)reader["fund_per"]
                });

                totalFunds += (double)reader["fund_net"];
                totalPer += (double)reader["percent"];
            }
            db.Close();

            if (funds.Count() > 0)
            {
                funds.Add(new StockFund() 
                { 
                    FundDate = Properties.Resources.Summary,
                    FundNet = totalFunds, 
                    TotalPercent = totalPer 
                });
            }

            return funds;
        }

        private void lstCode_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            var code = lstCode.SelectedItem as StockCode;

            if (!hashFunds.Contains(code.Code))
            {
                var fundList = GetFundList(code);

                hashFunds.Add(code.Code, fundList);
            }

            gridFund.ItemsSource = hashFunds[code.Code] as FundList;

        }

        private void cmdGrow_Click(object sender, RoutedEventArgs e)
        {
            var widthAni = new DoubleAnimation(
                cmdGrow.ActualWidth,
                gridFund.ActualWidth - cmdExit.ActualWidth - 10,
                TimeSpan.FromSeconds(3));

            widthAni.AutoReverse = true;

            cmdGrow.BeginAnimation(Button.WidthProperty, widthAni);
        }

        private void lstCode_MouseDoubleClick(object sender, MouseButtonEventArgs e)
        {
            var code = lstCode.SelectedItem as StockCode;
            var data = StockData.GetData(code.Code);

            if (data != null)
            {
                var w = new StockDetailWin();
                w.SetDataSource(data);

                w.Show();
            }
        }

        private void Window_MouseLeftButtonDown(object sender, MouseButtonEventArgs e)
        {

            m_Cursor = this.Cursor;
            this.Cursor = Cursors.Hand;
            base.DragMove();
        }

        private void cmdExit_Click(object sender, RoutedEventArgs e)
        {
            Close();
        }

        private void Window_MouseLeftButtonUp(object sender, MouseButtonEventArgs e)
        {
            if (m_Cursor != null)
            {
                this.Cursor = m_Cursor;
                m_Cursor = null;
            }
        }
        
    }
}

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
    public partial class MainPage : Page
    {
        private const string DBPATH = "C:/caiche/Github/StockInfo/stock_fund.db";
        private SQLiteConnection db = null;
        private Hashtable hashFunds = new Hashtable();
        private List<StockCode> codeList;

        public MainPage()
        {
            Properties.Resources.Culture = new CultureInfo("zh-CN");
            InitializeComponent();

            db = new SQLiteConnection("Data Source=" + DBPATH);

            codeList = GetCodes();
            lstCode.ItemsSource = codeList;
        }

        private List<StockCode> GetCodes()
        {
            String qrystr = "select code, name from code";
            db.Open();
            SQLiteCommand command = new SQLiteCommand(qrystr, db);
            SQLiteDataReader reader = command.ExecuteReader();

            List<StockCode> codes = new List<StockCode>();
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
            FundList funds = new FundList();

            String tablename = "funds";
            string qrystr = "SELECT date, fund_in, fund_out, fund_net" +
                                   ", fund_per / 100 as fund_per" + 
                                   ", fund_net / value as percent" +
                             " FROM " + tablename + 
                             " WHERE code = '" + stockCode.Code + "'" +
                             " ORDER BY date DESC LIMIT 50";

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
            StockCode code = (StockCode)lstCode.SelectedItem;

            if (!hashFunds.Contains(code.Code))
            {
                FundList fundList = GetFundList(code);

                hashFunds.Add(code.Code, fundList);
            }

            gridFund.ItemsSource = (FundList)hashFunds[code.Code];

        }

        private void cmdGrow_Click(object sender, RoutedEventArgs e)
        {
            DoubleAnimation widthAni = new DoubleAnimation();
            widthAni.To = gridFund.ActualWidth;
            widthAni.Duration = TimeSpan.FromSeconds(3);
            widthAni.AutoReverse = true;
            cmdGrow.BeginAnimation(Button.WidthProperty, widthAni);

            DoubleAnimation heightAni = new DoubleAnimation();
            heightAni.To = 60;
            heightAni.Duration = TimeSpan.FromSeconds(3);
            heightAni.AutoReverse = true;
            cmdGrow.BeginAnimation(Button.HeightProperty, heightAni);
        }

        private void lstCode_MouseDoubleClick(object sender, MouseButtonEventArgs e)
        {
            StockCode code = (StockCode)lstCode.SelectedItem;
            StockData data = StockData.GetData(code.Code);

            if (data != null)
            {
                StockDetailWin w = new StockDetailWin();
                w.SetDataSource(data);

                w.Show();
            }
        }

        
    }
}

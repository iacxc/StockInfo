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
    

    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        private const string DBPATH = "C:/caiche/Github/StockInfo/stock_fund.db";
        private SQLiteConnection m_DB = null;
        private List<StockFund> m_StockFunds;

        Cursor m_Cursor;
        private int m_LimitDays = 50;

        public MainWindow()
        {
            InitializeComponent();

            m_DB = new SQLiteConnection("Data Source=" + DBPATH);

            var codeList = GetCodes();
            var view = CollectionViewSource.GetDefaultView(codeList);
            view.GroupDescriptions.Add(new PropertyGroupDescription("Market"));
            lstCode.DataContext = view;

            m_StockFunds = GetAllFunds();
        }

        private List<StockCode> GetCodes()
        {
            var qrystr = "select code, name from code";
            m_DB.Open();
            var command = new SQLiteCommand(qrystr, m_DB);
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

            m_DB.Close();

            return codes;
        }

        private List<StockFund> GetAllFunds()
        {
            var funds = new List<StockFund>();
            var tablename = "funds";
            var qrystr = String.Format(
@"select code, date, fund_in, fund_out, fund_net
       , fund_per / 100 as fund_per, fund_net / value as percent
       , inc_p / 100 as inc_p
from {0} a 
where date in 
    (select date from {0}
     where code=a.code 
     order by date desc) 
order by code, date", tablename);

            m_DB.Open();
            var command = new SQLiteCommand(qrystr, m_DB);
            var reader = command.ExecuteReader();
            
            while (reader.Read())
            {
                funds.Insert(0, new StockFund()
                {
                    Code = (string)reader["code"],
                    Date = (string)reader["date"],
                    FundIn = (double)reader["fund_in"],
                    FundOut = (double)reader["fund_out"],
                    FundNet = (double)reader["fund_net"],
                    TotalPercent = (double)reader["percent"],
                    CurrentPercent = (double)reader["fund_per"],
                    Inc_p = (double)reader["inc_p"]
                });
            }
            m_DB.Close();

            return funds;
        }
        
        private void lstCode_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            var code = lstCode.SelectedItem as StockCode;

            var funds = from fund in m_StockFunds
                           where fund.Code == code.Code
                           select fund;

            funds = funds.Take(m_LimitDays).OrderBy(f => f.Date);

            double totalFunds = 0, totalPer = 0;
            foreach (var fund in funds)
            {
                totalFunds += fund.FundNet;
                totalPer += fund.TotalPercent;
            }

            List<StockFund> fundList = funds.ToList();
            fundList.Add(new StockFund()
            {
                Code = code.Code,
                Date = Properties.Resources.Summary,
                FundNet = totalFunds,
                TotalPercent = totalPer
            });

            gridFund.DataContext = fundList;
        }

        private void cmdGrow_Click(object sender, RoutedEventArgs e)
        {
            var widthAni = new DoubleAnimation(
                cmdGrow.ActualWidth,
                gridFund.ActualWidth,
                TimeSpan.FromSeconds(3));

            cmdGrow.BeginAnimation(Button.WidthProperty, widthAni);
            cmdGrow.IsEnabled = false;
        }

        private void lstCode_MouseDoubleClick(object sender, MouseButtonEventArgs e)
        {
            var codeList = from code in GetCodes()
                           select code.Code;

            var w = new StockDetailWin();
            w.SetCodeList(codeList);

            w.Show();

        }

        private void Window_MouseLeftButtonDown(object sender, MouseButtonEventArgs e)
        {
            m_Cursor = Cursor;
            Cursor = Cursors.Hand;
            DragMove();
        }

        private void Window_MouseLeftButtonUp(object sender, MouseButtonEventArgs e)
        {
            if (m_Cursor != null)
            {
                Cursor = m_Cursor;
                m_Cursor = null;
            }
        }

        private void OnExit(object sender, ExecutedRoutedEventArgs e)
        {
            Close();
        }

        private void OnOptions(object sender, ExecutedRoutedEventArgs e)
        {
            var dlg = new OptionsDialog(m_LimitDays);

            if (dlg.ShowDialog() == true)
            {
                m_LimitDays = dlg.LimitDays;

            }
        }
        
    }
}

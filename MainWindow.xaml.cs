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
using System.Windows.Navigation;
using System.Windows.Shapes;
using System.Data.SQLite;



namespace Stock_fund
{
    using FundList = ObservableCollection<StockFund>;

    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        private const string DBPATH = "C:/caiche/Github/StockInfo/stock_fund.db";
        private SQLiteConnection db = null;
        private Hashtable hashFunds = new Hashtable();

        public MainWindow()
        {
            InitializeComponent();

            db = new SQLiteConnection("Data Source=" + DBPATH);
            db.Open();

            String qrystr = "select * from code";
            SQLiteCommand command = new SQLiteCommand(qrystr, db);
            SQLiteDataReader reader = command.ExecuteReader();
            while (reader.Read())
            {
                ListBoxItem item = new ListBoxItem();
                item.Content = reader["code"].ToString();
                item.Tag = Convert.ToInt32(reader["market_share"]);
                item.ToolTip = reader["name"];
                lstCode.Items.Add(item);
            }
        }

        private void lstCode_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            ListBoxItem item = (ListBoxItem)lstCode.SelectedItem;
            if (item == null)
                return;

            String tablename = "T" + item.Content;
            String qrystr = "select date, fund_in, fund_out, fund_net, fund_per, price from " + 
                tablename + " order by date";
            
            SQLiteCommand command = new SQLiteCommand(qrystr, db);
            SQLiteDataReader reader = command.ExecuteReader();

            if (!hashFunds.Contains(tablename))
            {
                FundList fundList = new FundList();

                double totalFunds = 0, totalPer = 0;
                while (reader.Read())
                {
                    double amount = Convert.ToDouble(reader["price"]) * Convert.ToDouble(item.Tag);
                    double percent = Convert.ToDouble(reader["fund_net"]) / amount;
                    fundList.Add(new StockFund()
                    {
                        fundDate = reader["date"].ToString(),
                        fundIn = Convert.ToDouble(reader["fund_in"]),
                        fundOut = Convert.ToDouble(reader["fund_out"]),
                        fundNet = Convert.ToDouble(reader["fund_net"]),
                        fundPer = percent
                    });
                    totalFunds += Convert.ToDouble(reader["fund_net"]);
                    totalPer += percent;
                }

                if (fundList.Count() > 0)
                {
                    fundList.Add(new StockFund()
                    {
                        fundDate = "Total", fundIn = null, fundOut = null, fundNet = totalFunds, fundPer = totalPer,

                    });
                }

                hashFunds.Add(tablename, fundList);
            }

            dataGrid.ItemsSource = (FundList)hashFunds[tablename];
        }
    }
}

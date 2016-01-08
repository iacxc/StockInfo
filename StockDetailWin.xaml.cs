using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Shapes;

namespace Stock_fund
{
    /// <summary>
    /// Interaction logic for StockDetails.xaml
    /// </summary>
    public partial class StockDetailWin : Window
    {
        public StockDetailWin()
        {
            InitializeComponent();
        }

        public void SetDataSource(StockData data)
        {
            DataContext = new List<StockData>(){data};

            return;


            //tvStockDetail.Items.Clear();
            //tvStockDetail.Items.Add(item);

        }

    }
}

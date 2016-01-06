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
        class Node
        {
            public string Name { get; set; }
            public string Value { get; set; }
            public List<Node> Nodes { get; set; }

            public Node()
            {
                Nodes = new List<Node>();
            }

            public override string ToString()
            {
                return Name + ":" + Value;
            }
        }

        public StockDetailWin()
        {
            InitializeComponent();
        }

        public void SetDataSource(StockData data)
        {
            TreeViewItem item = new TreeViewItem()
                           { Header = String.Format("{0} : {1}",
                                 Properties.Resources.Code, data.Code) };
            item.Items.Add(new TreeViewItem()
                           { Header = String.Format("{0} : {1}",
                                 Properties.Resources.Price, data.Price) });
            item.Items.Add(new TreeViewItem()
                           { Header = String.Format("{0} : {1}",
                                 Properties.Resources.Last, data.Last) });
            item.Items.Add(new TreeViewItem()
                          { Header = String.Format("{0} : {1}", 
                                Properties.Resources.Open, data.Open) });
            item.Items.Add(new TreeViewItem() 
                          { Header = String.Format("{0} : {1}", 
                              Properties.Resources.High, data.High) });
            item.Items.Add(new TreeViewItem() 
                          { Header = String.Format("{0} : {1}", 
                              Properties.Resources.Low, data.Low) });
            item.Items.Add(new TreeViewItem() 
                          { Header = String.Format("{0} : {1}", 
                              Properties.Resources.Volume, data.Volume) });
            item.Items.Add(new TreeViewItem() 
                          { Header = String.Format("{0} : {1}", 
                              Properties.Resources.Amount, data.Amount) });
            item.Items.Add(new TreeViewItem() 
                          { Header = String.Format("{0} : {1}", 
                              Properties.Resources.CircuValue, data.CircuValue) });
            item.Items.Add(new TreeViewItem() 
                          { Header = String.Format("{0} : {1}", 
                              Properties.Resources.Value, data.Value) });

            tvStockDetail.Items.Clear();
            tvStockDetail.Items.Add(item);

        }

    }
}

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

            Node rootNode = new Node {Name="Code", Value=data.Code};
            rootNode.Nodes.Add(new Node {Name="Price", Value=data.Price.ToString()});
            rootNode.Nodes.Add(new Node {Name="Open", Value=data.Open.ToString()});
            rootNode.Nodes.Add(new Node {Name="Last", Value=data.Last.ToString()});

            List<Node> nodes = new List<Node>(){rootNode};
            tvStockDetail.ItemsSource = nodes;
        }

    }
}

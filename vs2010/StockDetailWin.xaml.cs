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
using System.Windows.Threading;


namespace Stock_fund
{
    /// <summary>
    /// Interaction logic for StockDetails.xaml
    /// </summary>
    public partial class StockDetailWin : Window
    {
        private IEnumerable<string> m_CodeList;
        private DispatcherTimer m_Timer;

        public StockDetailWin()
        {
            InitializeComponent();
            m_Timer = new DispatcherTimer();
            m_Timer.Interval = TimeSpan.FromSeconds(3);
            m_Timer.Tick += Timer_Tick;
        }

        private void Timer_Tick(object sender, EventArgs e)
        {
            var dataList = StockData.GetDatas(m_CodeList);
            dataList.Sort((left, right) =>
            {
                if (left.Inc_p < right.Inc_p) return 1;
                else if (left.Inc_p > right.Inc_p) return -1;
                else return 0;
            });

            DataContext = dataList;
        }

        public void SetCodeList(IEnumerable<string> codeList)
        {

            m_CodeList = codeList;
            m_Timer.Start();

            return;        
        }

    }
}

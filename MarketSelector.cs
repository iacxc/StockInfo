using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Windows;
using System.Windows.Controls;

namespace Stock_fund
{
    public class MarketSelector : StyleSelector
    {
        public Style SHStyle { get; set; }
        public Style SZStyle { get; set; }
        public string PropertyToEvaluate { get; set; }

        public override Style SelectStyle(object item, DependencyObject container)
        {
            StockCode code = (StockCode)item;

            if (code.Code.StartsWith("60"))
            {
                return SHStyle;
            }
            else
            {
                return SZStyle;
            }
        }
    
    }
}

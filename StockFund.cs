﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Stock_fund
{
    class StockFund
    {
        public string FundDate { get; set; }
        public double? FundIn { get; set; }
        public double? FundOut { get; set; }
        public double FundNet { get; set; }
        public double FundPercent { get; set; }
    }
}

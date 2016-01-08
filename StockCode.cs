using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Stock_fund
{
    class StockCode
    {
        public string m_Code;
        public string Code
        {
            get { return m_Code; }
            set
            {
                m_Code = value;
                Market = m_Code.Substring(0, 3);
            }
        }

        public string Market { get; set; }
        public string Name  { get; set; }
             
    }
}

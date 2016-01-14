using System;
using System.Collections.Generic;
using System.Linq;
using System.Windows;
using System.Text.RegularExpressions;
using System.Net;
using System.IO;

namespace Stock_fund
{
    public class StockData
    {
        public string Code { get; set; }
        public string Name { get; set; }
        public double Price { get; set; }
        public double Last { get; set; }
        public double Open { get; set; }
        public double High { get; set; }
        public double Low { get; set; }
        public double Volume { get; set; }
        public double Amount { get; set; }
        public double CircuValue { get; set; }
        public double Value { get; set; }

        public double Inc
        {
            get { return Price - Last; }
        }

        public double Inc_p
        {
            get { return (Price - Last) / Last; }
        }

        public static List<StockData> GetDatas(IEnumerable<string> codeList)
        {
            var codes = new List<string>();
            foreach (var code in codeList)
                codes.Add((code.StartsWith("60") ? "sh" : "sz") + code);

            string URL = "http://qt.gtimg.cn/q=" + String.Join(",", codes);

            HttpWebRequest request = (HttpWebRequest)WebRequest.Create(URL);
            WebResponse resp = request.GetResponse();
            Stream webStream = resp.GetResponseStream();
            StreamReader reader = new StreamReader(webStream);

            string response = reader.ReadToEnd();
            Regex rx = new Regex("(.+)=\"(.+)\"");

            var datas = new List<StockData>();
            foreach (var line in response.Split(new Char[]{'\n'}))
            {
                if (line.Count() == 0)
                    break;

                Match m = rx.Match(line);
                if (m.Success)
                {
                    string[] items = m.Groups[2].ToString().Split(new char[]{'~'});
                    datas.Add(new StockData()
                    {
                        Code=items[2],
                        Name=items[1],
                        Price=Double.Parse(items[3]),
                        Last=Double.Parse(items[4]),
                        Open=Double.Parse(items[5]),
                        High=Double.Parse(items[33]),
                        Low=Double.Parse(items[34]),
                        Amount = Double.Parse(items[36]),
                        Volume=Double.Parse(items[37]),
                        CircuValue=Double.Parse(items[44]),
                        Value=Double.Parse(items[45]),
                    });
                }
            }
            return datas;

        }
    }
}

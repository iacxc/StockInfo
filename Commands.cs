using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Windows.Input;

namespace Stock_fund
{
    static class Commands
    {
        static readonly RoutedUICommand m_OptionsCommand =
            new RoutedUICommand("Options", "Options", typeof(Commands));

        public static RoutedUICommand OptionsCommand
        {
            get { return m_OptionsCommand; }
        }

    }
}

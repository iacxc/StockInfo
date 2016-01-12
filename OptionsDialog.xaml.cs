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
using System.ComponentModel;


namespace Stock_fund
{
    /// <summary>
    /// Interaction logic for Options.xaml
    /// </summary>
    public partial class OptionsDialog : Window, INotifyPropertyChanged
    {

        private int m_LimitDays;
        public int LimitDays {
            get { return m_LimitDays; }

            set
            {
                if (m_LimitDays != value)
                {
                    m_LimitDays = value;
                    OnPropertyChanged("LimitDays");
                }
            }
        }

        public OptionsDialog()
        {
            DataContext = this;
            InitializeComponent();
        }

        public OptionsDialog(int days)
            :this()
        {
            LimitDays = days;
        }

        public event PropertyChangedEventHandler PropertyChanged;

        protected virtual void OnPropertyChanged(string propName)
        {
            var pc = PropertyChanged;
            if (pc != null)
                pc(this, new PropertyChangedEventArgs(propName));
        }

        private void OnOk(object sender, RoutedEventArgs e)
        {
            DialogResult = true;
            Hide();
        }

        private void OnCancel(object sender, RoutedEventArgs e)
        {
            DialogResult = false;
            Hide();
        }

    }
}

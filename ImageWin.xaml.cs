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
using System.Windows.Media.Animation;
using System.Windows.Shapes;

namespace Stock_fund
{
    /// <summary>
    /// Interaction logic for ImageWin.xaml
    /// </summary>
    public partial class ImageWin : Window
    {
        public ImageWin()
        {
            InitializeComponent();
        }

        private void Storyboard_CurrentTimeInvalidated(object sender, EventArgs e)
        {
            Clock storyboardClock = (Clock)sender;

            if (storyboardClock.CurrentProgress == null)
            {
                lblTime.Text = "[[ stoppped ]]";
            }
            else
            {
                lblTime.Text = storyboardClock.CurrentTime.ToString();
            }
        }
    }
}

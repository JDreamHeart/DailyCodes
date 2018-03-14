/*
* @Author: JinZhang
* @Date:   2018-03-14 20:31:48
* @Last Modified by:   JinZhang
* @Last Modified time: 2018-03-14 21:21:13
*/
using System
namespace Algorithmo
{
	class MaoPao
	{
		public double[] initRandomArr(int m, int n)
		{
			double[] arr = new double[n];
			Random ran = new Random();
			for (int i = 0; i < n; i++)
			{
				arr[i] = ran.Next(1,m);
			}
			return arr;
		}
		public void sort(arr)
		{
			double temp = 0;
			int n = arr.Length;
			for (int i = 0; i < n; i++)
			{
				for (int j = 0; j < n-i-1; j++)
				{
					if (arr[j] > arr[j+1])
					{
						temp = arr[j];
						arr[j] = arr[j+1];
						arr[j+1] = temp;
					}
				}
			}
			return arr;
		}
		public void dumpArr(arr)
		{
			string dumpStr = string.Join(", ", arr);
		}
	}

	class ExcuteMaoPao
	{
		public static main(string[] args)
		{
			MaoPao m = new MaoPao();
			double[] arr = m.initRandomArr(100,20);
			m.sort(arr);

		}
	}
}
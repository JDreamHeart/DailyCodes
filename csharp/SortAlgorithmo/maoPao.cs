/*
* @Author: JinZhang
* @Date:   2018-03-14 20:31:48
* @Last Modified by:   JimDreamHeart
* @Last Modified time: 2018-03-18 17:28:49
*/
using System;
namespace Algorithmo
{
	//排序算法类
	class SortAlgorithmoClass
	{
		public double[] sort(double[] arr)
		{
			double temp = new double();
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
	}

	class MainCS
	{
		//初始化随机数组
		public double[] initRandomArr(int m, int n)
		{
			//获取随机数组
			double[] arr = new double[n];
			Random ran = new Random();
			for (int i = 0; i < n; i++)
			{
				arr[i] = ran.Next(1,m);
			}
			//打印数组数据
			dumpArr(arr, 0);
			//返回数组数据
			return arr;
		}
		//打印数组数据
		public void dumpArr(double[] arr, int sortedFlag)
		{
			string dumpStr = string.Join(", ", arr);
			if (sortedFlag == 0)
			{
				Console.WriteLine("Dump array to string before sorting: \n {0} \n", dumpStr);
			}
			else
			{
				Console.WriteLine("Dump array to string after sorting: \n {0} \n", dumpStr);
			}
		}

		static void Main(string[] args)
		{
			//初始化随机数组
			MainCS mainCs = new MainCS();
			double[] arr = mainCs.initRandomArr(100,20);

			//实例化排序对象，并进行排序
			SortAlgorithmoClass sa = new SortAlgorithmoClass();
			sa.sort(arr);

			//打印排序后的数组
			mainCs.dumpArr(arr, 1);
			Console.ReadLine();
		}
	}
}
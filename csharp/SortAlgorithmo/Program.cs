using System;

namespace SortAlgorithmo
{
    class Program
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
			Program program = new Program();
			double[] arr = program.initRandomArr(100,20);

			// //冒泡排序
			// Bubble bbe = new Bubble();
			// bbe.sort(arr);
            
			// //插入排序
			// Insert ist = new Insert();
			// ist.sort(arr);

            // //选择排序
			// Select slt = new Select();
			// slt.sort(arr);

            //希尔排序
			Shell sl = new Shell();
			sl.sort(arr);

			//打印排序后的数组
			program.dumpArr(arr, 1);
			Console.ReadLine();
		}
    }
}

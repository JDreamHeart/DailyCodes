/*
* @Author: JimDreamHeart
* @Date:   2018-03-18 17:00:06
* @Last Modified by:   JimDreamHeart
* @Last Modified time: 2018-03-18 17:35:55
*/
using System;
namespace SortAlgorithmo
{
	//排序算法类
	class Insert
	{
		public double[] sort(double[] arr)
		{
			double temp = new double();
			int n = arr.Length;
			for (int i = 1; i < n; i++)
			{
				temp = arr[i];
				int j = i-1;
				for (; j >= 0; j--)
				{
					if (arr[j] <= temp)
					{
						break;
					}
					arr[j+1] = arr[j];
				}
				arr[j+1] = temp;
			}
			return arr;
		}
	}
}
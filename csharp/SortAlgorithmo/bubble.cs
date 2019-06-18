/*
* @Author: JinZhang
* @Date:   2018-03-14 20:31:48
* @Last Modified by:   JimDreamHeart
* @Last Modified time: 2018-03-18 17:28:49
*/
using System;
namespace SortAlgorithmo
{
	//排序算法类
	class Bubble
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
}
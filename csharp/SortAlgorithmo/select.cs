/*
* @Author: JimDreamHeart
* @Date:   2018-03-18 11:04:30
* @Last Modified by:   JimDreamHeart
* @Last Modified time: 2018-03-18 16:58:57
*/
using System;
namespace SortAlgorithmo
{
	//排序算法类
	class Select
	{
		public double[] sort(double[] arr)
		{
			int maxIdx = 0;
			int n = arr.Length;
			for (int i = 0; i < n; i++)
			{
				maxIdx = i;
				for (int j = i+1; j < n; j++)
				{
					if (arr[j] < arr[maxIdx])
					{
						maxIdx = j;
					}
				}
				double temp = arr[i];
				arr[i] = arr[maxIdx];
				arr[maxIdx] = temp;
			}
			return arr;
		}
	}
}
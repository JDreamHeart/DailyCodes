/*
* @Author: JimDreamHeart
* @Date:   2018-03-18 17:39:10
* @Last Modified by:   JimDreamHeart
* @Last Modified time: 2018-03-18 19:41:07
*/
using System;
namespace SortAlgorithmo
{
	//排序算法类
	class Shell
	{
		public double[] sortBase(double[] arr, int n, int gap)
		{
			double temp = new double();
			for (int i = 0; i < gap; i++)
			{
				for (int j = 1; i + j * gap < n; j++)
				{
					int k = i + (j - 1) * gap;
					temp = arr[k + gap];
					for (; k >= 0; k -= gap)
					{
						if (arr[k] <= temp)
						{
							break;
						}
						arr[k + gap] = arr[k];
					}
					arr[k + gap] = temp;
				}
			}
			return arr;
		}
		public double[] sort(double[] arr)
		{
			int divNum = 2;
			int len = arr.Length;
			int gap = len/divNum;
			while (gap > 0)
			{
				sortBase(arr, len, gap);
				gap /= divNum;
			}
			return arr;
		}
	}
}
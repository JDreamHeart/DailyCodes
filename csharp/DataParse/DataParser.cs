using System;
using System.IO;
using System.Security.Cryptography;
using System.Collections;
using System.Collections.Generic;
using System.Text.Json;

namespace ExcelParse {

    public class ExcelParser : IDataParser {
        public string md5MapJsonPath = "excel_md5_map.json";

        // 解析文件
        public void Parse(string filePath, string dirPath = "") {
            FileInfo fileInfo = new FileInfo(filePath);
            this.Parse(fileInfo);
        }

        // 解析文件
        public void Parse(FileInfo fileInfo, string dirPath) {
            if (!fileInfo.Exists) {
                return;
            }

            // todo: 解析Excel文件
        }

        // 解析对应路径的文件
        public void ParseDir(string dirPath) {
            if (!Directory.Exists(dirPath)) {
                return;
            }

            Dictionary<string, string> oldMd5Map = this.getMD5Map(dirPath);

            Dictionary<string, string> newMd5Map = new Dictionary<string, string>();

            List<string> changedFileList = new List<string>();

            DirectoryInfo dirInfo = new DirectoryInfo(dirPath);
            foreach(FileInfo fileInfo in dirInfo.GetFiles()) {
                string relativePath = fileInfo.FullName.Remove(dirPath);
                string md5Str = this.genMD5(fileInfo);
                if (!oldMd5Map.ContainsKey(relativePath) || oldMd5Map[relativePath] != md5Str) {
                    changedFileList.Add(fileInfo.FullName);
                }
                newMd5Map[relativePath] = md5Str;
            }

            foreach (string filePath in changedFileList) {
                this.Parse(filePath, dirPath);
            }

            this.saveMD5Map(dirPath, newMd5Map);

        }

        // 生成MD5
        string genMD5(string filePath) {
            using (FileStream file = new FileStream(filePath, System.IO.FileMode.Open)) {
                return this.computeMD5(file);
            }
            return "";
        }
        
        // 生成MD5
        string genMD5(FileInfo fileInfo) {
            using (FileStream file = fileInfo.Open(System.IO.FileMode.Open)) {
                return this.computeMD5(file);
            }
            return "";
        }

        // 计算MD5
        string computeMD5(Stream stream) {
            MD5 md5 = new MD5CryptoServiceProvider();
            byte[] hashVal = md5.ComputeHash(stream);
            StringBuilder strBuilder = new StringBuilder();
            for (int i = 0; i < hashVal.Length; i++)
            {
                strBuilder.Append(hashVal[i].ToString("x2"));
            }
            return strBuilder.ToString();
        }

        // 序列化Json并保存
        void saveMD5Map(string dirPath, Dictionary<string, string> md5Map) {
            string filePath = Path.Combine(dirPath, this.md5MapJsonPath); 
            using (FileStream fs = new FileStream(filePath, FileMode.OpenOrCreate)) {
                await JsonSerializer.SerializeAsync(fs, md5Map);
            }
        }

        // 反序列化Json文件
        Dictionary<string, string> getMD5Map(string dirPath) {
            string filePath = Path.Combine(dirPath, this.md5MapJsonPath); 
            if (File.Exists(filePath)) {
                using (FileStream fs = File.OpenRead(filePath)) {
                    return JsonSerializer.Deserialize<Dictionary<string, string>>(fs);
                }
            }
            return new Dictionary<string, string>();
        }

    }

}
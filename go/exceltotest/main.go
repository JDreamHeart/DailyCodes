/*
@Time : 2020/1/16 10:50
@Author : JinZhang
@File : main
@Software: GoLand
*/
package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"github.com/tealeg/xlsx"
	"os"
	"os/exec"
	"path"
	"path/filepath"
	"regexp"
	"strings"
	"time"
)

// 获取当前Go根路径
func getCwd() string {
	cwd, _ := os.Getwd()
	re, _ := regexp.Compile(`^(.*)\\code\.266\.com.*`)
	if sub := re.FindSubmatch([]byte(cwd)); len(sub) > 1 {
		cwd = string(sub[1])
	}
	return cwd
}

// 转换参数
func convertArgs(oriArgs string) (result string, e error) {
	argMap := make(map[string][]string)
	for _, line := range strings.Split(oriArgs, "\n") {
		if kv := strings.Split(line, "="); len(kv) > 1 {
			k, v := kv[0], kv[1]
			argMap[k] = []string{}
			for _, vv := range strings.Split(v, ",") {
				argMap[k] = append(argMap[k], vv)
			}
		}
	}
	args, err := json.Marshal(argMap)
	if err != nil {
		return "{}", err
	}
	return string(args), nil
}

// 执行测试脚本
func execGoTest(filePath, args string) (result string, e error) {
	// 校验测试文件
	if filePath == "" {
		e = fmt.Errorf("Error: Invalid filePath!")
		return
	}
	fp := path.Join(getCwd(), "code.266.com", filePath)
	fp, _ = filepath.Abs(fp)
	if _, err := os.Stat(fp); err != nil {
		e = fmt.Errorf("Error: Doesn't exist file[%s]!", fp)
		return
	}
	// 执行测试脚本
	cmd := exec.Command("go", "test", "-v", fp, "-args", args)
	var out bytes.Buffer
	cmd.Stdout = &out
	cmd.Run()
	fmt.Println(out.String())
	return filterResult(out.String()), nil
}

func filterResult(out string) (result string) {
	isPass := false
	for _, line := range strings.Split(out, "\n") {
		lineBytes := []byte(line)
		// 判断是否开始测试
		if ok, _ := regexp.Match("RUN", lineBytes); ok {
			isPass = false
			continue
		}
		// 判断是否测试通过
		if ok, _ := regexp.Match("PASS:", lineBytes); ok {
			isPass = true
			continue
		}
		// 判断是否为测试通过后的输出
		if isPass {
			re, _ := regexp.Compile(`^.*:\d+:(.*)`)
			if sub := re.FindSubmatch(lineBytes); len(sub) > 1 {
				result += string(sub[1]) + "\n"
			}
		}
	}
	return
}

var outputChan chan int

func outputTestResult(row *xlsx.Row) {
	// 校验当前行数据
	checkType, args := row.Cells[1], row.Cells[2]
	if len(row.Cells) < 6 {
		for k := 0; k < 6-len(row.Cells); k++ {
			row.AddCell()
		}
	}
	// 执行测试，并输出结果
	newArgs, err := convertArgs(args.Value)
	if err != nil {
		row.Cells[5].Value = err.Error()
	} else {
		result, err := execGoTest(checkType.Value, newArgs)
		if err != nil {
			row.Cells[5].Value = err.Error()
		} else {
			row.Cells[5].Value = result
		}
	}
	outputChan <- 1
}

func main() {
	t := time.Now() // 开始时间
	// 校验参数
	if len(os.Args) <= 1 {
		fmt.Println(fmt.Errorf("Error: Invalid main args!"))
		return
	}
	// 获取参数
	inputFile, isOutput := os.Args[1], false
	if len(os.Args) > 2 {
		if ok, _ := regexp.Match("output", []byte(os.Args[2])); ok {
			isOutput = true
		}
	}
	// 加载xlsx文件
	cwd, _ := os.Getwd()
	filePath := path.Join(cwd, inputFile)
	filePath, _ = filepath.Abs(filePath)
	if _, err := os.Stat(filePath); err != nil {
		fmt.Println(fmt.Errorf("Error: Doesn't exist file[%s]!", filePath))
		return
	}
	xlFile, err := xlsx.OpenFile(filePath)
	if err != nil {
		fmt.Println(err.Error())
		return
	}
	// 初始化channel
	totalRow := 0
	outputChan = make(chan int, 10)
	// 遍历sheet
	startRowIdx := 3 // 开始遍历的行数
	for _, sheet := range xlFile.Sheets {
		for i := startRowIdx; i < len(sheet.Rows); i++ { // 遍历行
			if row := sheet.Rows[i]; len(row.Cells) > 2 {
				totalRow++
				go outputTestResult(row)
			}
		}
	}
	// 等待输出结束
	for totalRow > 0 {
		select {
		case e := <-outputChan:
			if e == 0 {
				break
			}
			totalRow--
		}
	}
	// 重新保存文件
	if isOutput {
		err = xlFile.Save(filePath)
		if err != nil {
			fmt.Println(err.Error())
		} else {
			fmt.Println("Go test success.")
		}
	}
	fmt.Println("Go test success. Spent time:", time.Since(t))
}

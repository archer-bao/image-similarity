package main

import (
	"fmt"
	"image/jpeg"
	"os"
	"path/filepath"
	"time"

	"github.com/corona10/goimagehash"
)

func getFilelist(path string) []string {
	var slice []string
	err := filepath.Walk(path, func(path string, f os.FileInfo, err error) error {
		if f == nil {
			return err
		}
		if f.IsDir() {
			return nil
		}
		// println(path)
		slice = append(slice, path)
		return nil
	})
	if err != nil {
		fmt.Printf("filepath.Walk() returned %v\n", err)
	}
	return slice
}

func main() {
	slice1 := getFilelist("/home/user/path1")
	tmp := 0
	for i := 0; i < len(slice1); i++ {
		// fmt.Println(slice[i])
		slice2 := getFilelist("/home/user/path2")
		for j := 0; j < len(slice2); j++ {
			file1, err := os.Open(slice1[1])
			if err != nil {
				fmt.Printf("%v\n", err)
				return
			}

			file2, err := os.Open(slice1[2])
			if err != nil {
				fmt.Printf("%v\n", err)
				return
			}

			img1, _ := jpeg.Decode(file1)
			img2, _ := jpeg.Decode(file2)

			hash1, _ := goimagehash.DifferenceHash(img1)
			hash2, _ := goimagehash.DifferenceHash(img2)
			if tmp%500 == 0 {
				fmt.Println(time.Now())
				fmt.Println(slice1[1], " ==> ", slice1[2])
			}
			distance, _ := hash1.Distance(hash2)
			if distance <= 5 {
				fmt.Println("find: ", slice1[1], " ==> ", slice1[2])
			}

			tmp += 1

			file1.Close()
			file2.Close()
		}
	}
}

/*
BASICS

Runs main communication APIs for core Zelkova performance
All operations must be done in 64 bits for better reading
*/


package main

import (
    "fmt"
)


func main(){
    formatted_matrix_print(partial_matrix([]float64{1, -4, 6, -4, 1}, 8))
    fmt.Println("Success")
}

/*
BASICS

Executes matrix operations
All operations must be done in 64 bits for better reading except those requiring ints for gonum
*/


package main


import (
    "gonum.org/v1/gonum/mat"
    "fmt"
)


// Returns a matrix of zeros
func zeroed_matrix(row_number int, col_number int) *mat.Dense{
    return mat.NewDense(row_number, col_number, nil)
}



// Creates the u matrix for each derivative
// coefficients (arr) (float): Array of coefficients
// ts (int): Total size or resolution, so that the final matrix will be square and ts*ts dimensions

func partial_matrix(coefficients []float64, ts int) *mat.Dense {

    empty := mat.NewDense(ts, ts, nil)
    lc := len(coefficients)
    // Finds the middlepoint of the list given that it has an odd length
    mc := lc/2
    center := coefficients[mc]

    for row:=0; row < ts; row++{

        empty.Set(row, row, center)
        // Goes back and forth
        left_elements := min_of2ints((lc-1)/2, row)
        right_elements := min_of2ints((lc-1)/2, ts-row-1)

        for qq:=1; qq< (left_elements+1); qq++{
            empty.Set(row, row-qq, coefficients[mc-qq])
        }
        for hh:=1; hh< (right_elements+1); hh++{
            empty.Set(row, row+hh, coefficients[mc+hh])
        }
    }

    return empty
}



// Prints a formatted matrix
func formatted_matrix_print(M *mat.Dense){
    fa := mat.Formatted(M, mat.Prefix("   "), mat.Squeeze())
        fmt.Printf("with all values:\na = %v\n\n", fa)
}



// Finds the minimum of two integers
func min_of2ints(a, b int) int {
    if a < b {
        return a
    }
    return b
}


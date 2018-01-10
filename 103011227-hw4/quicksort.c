//
//  main.c
//  quicksort
//
//  Created by 周延儒 on 10/10/2017.
//  Copyright © 2017 周延儒. All rights reserved.
//

#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
int *A; // array
int Partition(int A[], int p, int r) {
    // your code
    int x=A[r];
    int i=p-1;
    int j=0;
    for (j=p;j<r; j++) {
        if (A[j]<=x) {
            i=i+1;
            //swap
            int tmp=A[i];
            A[i]=A[j];
            A[j]=tmp;
        }
    }
    
    
    //swap a[i+1] a[r]
    int tmp=A[i+1];
    A[i+1]=A[r];
    A[r]=tmp;
    
    return i+1;
    
    
}

void QuickSort(int A[], int p, int r) {
    // your code
    if (p<r) {
        int q=0;
        q=Partition(A, p, r);
        QuickSort(A, p, q-1);
        QuickSort(A, q+1, r);
    }
    
}

int main(int argc, char *argv[]) {
    FILE* fh = fopen("randomInt.txt", "r");
    int len;
    fscanf(fh, "%d", &len);
    A = calloc(len, sizeof(int));
    for (int i = 0; i < len; i++) {
        fscanf(fh, "%d", A+i);
    }
    fclose(fh);
    QuickSort(A, 0, len-1);
    // check if they are sorted
    for (int i = 0; i < len; i++) {
        if (A[i] != i) {
            fprintf(stderr, "error A[%d]=%d\n", i, A[i]);
        }
        //printf("A[%d]=%d\n", i, A[i]);
    }
}


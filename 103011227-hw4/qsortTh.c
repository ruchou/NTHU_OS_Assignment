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

int Partition(int p, int r) {
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

int numOfTh=0;

void* QuickSort(void *arg) {
    // your code
    pthread_t first_thread;
    pthread_t second_thread;
    int rc=0;
    
    

    int p=((int*)arg)[0];
    int r=((int*)arg)[1];

    
    if (p<r) {
        int q=0;
        q=Partition(p,r);
        int argsl[2]={p,q-1};
        int argsr[2]={q+1,r};
        
        if (numOfTh<10) {
            rc= pthread_create(&first_thread, NULL, QuickSort,
                               argsl);
            rc = pthread_create(&second_thread, NULL, QuickSort,
                                argsr);
            numOfTh=numOfTh+2;
            pthread_join(first_thread, NULL);
            pthread_join(second_thread, NULL);
            numOfTh=numOfTh-2;
            
        }else{
            QuickSort(argsl);
            QuickSort(argsr);
            
            
        }

    }
    return NULL;
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
    
    int args[2] = { 0, len-1 };
    QuickSort(args);
    // check if they are sorted
    for (int i = 0; i < len; i++) {
        if (A[i] != i) {
            fprintf(stderr, "error A[%d]=%d\n", i, A[i]);
        }
        //printf("A[%d]=%d\n", i, A[i]);
    }
}


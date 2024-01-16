/*

Copyright (c) Buzz, 2025

Author      - Aarav Shreshth
File Name   - stdiof.bzz 
File Type   - Standard library (I/O Subroutines) 
File Scope  - External (universal) 

*/

/* Pre Execution Flags */

**moduletype standalone  


/* INPUT / OUTPUT Subroutines (i/o) */

/*

Main <stdout> function, returns the bytes [stack] 
onto the console.

Return Type: void

*/

modular subr write(StrOrBytes__~str) @ void {

    /* Triggers a assembly call, in this case, it trigger
       write syscall
    */
    :: inb_write___ StrOrBytes__ ;
}



/*
/
/   EOF (End of file)
/
*/
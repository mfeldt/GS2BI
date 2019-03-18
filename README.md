# GS2BI
Make good building instructions with the Lego Digital Designer (LDD)

This python script evaluates the group system created by means of LDD in order
to enforce a sensible order of building instruction steps.

The way to create building instructions is essentially 

  * create groups in LDD be deconstrcucting the model sequentially
      - put the parts added last into the first group created 
      - the second-to last into the second etc.
      - same order goes for subgroups
      - a tutorial can be found here: https://youtu.be/mbef20mRTrI
  * save your file as lxfml
  * run the script like so:
  ```
       python2 gs2bi.py infile.lxfml outfile.lxfml
  ```
  * import the outfile.lxfml into LDD
  * look at the very sensible building instructions
  
  Some hints:
    - Each part must be in one and only in one group!
    - Do not create an all-over container group! Otherwise the resulting BIs 
      will consist of a single step and LDD will enter an infinite loop upon import!
      
    
      

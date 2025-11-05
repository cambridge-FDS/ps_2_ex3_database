2. The block
```
if __name__ == "__main__":
    main()
```
ensures that the functions in `data_loader.py` can be imported as a module without accidentally executing any of the code. If it is run as a script, everything executes as normal.

The package click allows the program to interface with the terminal when run. The "options" are kwargs for the function, which are retrieved from the command line and passed into the call to main.

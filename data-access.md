# 2. Data access:

- We have prepared a data loading module named `nba/data_loader.py`. Have a look at it and write a brief explanation of
    - The purpose of the following code block:

        ```
        if __name__ == "__main__":
            main()
        ```

        -> Answer:

        - The `if __name__ == "__main__":` is used to determine whether the Python script is being executed directly as a script, or imported as a module into another file.

        - When executed directly, Python automatically sets the variable `__name__` to `"__main__"`, causing the `main()` function to run.

        - When imported as a module (e.g., `from nba.data_loader import ...`), `__name__` is set to the module's name (`"nba.data_loader"`). The `main()` block is skipped, preventing `main()` function from running automatically upon import.

    - How the `click` package enables command-line interface functionality.

        -> Answer:

        - By attaching decorators like `@click.command()` and `@click.option(...)` to the `main()` function, `click` automatically binds command-line arguments (such as `-u` for username, `-k` for API key, and `-d` for dataset) directly to the function's parameters.

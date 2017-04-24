##### MySQL Command-Line Tool code execution mode

mysql is a simple SQL shell with input line editing capabilities. It supports interactive and noninteractive use. When used interactively, query results are presented in an ASCII-table format. When used noninteractively (for example, as a filter), the result is presented in tab-separated format. The output format can be changed using command options.

###### Interactive Code Execution

MySQL Shell provides an interactive code execution mode, where you type code at the MySQL Shell prompt and each entered statement is processed, with the result of the processing printed onscreen. These codes can be written in JavaScript, Python or SQL depending on the type of session being used.

###### Batch Code Execution

In addition to the interactive execution of code, MySQL Shell can also take code from different sources and process it. This method of processing code in a non-interactive way is called Batch Execution.

As batch execution mode is intended for script processing of a single language, it is limited to having minimal non-formatted output and disabling the execution of commands. To avoid these limitations, use the --interactive command-line option, which tells MySQL Shell to execute the input as if it were an interactive session. In this mode the input is processed line by line just as if each line were typed in an interactive session. For more information see Section 3.8.3.5, [“Batch Mode Made Interactive”](https://dev.mysql.com/doc/refman/8.0/en/mysql-shell-batch-mode-interactive.html).

If you have problems due to insufficient memory for large result sets, use the `--quick` option. This forces mysql to retrieve results from the server a row at a time rather than retrieving the entire result set and buffering it in memory before displaying it. This is done by returning the result set using the `mysql_use_result()` C API function in the client/server library rather than `mysql_store_result()`.

Reference: 
[MySQL Shell Features](https://dev.mysql.com/doc/refman/8.0/en/mysql-shell-features.html)

[mysql — The MySQL Command-Line Tool](https://dev.mysql.com/doc/refman/8.0/en/mysql.html)
## NULL and UNKNOWN (Transact-SQL)

> From: https://docs.microsoft.com/en-us/sql/t-sql/language-elements/null-and-unknown-transact-sql?view=sql-server-2017

> 03/06/2017

NULL indicates that the value is unknown. A null value is different from an empty or zero value. No two null values are equal. Comparisons between two null values, or between a null value and any other value, return unknown because the value of each NULL is unknown.

Null values generally indicate data that is unknown, not applicable, or to be added later. For example, a customer's middle initial may not be known at the time the customer places an order.

Note the following about null values:

- To test for null values in a query, use IS NULL or IS NOT NULL in the WHERE clause.

- Null values can be inserted into a column by explicitly stating NULL in an INSERT or UPDATE statement or by leaving a column out of an INSERT statement.

- Null values cannot be used as information that is required to distinguish one row in a table from another row in a table, such as primary keys, or for information used to distribute rows, such as distribution keys.

When null values are present in data, logical and comparison operators can potentially return a third result of UNKNOWN instead of just TRUE or FALSE. This need for three-valued logic is a source of many application errors. Logical operators in a boolean expression that includes UNKNOWNs will return UNKNOWN unless the result of the operator does not depend on the UNKNOWN expression. These tables provide examples of this behavior.

The following table shows the results of applying an AND operator to two Boolean expressions where one expression returns UNKNOWN.

<table> 
  <thead> 
    <tr> 
      <th>Expression 1</th>  
      <th>Expression 2</th>  
      <th>Result</th> 
    </tr> 
  </thead>  
  <tbody> 
    <tr> 
      <td>TRUE</td>  
      <td>UNKNOWN</td>  
      <td>UNKNOWN</td> 
    </tr>  
    <tr> 
      <td>UNKNOWN</td>  
      <td class="">UNKNOWN</td>  
      <td>UNKNOWN</td> 
    </tr>  
    <tr> 
      <td>FALSE</td>  
      <td>UNKNOWN</td>  
      <td>FALSE</td> 
    </tr> 
  </tbody> 
</table>

The following table shows the results of applying an OR operator to two Boolean expressions where one expression returns UNKNOWN.

<table> 
  <thead> 
    <tr> 
      <th>Expression 1</th>  
      <th>Expression 2</th>  
      <th>Result</th> 
    </tr> 
  </thead>  
  <tbody> 
    <tr> 
      <td>TRUE</td>  
      <td>UNKNOWN</td>  
      <td>TRUE</td> 
    </tr>  
    <tr> 
      <td>UNKNOWN</td>  
      <td>UNKNOWN</td>  
      <td>UNKNOWN</td> 
    </tr>  
    <tr> 
      <td>FALSE</td>  
      <td>UNKNOWN</td>  
      <td>UNKNOWN</td> 
    </tr> 
  </tbody> 
</table>
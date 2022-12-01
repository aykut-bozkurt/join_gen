## Query Generator for Postgres
Tool generates SELECT queries, whose depth can be configured, with different join orders. It also generates DDLs required for query execution. 
You can also tweak configuration parameters for data inserting command generation.

### Configuration
You can configure 3 different parts:

- [DDL Configuration](#ddl-configuration)
- [Data Insertion Configuration](#data-insertion-configuration)
- [Query Configuration](#query-configuration)

## DDL Configuration
Tool generates related ddl commands before generating queries. 

Schema for DDL configuration:
```yaml
ddlOutFile: <string>
commonColName: <string>
targetTables: <Table[]>
  - Table:
      name: <string>
      citusType: <CitusType>
      maxCount: <int>
      rowCount: <int>
      nullRate: <float>
      duplicateRate: <float>
      columns: <Column[]>
        - Column: 
          name: <string>
          type: <string>
      dupCount: <int>
```

Explanation:
```yaml
ddlOutFile: "file to write generated DDL commands"
commonColName: "name of the column that will be used as distribution column, filter column in restrictions and target column in selections"
targetTables: "array of tables that will be used in generated queries"
  - Table:
      name: "name prefix of table"
      citusType: "citus type of table"
      maxCount: "limits how many times table can appear in query"
      rowCount: "total # of rows that will be inserted into table"
      nullRate: "percentage of null rows in rowCount that will be inserted into table"
      duplicateRate: "percentage of duplicates in rowCount that will be inserted into table"
      columns: "array of columns in table"
        - Column: 
          name: "name of column"
          type: "name of data type of column(only support 'int' now)"
      dupCount: "how many tables with the same configuration we should create(only by changing full name, still using the same name prefix)"
```


## Data Insertion Configuration
Tool generates data insertion commands if you want tables with filled data. You can configure total number of rows, what percentage of them should 
be null and what percentage of them should be duplicated. For related configuration see Table schema at [DDL Configuration](#ddl-configuration). You
can also configure range of the randomly generated data. See `dataRange` at [Query Configuration](#query-configuration).

## Query Configuration
After generation of ddls and data insertion commands, the tool generates queries.

Schema for Query configuration:
```yaml
queryCount: <int>
queryOutFile: <string>
semiAntiJoin: <bool>
limit: <bool>
orderby: <bool>
aggregate: <bool>
useAvgAtTopLevelTarget: <bool>
dataRange:
  from: <int>
  to: <int>
filterRange:
  from: <int>
  to: <int>
limitRange:
  from: <int>
  to: <int>
targetRteCount: <int>
targetCteCount: <int>
targetCteRteCount: <int>
targetJoinTypes: <JoinType[]>
targetRteTypes: <RteType[]>
targetRestrictOps: <RestrictOp[]>
targetAggregateFunctions: <string[]>
```

Explanation:
```yaml
queryCount: "number of queries to generate"
queryOutFile: "fileto write generated queries"
semiAntiJoin: "should we support semin joins (WHERE col IN (Subquery))"
limit: "should we support limit clause"
orderby: "should we support order by clause"
aggregate: "should we support aggregate at targetlist"
useAvgAtTopLevelTarget: "should we make top level query as select avg() from (subquery)"
dataRange:
  from: "starting boundary for data generation"
  to: "end boundary for data generation"
filterRange:
  from: "starting boundary for restriction clause"
  to: "end boundary for restriction clause"
limitRange:
  from: "starting boundary for limit clause"
  to: "end boundary for data limit clause"
targetRteCount: "limits how many rtes should exist in non-cte part of the query"
targetCteCount: "limits how many ctes should exist in query"
targetCteRteCount: "limits how many rtes should exist in cte part of the query"
targetJoinTypes: "supported join types"
targetRteTypes: "supported rte types"
targetRestrictOps: "supported restrict ops"
targetAggregateFunctions: "supported aggregate function names"
```

## Misc Configuration
Tool has some configuration options which does not suit above 3 parts.

Schema for misc configuration:
```yaml
interactiveMode: <bool>
```

Explanation:
```yaml
interactiveMode: "when true, interactively prints generated ddls and queries. Otherwise, it writes them to configured files."
```

## Goal of the Tool
Tool supports a simple syntax to be useful to generate queries with different join orders. Main motivation for me to create the tool was to compare results of the generated queries for different [Citus](https://github.com/citusdata/citus) tables and Postgres tables. That is why we support a basic syntax for now. It can be extended to support different queries.

## Supported Operations
It uses `commonColName` for any kind of target selection required for any supported query clause.

### Column Type Support
Tool currently supports only int data type, but plans to support other basic types.

### Join Support
Tool supports following joins:
```yaml
targetJoinTypes:
  - INNER
  - LEFT
  - RIGHT
  - FULL
```

### Citus Table Support
Tool supports following citus table types:
```yaml
targetTables:
  - Table:
    ...
    citusType: <one of (DISTRIBUTED || REFERENCE || POSTGRES)>
    ...
```

### Restrict Operation Support
Tool supports following restrict operations:
```yaml
targetRestrictOps:
  - LT
  - EQ
  - GT
```

### Rte Support
Tool supports following rtes:
```yaml
targetRteTypes:
  - RELATION
  - SUBQUERY
  - CTE
  - VALUES
```

### Aggregation Support
Tool supports any aggregate functions which takes int column as input and returns int result. e.g. max, min, count

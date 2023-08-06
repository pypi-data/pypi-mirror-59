# Readme

ncbi-taxonomist is still under development and has to be considered unstable.

## Synopsis

ncbi-taxonomist handles and manages phylogenetic data from NCBI. It can:
  - map between taxids and names
  - resolve lineages
  - store obtained taxa and their data locally in a SQLite database
  - group taxa into user defined groups (locally)

taxonomist has several simple operations, e.g. map or import, which work
together using pipes, e.g. to populate a database, map will fetch data from
Entrez and print it to STDOUT while import reads the STDIN to populate a local
database. Taxonomic information is obtained from Entrez, but a predownloaded
database can be imported as well.

The true strength is to find and link related metadata from other Entrez
databases, e.g. fetching data for metagenomic data-sets for specific or
diverse group of organisms. It can store phylogenetic groups, e.g. all taxa
for a specific project, in a local database.

ncbi-taxonomist uses several operations to manage taxonomic information.

## Status

The basic operations are working and unlikely to change in the near future.
Metadata querying is still in development.

## Containers

WIP

## Operations

### map

map taxCollect taxonomic information from Entrez phylogeny server or loading a
downloaded NCBI Taxonomy database into a local database. Returns taxonomic
nodes in JSON.

#### Map taxid and names remotely

`src/ncbi-taxonomist.py map -t 2 -n human -r`

#### Map taxid and names from local database

`src/ncbi-taxonomist.py map -t 2 -n human -db taxa.db`

#### Map sequence accessions

`src/ncbi-taxonomist.py map -t 2 -n human -db taxa.db`

#### Format specific filed from map output to csv using `jq`

```
src/ncbi-taxonomist.py map -t 2 -n human -r \ |
jq -r '[.taxon_id, .names.scientific_name] | @csv
```

### import

Importing stores taxa in a local SQLite database. The taxa are fetched remotely.

#### Import taxa
```
src/ncbi-taxonomist.py map -t 2 -n human -r  | \
src/ncbi-taxonomist.py import -db testdb.sql
```

### Resolve

Resolves lineages for names and taxids. The result is a JSON array with the taxa
defining the lineage in ascending order. This guarnatees the query is the  first
element in the array.

Further extraction can be done via a script reading JSON arrays line-be-line or
via othe tools, e.g. `jq` [REF]

#### Resolve and format via `jq`

```
src/ncbi_taxonomist/ncbi-taxonomist.py resolve  -n man  -db testdb2.sql |  \
jq -r  '[.[] |  .names.scientific_name ]| @tsv'
```
#### Resolve accessions remotely

```
src/ncbi-taxonomist.py map  -a MH842226.1 NQWZ01000003.1 -r | \
src/ncbi-taxonomist.py resolve -m -r

```
### Extract

Extract nodes from a specified superkingdom and subtree
WIP

### Group **WIP**

Collect NCBI taxids into a group for later use


## Output

JSON is returned because I have no clue what you want to do with the result.
This allows to write quick parsers for your needs.

[0]: https://stedolan.github.io/jq/

# parquet-tools-assembly
Parquet-tools assembly and distribution

Repository provides script to clone [apache/parquet-mr](https://github.com/apache/parquet-mr) and
build distribution for submodule `parquet-tools`, command-line utility to read Parquet files.

## Structure
Repo has following structure:
- `bin` binaries copied from `parquet-tools` with some minor changes, e.g. `parquet-cat`
- `lib` contains jar files that will be included in distribution, acts as staging folder
- `sbin` scripts to build distribution
- `staging` staging folder for cloned repositories (folder for each tag)

## Assembly
Script creates `tar.gz` and `zip` distributions with or without Hadoop dependency. Name
`parquet-tools-dist-TAG-VERSION.tar.gz` contains provided tag, `VERSION` is a version of this
repository, not `parquet-tools` or Hadoop. Suffix `-dh` is included in name when client dependency
is included. Some versions of `parquet-tools` have already been prepared,
see [releases](https://github.com/lightcopy/parquet-tools-assembly/releases) for more info.

## Requirements
To build `parquet-tools` you must have `python`, `git` and `mvn` installed, though script checks if
those are available. Currently project works and tested only for Python 2.7.x, but it should be
trivial to extend it for Python 3.x.

## Usage
You can build distribution with or without Hadoop dependency
([see parquet-tools for more info](https://github.com/apache/parquet-mr/tree/master/parquet-tools)),
meaning whether or not client library will be included as part of uber-jar.

```sh
cd parquet-tools-assembly && sbin/make-distribution.sh --tag=XYZ
```

With Hadoop dependency:
```sh
cd parquet-tools-assembly && sbin/make-distribution.sh --tag=XYZ --client=true
```
where:
- `--tag` - `parquet-mr` repository tag to use, e.g. `apache-parquet-1.8.1`.
  See [all available tags](https://github.com/apache/parquet-mr/tags).
- `--client` - whether or not client library should be included.
  If true, distribution name will include `-dh` suffix.

Once archives are built, unarchive them into wanted directory:
```sh
tar zxf parquet-tools-dist.tar.gz
cd parquet-tools-dist
```

And use scripts:
```sh
bin/parquet-schema /path/to/parquet-file
bin/parquet-head /path/to/parquet-file
bin/parquet-cat /path/to/parquet-file
```

#/usr/bin/env python3
import argparse
import csv
import glob
import sys
from textwrap import dedent as _d

DESCRIPTION = """
Generate a script to import some data into openfoodfacts-query database,
from data exported thanks to export_db_sample.py.

It can be piped into psql, for example:
```
python3 import_db_sample.py  data/exports/test /opt/data/exports/test | \
docker compose exec -T query_postgres psql -U productopener -d query
```

It is intended to have data for local development.
"""

def generate_import_script(source_dir, docker_dir):
  outputs = []

  def cmd(sql):
    outputs.append(_d(sql))

  def priority(file_name):
    if file_name.endswith("product.csv"):
      return 0
    if file_name.endswith("product_update.csv"):
      return 1
    if file_name.endswith("product_update_event.csv"):
      return 2
    if file_name.endswith("_tag.csv"):
      return 10
    return 100

  files = glob.glob(f"{source_dir}/*.csv")
  files = sorted(files, key=priority)

  for file in files:
    docker_path = file.replace(source_dir, docker_dir)

    table_name = file.split("/")[-1].split(".")[0]
    csv_reader = csv.reader(open(file), delimiter=",")
    # get column names from csv,
    # because they might not have same order
    colnames = ",".join(next(csv_reader))
    cmd(
      f"""
      COPY {table_name} ({colnames}) FROM '{docker_path}' WITH (FORMAT CSV, DELIMITER ',',HEADER MATCH);
      """
    )
  return outputs

def get_parser():
  parser = argparse.ArgumentParser(description=DESCRIPTION)
  parser.add_argument(
    "source_dir",
    type=str,
    help="path to source directory, containing csv, on the host machine"
  )
  parser.add_argument(
    "docker_dir",
    type=str,
    help="path to source directory, containing csv in the postgres docker container"
  )
  return parser

if __name__ == "__main__":
  parser = get_parser()
  args = parser.parse_args()
  outputs = generate_import_script(args.source_dir, args.docker_dir)
  print("\n".join(outputs))

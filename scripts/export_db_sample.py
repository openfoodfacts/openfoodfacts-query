# /usr/bin/env python3
import argparse
import datetime as dt
import sys
from textwrap import dedent

sys.path.append(".")
from query.tables import product_tags_list

DESCRIPTION = """
Generate a script to export some data from openfoodfacts-query database,
starting from the event table.

It is intended to get data for developers.

It can be piped into the docker psql, this will generates exports in a folder,
that you can then either
get from a shared folder (typically /opt/data mapped to ./data),
or `docker cp -a container_name:/path/to/folder local/path`

This scripts currently only export part of the tables.
"""
# TODO: add product_country, product_scans_by_country, country, contributor


def generate_export_script(from_date, to_date, export_dir):

    outputs = []

    def cmd(sql):
        outputs.append(dedent(sql))

    cmd(
        f"""
    \\! mkdir -p {export_dir}
    -- enable writing by postgres process
    \\! chmod a+rwX {export_dir}
    \\set export_dir '{export_dir}'
    \\set from_date '{from_date}'
    \\set to_date '{to_date}'
    """
    )

    cmd(
        """
    \\set export_path :export_dir/product_update_event.csv

    COPY (
      select * from product_update_event as e
        where
          e.received_at::timestamp between :'from_date' and :'to_date'
    )
    TO :'export_path' DELIMITER ',' CSV HEADER;
    """
    )

    cmd(
        """
    \\set export_path :export_dir/product_update.csv

    COPY (
      select p.* from product_update as p
        left join product_update_event as e
        on p.event_id = e.id
      where
        e.received_at::timestamp between :'from_date' and :'to_date'
    )
    TO :'export_path' DELIMITER ',' CSV HEADER;
    """
    )
    cmd(
        """
    \\set export_path :export_dir/product.csv
    COPY (
      select * from product
      where id in
      (
        select p.product_id from product_update as p
          left join product_update_event as e
          on p.event_id = e.id
        where  e.received_at::timestamp between :'from_date' and :'to_date'
      )
    )
    TO :'export_path' DELIMITER ',' CSV HEADER;
    """
    )
    # should use product_tags.TAG_TABLES
    for table_name in product_tags_list.TAG_TABLES.values():
        cmd(
            f"""
      \\set table_name {table_name}
      \\set export_path :export_dir/:table_name.csv

      COPY (
        select * from :table_name
        where product_id in
        (
          select p.product_id from product_update as p
            left join product_update_event as e
            on p.event_id = e.id
          where  e.received_at::timestamp between :'from_date' and :'to_date'
        )
      )
      TO :'export_path' DELIMITER ',' CSV HEADER;
      """
        )
    return outputs


def get_parser():
    now = dt.datetime.now()
    default_start = (now - dt.timedelta(minutes=20)).strftime("%Y-%m-%d %H:%M:%S")
    default_end = now.strftime("%Y-%m-%d %H:%M:%S")
    default_folder = "/opt/data/exports/" + now.strftime("%Y-%m-%d_%H:%M:%S")
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument(
        "from_date",
        default=default_start,
        type=str,
        nargs="?",
        help=(
            "Start date in iso format, e.g. 2025-11-21 11:00:00\n"
            + "If empty, it's now - 20 minutes"
        ),
    )
    parser.add_argument(
        "to_date",
        default=default_end,
        type=str,
        nargs="?",
        help=(
            "End date in iso format, e.g. 2025-11-21 11:20:00\n" + "If empty, it's now"
        ),
    )
    parser.add_argument(
        "--dest",
        default=default_folder,
        type=str,
        help=(
            "Target directory, it will be created if it does not exists,"
            + f"defaults to {default_folder} (according to current time)"
        ),
    )
    return parser


if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()
    outputs = generate_export_script(args.from_date, args.to_date, args.dest)
    print("\n".join(outputs))

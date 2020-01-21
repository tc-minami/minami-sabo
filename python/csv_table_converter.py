import argparse
import os


# Default value used, if args are not specified.
DEF_CSV_PATH = "./data/input.csv"       # CSV file path to import.
DEF_EXPORT_PATH = "output/output.txt"   # File path to export converted text.
DEF_START_ROW = 2                       # Row index to start extracting from csv.
DEF_END_ROW = 3                         # Row index to end extracting from csv.
DEF_START_COLUMN = 1                    # Column index to start extracting from csv.
DEF_END_COLUMN = -1                     # Column index to end extracting from csv.
DEF_TITLE_IS_ROW = 1                    # Whether 1st row is marked as header. 1 = True / Else = False.
DEF_TITLE_IS_COLUMN = 1                 # Whether 1st column is marked as header. 1 = True / Else = False.

NEW_LINE = "\n"         # Line separator
CSV_SEPARATOR = ","     # CSV separator. To adjust for other format like TSV and PSV, adjust here.

# Tags.
# If need to adjust style, adjust variables here.
TAG_TABLE = "<table>"
TAG_TABLE_END = "</table>"
TAG_TABLE_ROW = "<tr>"
TAG_TABLE_ROW_END = "</tr>"
TAG_TABLE_HEADER = "<th>"
TAG_TABLE_HEADER_END = "</th>"
TAG_TABLE_DATA = "<td>"
TAG_TABLE_DATA_END = "</td>"

# Help text shown when -h or --help is called.
CMD_HELP_CSV = "CSV file path."
CMD_HELP_ROW = "Start row index. First row is 0."
CMD_HELP_ROW_END = "End row index. Not used if negative value."
CMD_HELP_COL = "Start column index. First column is 0."
CMD_HELP_COL_END = "End column index. Not used if negative value."
CMD_HELP_TITLE_IS_ROW = "Whether title is row. Set 1 for true and else for false."
CMD_HELP_TITLE_IS_COL = "Whether title is col. Set 1 for true and else for false."
CMD_HELP_EXPORT = "Export file path. If not set, will not be exported to file."


def get_args():
    """
    Gets the args parameter.

    :return parse_args(): Parameters
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("--csv", help=CMD_HELP_CSV, type=str, default=DEF_CSV_PATH)
    parser.add_argument("--row", help=CMD_HELP_ROW, type=int, default=DEF_START_ROW)
    parser.add_argument("--row_end", help=CMD_HELP_ROW_END, type=int, default=DEF_END_ROW)
    parser.add_argument("--col", help=CMD_HELP_COL, type=int, default=DEF_START_COLUMN)
    parser.add_argument("--col_end", help=CMD_HELP_COL_END, type=int, default=DEF_END_COLUMN)
    parser.add_argument("--title_is_row", help=CMD_HELP_TITLE_IS_ROW, type=int, default=1)
    parser.add_argument("--title_is_col", help=CMD_HELP_TITLE_IS_COL, type=int, default=1)
    parser.add_argument("--export", help=CMD_HELP_EXPORT, type=str, default=DEF_EXPORT_PATH)

    return parser.parse_args()


def read_csv(csv_path: str) -> [[str]]:
    """
    Reads CSV content from given path.

    :param csv_path: strS
    :return csv_text: [[str]] or empty text if csv_path is invalid.
    """

    # Return empty result if csv_path is invalid.
    if not os.path.exists(csv_path):
        print("CSV path is invalid. Please whether csv file exists at {}".format(csv_path))
        return ""

    return [line.rstrip().split(CSV_SEPARATOR) for line in open(csv_path).readlines()]


def convert_csv_2_table(args, csv: [[str]]) -> str:
    """
    Convert csv text to html table text.

    :param args: Parameters
    :param csv: [[str]]
    :return table_html: str
    """

    if not csv:
        return ""

    table_html = "{}{}".format(TAG_TABLE, NEW_LINE)
    for col in range(len(csv)):
        # Check whether to convert this column.
        if args.col > col:
            continue
        if 0 < args.col_end < col:
            continue

        table_html += "{}{}".format(TAG_TABLE_ROW, NEW_LINE)
        for row in range(len(csv[col])):
            # Check whether to convert this row.
            if args.row > row:
                continue
            if 0 < args.row_end < row:
                continue

            # Setup <th> tag or <td> tags.
            if args.title_is_row == 1 and row == args.row:
                table_html += "{}{}{}{}".format(TAG_TABLE_HEADER, csv[col][row], TAG_TABLE_HEADER_END, NEW_LINE)
            elif args.title_is_col == 1 and col == args.col:
                table_html += "{}{}{}{}".format(TAG_TABLE_HEADER, csv[col][row], TAG_TABLE_HEADER_END, NEW_LINE)
            else:
                table_html += "{}{}{}{}".format(TAG_TABLE_DATA, csv[col][row], TAG_TABLE_DATA_END, NEW_LINE)

        # Setup close tags.
        table_html += "{}{}".format(TAG_TABLE_ROW_END, NEW_LINE)
    table_html += "{}{}".format(TAG_TABLE_END, NEW_LINE)

    return table_html


def write_output_file(export_path: str, output_content: str):
    """
    Writes output_content to export_path.

    :param export_path: str
    :param output_content: str
    :return: Null
    """

    if len(export_path) > 0:
        # Create folder if not exist.
        dir_path = os.path.dirname(export_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        # Write to file.
        f = open(export_path, 'w')
        f.write(output_content)
        f.close()
        print("export to file {} complete!".format(export_path))

    else:
        print(output_content)


def main():
    args = get_args()
    table_html = convert_csv_2_table(args, read_csv(args.csv))

    if not table_html:
        print("Failed to convert CSV to Table.")
    else:
        write_output_file(args.export, table_html)


if __name__ == '__main__':
    main()
csvFilePath = DEF_CSV_PATH


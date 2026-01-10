import csv
import os


def read_csv_as_dicts(path, encoding='utf-8', limit=None):
    """Read a CSV file and return a list of dicts (one per row).

    Args:
        path (str): Path to the CSV file.
        encoding (str): File encoding to use.
        limit (int|None): If set, limit the returned rows to this number.

    Returns:
        list[dict]: Rows from the CSV as dictionaries.
    """
    if not os.path.isfile(path):
        raise FileNotFoundError(f"CSV file not found: {path}")

    rows = []
    with open(path, newline='', encoding=encoding) as fh:
        reader = csv.DictReader(fh)
        for i, row in enumerate(reader):
            rows.append(row)
            if limit is not None and i + 1 >= limit:
                break

    return rows


if __name__ == '__main__':
    import sys
    p = sys.argv[1] if len(sys.argv) > 1 else ''
    if not p:
        print('Usage: python csv_importer.py <path-to-csv>')
    else:
        try:
            data = read_csv_as_dicts(p, limit=5)
            print(f'Loaded {len(data)} rows (preview):')
            for r in data:
                print(r)
        except Exception as e:
            print('Error reading CSV:', e)

# CSV → Notion Expenses

Convert an `expenses.csv` into a Notion-flavored markdown table you can paste into a Notion page.

## Usage

```bash
python csv_to_notion.py expenses.csv
python csv_to_notion.py expenses.csv -o notion-expenses.md
python csv_to_notion.py examples/expenses.csv --limit 20
```

## Input columns (flexible)

Looks for common headers: `date`, `merchant`/`vendor`, `description`, `amount`, `currency`, `category`.

## License

MIT

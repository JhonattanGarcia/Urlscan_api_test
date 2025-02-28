# URLScan.io API Search Tool

## Requirements

- You must have an account on [UrlScan.io](https://urlscan.io/) with authorized API access.
- Add your API key to `key.txt` (without line breaks or spaces).
- Configure `config.json` according to your needs.
- Adjust search criteria in `criteria.json`.

## Usage

1. Run the script:
   ```bash
   python Generate_report.py
   ```
2. The results will be saved in the folder defined in `config.json` in JSON or CSV format.

## Configuration

Modify `config.json` to adjust the number of results, output format, and other parameters.

## Configuring `criteria.json`

The file `criteria.json` defines the search parameters. You can modify or add fields as needed. Example:

```json
{
    "search_criteria": [
        { "type": "domain", "value": "example.com" },
        { "type": "ip", "value": "8.8.8.8" }
    ]
}
```

- **type**: Defines the type of search (`domain`, `ip`).
- **value**: The value to be searched.
- You can add or remove search criteria as needed.

## Notes

- `criteria.json` defines the search terms.
- The `key.txt` file should not be shared for security reasons.


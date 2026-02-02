from pathlib import Path
from processing.tb_to_json import process_treebank

import argparse
import json
from pathlib import Path
from typing import Optional

import pandas as pd

''' Example usage: 

Process all Latin AGLDT treebanks with default grammar queries:
    python3 cli.py ../tb_data/AGLDT/Latin/ --lang lat --out ./ --metadata ./treebank_urns.csv

'''

def collect_xml_files(input_path: Path) -> list[Path]:
    if input_path.is_file():
        if input_path.suffix.lower() != ".xml":
            raise ValueError(f"Input file {input_path} is not an XML file")
        return [input_path]

    if input_path.is_dir():
        xml_files = sorted(input_path.glob("*.xml"))
        if not xml_files:
            raise ValueError(f"No XML files found in directory {input_path}")
        return xml_files

    raise ValueError(f"Input path {input_path} does not exist")


def load_user_queries(path: Optional[Path]):
    if path is None:
        return None

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("Grammar query file must contain a list of queries")

    return data


def load_metadata(csv_path: Optional[Path]) -> dict[str, dict[str,str]]:
    """
    Load metadata CSV into a dictionary mapping URN -> {title, author}.
    CSV should have columns: URN, Title, Author
    """
    if csv_path is None:
        return {}

    df = pd.read_csv(csv_path, dtype=str)
    metadata = {}
    for _, row in df.iterrows():
        metadata[row['URN']] = {
            'title': row['Title'],
            'author': row['Author'],
            'prose': row['Prose']
        }

    return metadata


def process_file(
    xml_path: Path,
    *,
    lang: str,
    out_dir: Path,
    prose: bool,
    metadata_dict: dict[str, dict[str,str]]
) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)

    # Resolve metadata from CSV or fallback to file stem
    urn = '.'.join(xml_path.stem.split('.')[:-1])
    meta = metadata_dict.get(urn, {})
    title = meta.get('title', xml_path.stem)
    author = meta.get('author', '')

    prose = meta.get('Prose', True)
    if type(prose) != type(True): #if prose is not a bool
        prose = prose.lower() == 'true'

    doc = process_treebank(
        xml_path,
        lang=lang,
        urn=urn,
        title=title,
        author=author,
        prose=prose,
    )

    out_path = out_dir / f"{xml_path.stem}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(doc, f, indent=4, ensure_ascii=False)

    print(f"✓ Processed {xml_path.name} → {out_path}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert dependency treebank XML files into annotated JSON"
    )

    parser.add_argument("input", help="Path to an XML file or a directory of XML files")
    parser.add_argument("--lang", required=True, help="Language code (e.g. 'grc', 'lat')")
    parser.add_argument("--out", required=True, help="Output directory for JSON files")
    parser.add_argument("--prose", action="store_true", help="Treat text as prose")
    parser.add_argument("--grammar", type=Path, help="Path to JSON file containing additional grammar queries")
    parser.add_argument("--no-default-grammar", action="store_true", help="Do not include built-in grammar queries")
    parser.add_argument("--metadata", type=Path, help="Path to CSV file mapping URNs to Title and Author")

    args = parser.parse_args()

    input_path = Path(args.input)
    out_dir = Path(args.out)

    xml_files = collect_xml_files(input_path)
    metadata_dict = load_metadata(args.metadata)

    for xml_path in xml_files:
        process_file(
            xml_path,
            lang=args.lang,
            out_dir=out_dir,
            prose=args.prose,
            metadata_dict=metadata_dict
        )

if __name__ == "__main__":
    main()
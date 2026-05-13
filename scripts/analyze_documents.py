"""Document analysis tool for RAG pipeline."""
import re
from pathlib import Path
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass, asdict
import json


@dataclass
class DocumentStats:
    """Statistics for a single document."""
    filename: str
    file_size_kb: float
    word_count: int
    line_count: int
    section_count: int
    subsection_count: int
    code_block_count: int
    table_count: int
    emoji_section_count: int
    avg_section_length: float
    sections: List[str]


class DocumentAnalyzer:
    """Analyze markdown documents for RAG pipeline."""

    # Standard emoji sections in Notion documents
    EMOJI_SECTIONS = [
        "🔽 What?",
        "🔁 What does it do?",
        "🤷‍♂️ Why do we use it?",
        "🤔 How does it work?",
        "✍️ How to use it?",
        "👍 Advantages",
        "👎 Disadvantages",
        "↔️ Alternatives",
        "✅ Best practices",
        "🛠️ Use cases",
        "🛑 Worst practices"
    ]

    def __init__(self, data_dir: Path):
        """Initialize analyzer with data directory."""
        self.data_dir = Path(data_dir)

    def analyze_file(self, file_path: Path) -> DocumentStats:
        """Analyze a single markdown file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Basic stats
        file_size_kb = file_path.stat().st_size / 1024
        word_count = len(content.split())
        line_count = len(content.split('\n'))

        # Section analysis
        sections = self._extract_sections(content)
        section_count = len([s for s in sections if s.startswith('## ')])
        subsection_count = len([s for s in sections if s.startswith('### ')])

        # Code blocks
        code_block_count = len(re.findall(r'```[\s\S]*?```', content))

        # Tables
        table_count = len(re.findall(r'\|.*\|.*\n\|[-:| ]+\|', content))

        # Emoji sections
        emoji_section_count = sum(
            content.count(emoji) for emoji in self.EMOJI_SECTIONS
        )

        # Average section length
        section_texts = self._extract_section_texts(content)
        avg_section_length = (
            sum(len(text.split()) for text in section_texts) / len(section_texts)
            if section_texts else 0
        )

        return DocumentStats(
            filename=file_path.name,
            file_size_kb=round(file_size_kb, 2),
            word_count=word_count,
            line_count=line_count,
            section_count=section_count,
            subsection_count=subsection_count,
            code_block_count=code_block_count,
            table_count=table_count,
            emoji_section_count=emoji_section_count,
            avg_section_length=round(avg_section_length, 2),
            sections=[s.strip() for s in sections[:20]]  # First 20 sections
        )

    def _extract_sections(self, content: str) -> List[str]:
        """Extract section headers from markdown."""
        lines = content.split('\n')
        sections = []

        for line in lines:
            if re.match(r'^#{1,3}\s+', line):
                sections.append(line.strip())

        return sections

    def _extract_section_texts(self, content: str) -> List[str]:
        """Extract text content of each section."""
        # Split by ## headers
        sections = re.split(r'\n## ', content)
        return [s.strip() for s in sections if s.strip()]

    def analyze_all(self) -> Dict[str, Any]:
        """Analyze all markdown files in data directory."""
        md_files = list(self.data_dir.glob("*.md"))

        if not md_files:
            return {
                "error": f"No markdown files found in {self.data_dir}",
                "files_analyzed": 0
            }

        stats = []
        for file_path in md_files:
            try:
                file_stats = self.analyze_file(file_path)
                stats.append(file_stats)
            except Exception as e:
                print(f"Error analyzing {file_path.name}: {e}")

        # Aggregate statistics
        total_words = sum(s.word_count for s in stats)
        total_size_kb = sum(s.file_size_kb for s in stats)
        total_sections = sum(s.section_count for s in stats)
        total_code_blocks = sum(s.code_block_count for s in stats)
        total_tables = sum(s.table_count for s in stats)

        return {
            "files_analyzed": len(stats),
            "total_words": total_words,
            "total_size_kb": round(total_size_kb, 2),
            "total_sections": total_sections,
            "total_code_blocks": total_code_blocks,
            "total_tables": total_tables,
            "avg_words_per_file": round(total_words / len(stats), 2) if stats else 0,
            "avg_sections_per_file": round(total_sections / len(stats), 2) if stats else 0,
            "file_stats": [asdict(s) for s in stats]
        }

    def generate_report(self, output_path: Path = None) -> str:
        """Generate a detailed analysis report."""
        results = self.analyze_all()

        if "error" in results:
            return results["error"]

        report_lines = [
            "="*70,
            "DOCUMENT ANALYSIS REPORT",
            "="*70,
            "",
            "SUMMARY",
            "-"*70,
            f"Files analyzed: {results['files_analyzed']}",
            f"Total words: {results['total_words']:,}",
            f"Total size: {results['total_size_kb']:.2f} KB",
            f"Total sections: {results['total_sections']}",
            f"Total code blocks: {results['total_code_blocks']}",
            f"Total tables: {results['total_tables']}",
            f"Avg words per file: {results['avg_words_per_file']:,.2f}",
            f"Avg sections per file: {results['avg_sections_per_file']:.2f}",
            "",
            "FILE DETAILS",
            "-"*70,
        ]

        for file_stat in results['file_stats']:
            report_lines.extend([
                "",
                f"File: {file_stat['filename']}",
                f"  Size: {file_stat['file_size_kb']:.2f} KB",
                f"  Words: {file_stat['word_count']:,}",
                f"  Lines: {file_stat['line_count']:,}",
                f"  Sections (##): {file_stat['section_count']}",
                f"  Subsections (###): {file_stat['subsection_count']}",
                f"  Code blocks: {file_stat['code_block_count']}",
                f"  Tables: {file_stat['table_count']}",
                f"  Emoji sections: {file_stat['emoji_section_count']}",
                f"  Avg section length: {file_stat['avg_section_length']:.2f} words",
                "",
                f"  First sections:",
            ])

            for section in file_stat['sections'][:10]:
                report_lines.append(f"    - {section}")

        report_lines.extend([
            "",
            "="*70,
            "STRUCTURAL PATTERNS DETECTED",
            "="*70,
            "",
            "Standard emoji sections found in documents:",
        ])

        for emoji in self.EMOJI_SECTIONS:
            report_lines.append(f"  - {emoji}")

        report_lines.extend([
            "",
            "RECOMMENDATIONS FOR CHUNKING",
            "-"*70,
            "1. Structure-based chunking by ## headers (primary)",
            "   - Preserves semantic boundaries",
            f"   - Average section: {results['avg_sections_per_file']:.0f} per file",
            "",
            "2. Hierarchical chunking with emoji subsections",
            "   - Parent: Full ## section",
            "   - Children: Individual emoji subsections",
            "",
            "3. Table handling required",
            f"   - {results['total_tables']} tables detected",
            "   - Keep tables within parent sections",
            "",
            "4. Code block preservation",
            f"   - {results['total_code_blocks']} code blocks detected",
            "   - Maintain code formatting in chunks",
            "",
            "="*70,
        ])

        report = "\n".join(report_lines)

        # Save to file if path provided
        if output_path:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(report)

            # Also save JSON
            json_path = output_path.with_suffix('.json')
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2)

            print(f"\nReport saved to: {output_path}")
            print(f"JSON data saved to: {json_path}")

        return report


def main():
    """Run document analysis."""
    data_dir = Path("data/raw")

    if not data_dir.exists():
        print(f"Error: Directory {data_dir} does not exist")
        return

    analyzer = DocumentAnalyzer(data_dir)
    report = analyzer.generate_report(output_path=Path("docs/document_analysis.txt"))

    print(report)


if __name__ == "__main__":
    main()

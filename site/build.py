#!/usr/bin/env python3
from __future__ import annotations

import json
import posixpath
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import markdown
import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape


ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "docs"
TEMPLATE_DIR = ROOT / "site" / "templates"
STATIC_DIR = ROOT / "site" / "static"
GITHUB_BASE_URL = (
    "https://github.com/failuresmith/failure_atlas/blob/main"
)

ID_RE = re.compile(r"\b(?:FP|FM|GR|PM)_\d{3}(?!\d)")
HEADING_RE = re.compile(r"^#\s+(.+)$", re.MULTILINE)
INLINE_META_RE = re.compile(
    r"^\s*(ID|Title|Domain|Mechanism|Class|Subclass|Status|Type|Hypothesis|Invariant)\s*:\s*(.+?)\s*$",
    re.IGNORECASE,
)
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")

TYPE_ORDER = {"FP": 0, "FM": 1, "GR": 2, "PM": 3}
TYPE_LABELS = {
    "FP": "Failure Pattern",
    "FM": "Failure Mode",
    "GR": "Guard Rail",
    "PM": "Postmortem",
}
SOURCE_PRIORITY = {
    "atlas": 0,
    "guardrails": 1,
    "postmortems": 2,
    "lab/postmortems": 3,
    "lab/failure_modes": 4,
}


@dataclass
class TaxonomyInfo:
    failure_domain: str = ""
    mechanism: str = ""
    related_ids: set[str] = field(default_factory=set)


@dataclass
class Artifact:
    id: str
    artifact_type: str
    title: str
    source_path: str
    body_markdown: str
    raw_frontmatter: dict[str, Any] = field(default_factory=dict)
    failure_domain: str = ""
    mechanism: str = ""
    summary: str = ""
    related_ids: list[str] = field(default_factory=list)
    status: str = ""
    bundle_links: list[dict[str, str]] = field(default_factory=list)
    source_url: str = ""
    slug: str = ""
    entry_href: str = ""


def source_priority(path: str) -> int:
    for prefix, rank in SOURCE_PRIORITY.items():
        if path.startswith(prefix):
            return rank
    return 999


def id_sort_key(value: str) -> tuple[int, int, str]:
    match = re.match(r"^(FP|FM|GR|PM)_(\d{3})", value)
    if not match:
        return (999, 999, value)
    prefix, number = match.groups()
    return (int(number), TYPE_ORDER.get(prefix, 99), value)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def split_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---\n"):
        return {}, text
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", text, re.DOTALL)
    if not match:
        return {}, text
    fm_raw, body = match.groups()
    try:
        data = yaml.safe_load(fm_raw) or {}
        if not isinstance(data, dict):
            data = {}
    except yaml.YAMLError:
        data = {}
    return data, body


def parse_inline_metadata(body: str) -> dict[str, str]:
    data: dict[str, str] = {}
    for line in body.splitlines()[:50]:
        match = INLINE_META_RE.match(line)
        if match:
            key, value = match.groups()
            data[key.strip().lower()] = value.strip()
    return data


def infer_id(frontmatter: dict[str, Any], rel_path: str) -> str:
    for key in ("ID", "id"):
        value = frontmatter.get(key)
        if isinstance(value, str):
            match = ID_RE.search(value)
            if match:
                return match.group(0)
    match = ID_RE.search(Path(rel_path).name)
    return match.group(0) if match else ""


def infer_title(frontmatter: dict[str, Any], inline_meta: dict[str, str], body: str, rel_path: str) -> str:
    for key in ("Title", "title"):
        value = frontmatter.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    if inline_meta.get("title"):
        return inline_meta["title"]
    heading = HEADING_RE.search(body)
    if heading:
        return heading.group(1).strip()
    stem = Path(rel_path).stem
    stem = re.sub(r"^(FP|FM|GR|PM)_\d{3}_?", "", stem)
    return stem.replace("_", " ").strip().title() or rel_path


def infer_summary(body: str) -> str:
    blocks = re.split(r"\n\s*\n", body)
    for block in blocks:
        cleaned = block.strip()
        if not cleaned:
            continue
        if cleaned.startswith("#"):
            lines = cleaned.splitlines()
            while lines and lines[0].strip().startswith("#"):
                lines.pop(0)
            cleaned = " ".join(lines).strip()
            if not cleaned:
                continue
        if cleaned.startswith("```"):
            continue
        if cleaned.startswith("|"):
            continue
        if cleaned.startswith("- ") or cleaned.startswith("* "):
            continue
        single = re.sub(r"\s+", " ", cleaned)
        single = re.sub(r"[`*_>#]", "", single).strip()
        if single:
            return single[:240]
    return "No summary available yet."


def normalize_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        items = value
    else:
        items = [value]
    extracted: list[str] = []
    for item in items:
        if not isinstance(item, str):
            continue
        extracted.extend(ID_RE.findall(item))
    return extracted


def extract_related_ids(frontmatter: dict[str, Any], body: str) -> list[str]:
    ids: set[str] = set()
    for key in (
        "reproduced_in",
        "mitigated_by",
        "related_pattern",
        "related_patterns",
        "related",
        "mitigates",
        "postmortem",
    ):
        ids.update(normalize_list(frontmatter.get(key)))
    ids.update(ID_RE.findall(body))
    return sorted(ids, key=id_sort_key)


def strip_markdown(markdown_text: str) -> str:
    text = re.sub(r"```.*?```", " ", markdown_text, flags=re.DOTALL)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1", text)
    text = re.sub(r"[#>*_\-|]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def parse_table_rows(markdown_text: str) -> list[list[str]]:
    rows: list[list[str]] = []
    for line in markdown_text.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if not cells:
            continue
        if all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells if cell):
            continue
        rows.append(cells)
    return rows


def first_id(cell: str) -> str:
    match = ID_RE.search(cell)
    return match.group(0) if match else ""


def apply_taxonomy_mapping(mapping: dict[str, TaxonomyInfo], key: str, failure_domain: str, mechanism: str) -> None:
    if not key:
        return
    current = mapping.setdefault(key, TaxonomyInfo())
    if failure_domain and not current.failure_domain:
        current.failure_domain = failure_domain
    if mechanism and not current.mechanism:
        current.mechanism = mechanism


def add_bidirectional_links(mapping: dict[str, TaxonomyInfo], ids: list[str]) -> None:
    clean_ids = [item for item in ids if item]
    for current in clean_ids:
        node = mapping.setdefault(current, TaxonomyInfo())
        for other in clean_ids:
            if other != current:
                node.related_ids.add(other)


def build_taxonomy_layer() -> dict[str, TaxonomyInfo]:
    mapping: dict[str, TaxonomyInfo] = {}

    failure_index_path = ROOT / "failure_index.md"
    if failure_index_path.exists():
        rows = parse_table_rows(read_text(failure_index_path))
        for row in rows[1:]:
            if len(row) < 7:
                continue
            fp_id = first_id(row[0])
            pm_id = first_id(row[1])
            fm_id = first_id(row[5])
            gr_id = first_id(row[6])
            failure_domain = row[3].strip()
            mechanism = row[4].strip()

            for item in (fp_id, pm_id, fm_id, gr_id):
                apply_taxonomy_mapping(mapping, item, failure_domain, mechanism)
            add_bidirectional_links(mapping, [fp_id, pm_id, fm_id, gr_id])

    docs_taxonomy_path = ROOT / "taxonomy.md"
    if docs_taxonomy_path.exists():
        rows = parse_table_rows(read_text(docs_taxonomy_path))
        for row in rows[1:]:
            if len(row) < 5:
                continue
            failure_domain = row[0].strip()
            mechanism = row[1].strip()
            fp_id = first_id(row[2])
            fm_id = first_id(row[3])
            gr_id = first_id(row[4])

            for item in (fp_id, fm_id, gr_id):
                apply_taxonomy_mapping(mapping, item, failure_domain, mechanism)
            add_bidirectional_links(mapping, [fp_id, fm_id, gr_id])

    return mapping


def infer_artifact_type(artifact_id: str) -> str:
    return artifact_id.split("_", 1)[0] if artifact_id else ""


def artifact_type_label(artifact_type: str) -> str:
    return TYPE_LABELS.get(artifact_type, artifact_type)


def rewrite_relative_links(content: str, source_rel: str) -> str:
    source_dir = posixpath.dirname(source_rel)

    def replace(match: re.Match[str]) -> str:
        text, href = match.groups()
        href = href.strip()
        if not href or href.startswith("#"):
            return match.group(0)
        if re.match(r"^[a-z]+://", href) or href.startswith("mailto:"):
            return match.group(0)

        path_part, anchor = (href.split("#", 1) + [""])[:2]
        if not path_part:
            return match.group(0)

        resolved = posixpath.normpath(posixpath.join(source_dir, path_part))
        if resolved.startswith("../"):
            return match.group(0)

        final = f"{GITHUB_BASE_URL}/{resolved}"
        if anchor:
            final = f"{final}#{anchor}"
        return f"[{text}]({final})"

    return LINK_RE.sub(replace, content)


def make_artifact_from_markdown(rel_path: str) -> Artifact | None:
    file_path = ROOT / rel_path
    text = read_text(file_path)
    frontmatter, body = split_frontmatter(text)
    inline_meta = parse_inline_metadata(body)

    artifact_id = infer_id(frontmatter, rel_path)
    if not artifact_id:
        return None

    artifact_type = infer_artifact_type(artifact_id)
    title = infer_title(frontmatter, inline_meta, body, rel_path)
    summary = infer_summary(body)
    failure_domain = str(
        frontmatter.get("Domain")
        or frontmatter.get("domain")
        or frontmatter.get("failure_domain")
        or frontmatter.get("class")
        or inline_meta.get("domain")
        or inline_meta.get("failure_domain")
        or inline_meta.get("class")
        or ""
    ).strip()
    mechanism = str(
        frontmatter.get("Mechanism")
        or frontmatter.get("mechanism")
        or frontmatter.get("subclass")
        or inline_meta.get("mechanism")
        or inline_meta.get("subclass")
        or ""
    ).strip()
    status = str(frontmatter.get("Status") or frontmatter.get("status") or inline_meta.get("status") or "").strip()
    related_ids = [rid for rid in extract_related_ids(frontmatter, body) if rid != artifact_id]

    return Artifact(
        id=artifact_id,
        artifact_type=artifact_type,
        title=title,
        source_path=rel_path,
        body_markdown=body,
        raw_frontmatter=frontmatter,
        failure_domain=failure_domain,
        mechanism=mechanism,
        summary=summary,
        related_ids=related_ids,
        status=status,
    )


def gather_markdown_artifacts() -> list[Artifact]:
    artifacts: list[Artifact] = []
    roots = [
        ROOT / "atlas",
        ROOT / "guardrails",
        ROOT / "postmortems",
        ROOT / "lab" / "postmortems",
    ]

    for root in roots:
        if not root.exists():
            continue
        for file_path in sorted(root.glob("*.md")):
            if file_path.name == "AGENTS.md":
                continue
            rel_path = file_path.relative_to(ROOT).as_posix()
            artifact = make_artifact_from_markdown(rel_path)
            if artifact:
                artifacts.append(artifact)

    return artifacts


def gather_fm_bundle_artifacts() -> list[Artifact]:
    bundles: list[Artifact] = []
    fm_root = ROOT / "lab" / "failure_modes"
    if not fm_root.exists():
        return bundles

    for directory in sorted(fm_root.iterdir()):
        if not directory.is_dir():
            continue
        match = re.match(r"^(FM_\d{3})", directory.name)
        if not match:
            continue

        fm_id = match.group(1)
        primary = directory / "spec.md"
        if not primary.exists():
            primary = directory / "README.md"
        if not primary.exists():
            continue

        rel_path = primary.relative_to(ROOT).as_posix()
        artifact = make_artifact_from_markdown(rel_path)
        if artifact is None:
            text = read_text(primary)
            _, body = split_frontmatter(text)
            artifact = Artifact(
                id=fm_id,
                artifact_type="FM",
                title=fm_id,
                source_path=rel_path,
                body_markdown=body,
                summary=infer_summary(body),
            )

        artifact.id = fm_id
        artifact.artifact_type = "FM"

        links: list[dict[str, str]] = []
        candidates = [
            ("Directory", directory),
            ("README", directory / "README.md"),
            ("Spec", directory / "spec.md"),
            ("Results", directory / "results" / "summary.md"),
        ]
        for label, path in candidates:
            if path.exists():
                links.append(
                    {
                        "label": label,
                        "path": path.relative_to(ROOT).as_posix(),
                        "url": f"{GITHUB_BASE_URL}/{path.relative_to(ROOT).as_posix()}",
                    }
                )

        artifact.bundle_links = links
        bundles.append(artifact)

    return bundles


def merge_artifacts(artifacts: list[Artifact]) -> list[Artifact]:
    by_id: dict[str, Artifact] = {}

    for artifact in artifacts:
        existing = by_id.get(artifact.id)
        if existing is None:
            by_id[artifact.id] = artifact
            continue

        if source_priority(artifact.source_path) < source_priority(existing.source_path):
            winner, loser = artifact, existing
        else:
            winner, loser = existing, artifact

        related = set(winner.related_ids) | set(loser.related_ids)
        winner.related_ids = sorted(related, key=id_sort_key)
        if not winner.failure_domain and loser.failure_domain:
            winner.failure_domain = loser.failure_domain
        if not winner.mechanism and loser.mechanism:
            winner.mechanism = loser.mechanism
        if (not winner.summary or winner.summary == "No summary available yet.") and loser.summary:
            winner.summary = loser.summary
        if not winner.bundle_links and loser.bundle_links:
            winner.bundle_links = loser.bundle_links
        by_id[winner.id] = winner

    return list(by_id.values())


def enrich_with_taxonomy(artifacts: list[Artifact], taxonomy: dict[str, TaxonomyInfo]) -> list[Artifact]:
    by_id = {artifact.id: artifact for artifact in artifacts}

    for artifact in artifacts:
        tax = taxonomy.get(artifact.id)
        if tax:
            if not artifact.failure_domain:
                artifact.failure_domain = tax.failure_domain
            if not artifact.mechanism:
                artifact.mechanism = tax.mechanism
            artifact.related_ids = sorted(
                set(artifact.related_ids) | set(tax.related_ids) - {artifact.id},
                key=id_sort_key,
            )

    for artifact in artifacts:
        if artifact.failure_domain and artifact.mechanism:
            continue
        fp_related = next((rid for rid in artifact.related_ids if rid.startswith("FP_")), "")
        if fp_related and fp_related in by_id:
            fp_item = by_id[fp_related]
            if not artifact.failure_domain:
                artifact.failure_domain = fp_item.failure_domain
            if not artifact.mechanism:
                artifact.mechanism = fp_item.mechanism

    return artifacts


def assign_paths(artifacts: list[Artifact]) -> None:
    used_slugs: set[str] = set()
    for artifact in artifacts:
        base_slug = artifact.id.lower()
        slug = base_slug
        index = 2
        while slug in used_slugs:
            slug = f"{base_slug}-{index}"
            index += 1
        used_slugs.add(slug)

        artifact.slug = slug
        artifact.entry_href = f"entries/{slug}.html"
        artifact.source_url = f"{GITHUB_BASE_URL}/{artifact.source_path}"


def artifact_sort_key(artifact: Artifact) -> tuple[int, int, str]:
    match = re.match(r"^(FP|FM|GR|PM)_(\d{3})", artifact.id)
    if not match:
        return (999, 999, artifact.id)
    prefix, number = match.groups()
    return (int(number), TYPE_ORDER.get(prefix, 99), artifact.id)


def render_site(artifacts: list[Artifact]) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    entries_dir = OUTPUT_DIR / "entries"
    assets_dir = OUTPUT_DIR / "assets"
    entries_dir.mkdir(parents=True, exist_ok=True)
    assets_dir.mkdir(parents=True, exist_ok=True)

    env = Environment(
        loader=FileSystemLoader(str(TEMPLATE_DIR)),
        autoescape=select_autoescape(["html", "xml"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    env.globals["artifact_type_label"] = artifact_type_label
    md = markdown.Markdown(extensions=["fenced_code", "tables", "sane_lists", "toc"])

    by_id = {artifact.id: artifact for artifact in artifacts}
    source_to_entry = {artifact.source_path: artifact.entry_href for artifact in artifacts}

    for artifact in artifacts:
        grouped_related: dict[str, list[dict[str, str]]] = {}
        for related_id in artifact.related_ids:
            related_item = by_id.get(related_id)
            related_type = related_item.artifact_type if related_item else infer_artifact_type(related_id)
            type_label = artifact_type_label(related_type) or related_id
            if related_item:
                item = {
                    "id": related_id,
                    "title": related_item.title,
                    "type": related_type,
                    "type_label": type_label,
                    "href": f"../{related_item.entry_href}",
                }
            else:
                item = {
                    "id": related_id,
                    "title": type_label,
                    "type": related_type,
                    "type_label": type_label,
                    "href": "",
                }

            grouped_related.setdefault(related_type, []).append(item)

        related_groups = [
            {
                "type": related_type,
                "type_label": artifact_type_label(related_type) or related_type or "Artifact",
                "artifacts": sorted(items, key=lambda item: id_sort_key(item["id"])),
            }
            for related_type, items in sorted(
                grouped_related.items(),
                key=lambda entry: TYPE_ORDER.get(entry[0], 99),
            )
        ]

        rewritten = rewrite_relative_links(artifact.body_markdown, artifact.source_path)
        html_body = md.convert(rewritten)
        html_body = re.sub(r"^\s*<h1[^>]*>.*?</h1>\s*", "", html_body, count=1, flags=re.DOTALL)
        md.reset()

        rendered_bundle_links: list[dict[str, Any]] = []
        for link in artifact.bundle_links:
            internal_entry = source_to_entry.get(link.get("path", ""))
            if internal_entry:
                href = f"../{internal_entry}"
                if internal_entry == artifact.entry_href and link.get("label") == "Spec":
                    href = "#spec"
                rendered_bundle_links.append(
                    {
                        "label": link.get("label", ""),
                        "href": href,
                        "external": False,
                    }
                )
            else:
                rendered_bundle_links.append(
                    {
                        "label": link.get("label", ""),
                        "href": link.get("url", ""),
                        "external": True,
                    }
                )

        template = env.get_template("entry.html")
        rendered = template.render(
            artifact=artifact,
            related_groups=related_groups,
            rendered_bundle_links=rendered_bundle_links,
            rendered_body=html_body,
            asset_prefix="../",
            search_index_url="../search-index.json",
            generated_at=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        )
        (OUTPUT_DIR / artifact.entry_href).write_text(rendered, encoding="utf-8")

    domains = sorted({item.failure_domain for item in artifacts if item.failure_domain})
    mechanisms = sorted({item.mechanism for item in artifacts if item.mechanism})
    types = sorted({item.artifact_type for item in artifacts}, key=lambda x: TYPE_ORDER.get(x, 99))

    index_template = env.get_template("index.html")
    index_html = index_template.render(
        artifacts=artifacts,
        domains=domains,
        mechanisms=mechanisms,
        types=types,
        by_id=by_id,
        asset_prefix="",
        search_index_url="search-index.json",
        generated_at=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
    )
    (OUTPUT_DIR / "index.html").write_text(index_html, encoding="utf-8")

    for static_name in ("styles.css", "app.js"):
        content = read_text(STATIC_DIR / static_name)
        (assets_dir / static_name).write_text(content, encoding="utf-8")

    search_index = []
    manifest_entries = []

    for artifact in artifacts:
        # Keep enough body text in the search index so mid/late sections of
        # entries remain discoverable (e.g. framework names listed in
        # generalization sections).
        excerpt = strip_markdown(artifact.body_markdown)
        searchable_text = " ".join(
            filter(
                None,
                [
                    artifact.id,
                    artifact.title,
                    artifact.artifact_type,
                    artifact.failure_domain,
                    artifact.mechanism,
                    artifact.summary,
                    " ".join(artifact.related_ids),
                    excerpt,
                ],
            )
        )
        search_index.append(
            {
                "id": artifact.id,
                "title": artifact.title,
                "type": artifact.artifact_type,
                "failure_domain": artifact.failure_domain,
                "mechanism": artifact.mechanism,
                "summary": artifact.summary,
                "url": artifact.entry_href,
                "source_url": artifact.source_url,
                "searchable_text": searchable_text,
            }
        )

        manifest_entries.append(
            {
                "id": artifact.id,
                "type": artifact.artifact_type,
                "title": artifact.title,
                "failure_domain": artifact.failure_domain,
                "mechanism": artifact.mechanism,
                "summary": artifact.summary,
                "source_path": artifact.source_path,
                "entry_path": artifact.entry_href,
                "related_ids": artifact.related_ids,
                "bundle_links": artifact.bundle_links,
                "status": artifact.status,
            }
        )

    (OUTPUT_DIR / "search-index.json").write_text(
        json.dumps(search_index, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    (OUTPUT_DIR / "manifest.json").write_text(
        json.dumps(
            {
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "entries": manifest_entries,
                "domains": domains,
                "mechanisms": mechanisms,
                "types": types,
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    (OUTPUT_DIR / ".nojekyll").write_text("", encoding="utf-8")


def main() -> None:
    taxonomy = build_taxonomy_layer()
    artifacts = gather_markdown_artifacts() + gather_fm_bundle_artifacts()
    artifacts = merge_artifacts(artifacts)
    artifacts = enrich_with_taxonomy(artifacts, taxonomy)
    artifacts = sorted(artifacts, key=artifact_sort_key)
    assign_paths(artifacts)
    render_site(artifacts)

    print(f"Generated site with {len(artifacts)} entries -> {OUTPUT_DIR}")


if __name__ == "__main__":
    main()

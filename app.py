"""Validate and report a fictional GRC exercise using the Python standard library.

Public API: validate(data, root) -> list[str]; build_report(data, root) -> dict;
render_markdown(report) -> str.  The latter two consume validated exercise data.
No network calls, security deployment, normative assessment or real acceptance.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import date
import hashlib
import json
import os
from pathlib import Path, PureWindowsPath
import re
import sys
import tempfile
from typing import Any


WARNING = (
    "EXERCICE PÉDAGOGIQUE ASSISTÉ PAR IA — données fictives. Aucun audit qualifié, "
    "conformité certifiée ou décision réelle d'homologation."
)
SCORE_NOTE = (
    "Gravité × vraisemblance : convention locale d'exercice, "
    "non une prescription ISO ou EBIOS RM. Une cible n'est pas un résultat obtenu."
)
ACTION_STATUSES = ("planned", "documented", "implemented_in_lab")
RISK_STATUSES = ("open", "treated", "accepted_simulated")
LEVELS = ("faible", "modéré", "élevé", "critique")
FIELDS = {
    "business_values": ("id", "name", "mission"),
    "supporting_assets": ("id", "name", "business_value_ids"),
    "feared_events": ("id", "name", "business_value_id", "severity", "rationale"),
    "baseline_controls": ("id", "name", "status", "evidence_ids"),
    "risk_sources": ("id", "name", "motivation"),
    "targeted_objectives": ("id", "name"),
    "source_objective_pairs": (
        "id", "risk_source_id", "targeted_objective_id", "retained", "rationale"
    ),
    "stakeholders": ("id", "name", "exposure"),
    "strategic_scenarios": (
        "id", "name", "pair_id", "stakeholder_ids", "feared_event_id", "path"
    ),
    "operational_scenarios": (
        "id", "name", "strategic_scenario_id", "asset_ids", "steps", "likelihood",
        "rationale"
    ),
    "risks": (
        "id", "name", "operational_scenario_id", "initial_severity",
        "initial_likelihood", "current_severity", "current_likelihood",
        "target_severity", "target_likelihood", "rationale", "current_rationale",
        "target_rationale", "action_ids", "status", "acceptance"
    ),
    "treatment_actions": (
        "id", "name", "risk_ids", "owner", "due_date", "status", "evidence_ids"
    ),
    "evidence": ("id", "path", "description"),
}
REFERENCES = {
    "supporting_assets": {"business_value_ids": "business_values"},
    "feared_events": {"business_value_id": "business_values"},
    "baseline_controls": {"evidence_ids": "evidence"},
    "source_objective_pairs": {
        "risk_source_id": "risk_sources", "targeted_objective_id": "targeted_objectives"
    },
    "strategic_scenarios": {
        "pair_id": "source_objective_pairs", "stakeholder_ids": "stakeholders",
        "feared_event_id": "feared_events"
    },
    "operational_scenarios": {
        "strategic_scenario_id": "strategic_scenarios", "asset_ids": "supporting_assets"
    },
    "risks": {"operational_scenario_id": "operational_scenarios", "action_ids": "treatment_actions"},
    "treatment_actions": {"risk_ids": "risks", "evidence_ids": "evidence"},
}
SCALE_FIELDS = {
    "feared_events": ("severity",),
    "operational_scenarios": ("likelihood",),
    "risks": (
        "initial_severity", "initial_likelihood", "current_severity",
        "current_likelihood", "target_severity", "target_likelihood"
    ),
}
SPECIAL_FIELDS = {
    "business_value_ids", "severity", "evidence_ids", "retained", "stakeholder_ids",
    "path", "asset_ids", "steps", "likelihood", "initial_severity",
    "initial_likelihood", "current_severity", "current_likelihood", "target_severity",
    "target_likelihood", "action_ids", "acceptance", "risk_ids", "due_date", "status"
}


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _date(value: Any) -> bool:
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        return False
    try:
        date.fromisoformat(value)
        return True
    except ValueError:
        return False


def _scale(value: Any) -> bool:
    return type(value) is int and 1 <= value <= 4


def _safe_path(root: Path, name: Any, *, must_exist: bool = True) -> Path:
    """Resolve a repository-relative path, refusing traversal and symlink/junctions."""
    if not _text(name) or "\x00" in name:
        raise ValueError("chemin relatif non vide requis")
    portable = name.replace("\\", "/")
    path = Path(portable)
    win = PureWindowsPath(name)
    if path.is_absolute() or win.drive or win.root or ".." in path.parts:
        raise ValueError("chemin hors dépôt ou absolu interdit")
    root = root.resolve()
    candidate = root
    for part in path.parts:
        candidate /= part
        if candidate.is_symlink() or getattr(candidate, "is_junction", lambda: False)():
            raise ValueError("lien symbolique ou jonction interdit")
    try:
        resolved = candidate.resolve(strict=must_exist)
        resolved.relative_to(root)
    except (OSError, RuntimeError, ValueError) as exc:
        raise ValueError("chemin absent, invalide ou hors dépôt") from exc
    return resolved


def _digest(path: Path) -> tuple[str, int]:
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as stream:
        while block := stream.read(1024 * 1024):
            digest.update(block)
            size += len(block)
    return digest.hexdigest(), size


def validate(data: Any, root: str | Path) -> list[str]:
    """Return all detected contract violations; never export or alter any file."""
    errors: list[str] = []
    root = Path(root)
    if not isinstance(data, dict):
        return ["racine : objet JSON requis"]
    metadata = data.get("metadata")
    if not isinstance(metadata, dict):
        errors.append("metadata : objet requis")
    else:
        for field in ("name", "version", "scoring_note", "scope"):
            if not _text(metadata.get(field)):
                errors.append(f"metadata.{field} : texte non vide requis")
        if not _date(metadata.get("created")):
            errors.append("metadata.created : date ISO YYYY-MM-DD valide requise")
        for field in ("educational", "fictional"):
            if metadata.get(field) is not True:
                errors.append(f"metadata.{field} : true obligatoire")
        exclusions = metadata.get("exclusions")
        if not isinstance(exclusions, list) or not exclusions or not all(map(_text, exclusions)):
            errors.append("metadata.exclusions : liste non vide de textes requise")

    rows: dict[str, list[dict]] = {}
    index: dict[str, dict[str, dict]] = {}
    seen_ids: dict[str, str] = {}
    for collection, fields in FIELDS.items():
        values = data.get(collection)
        rows[collection], index[collection] = [], {}
        if not isinstance(values, list) or not values:
            errors.append(f"{collection} : liste non vide requise")
            continue
        for number, row in enumerate(values):
            at = f"{collection}[{number}]"
            if not isinstance(row, dict):
                errors.append(f"{at} : objet requis")
                continue
            rows[collection].append(row)
            for field in fields:
                if field not in row:
                    errors.append(f"{at}.{field} : champ requis")
                elif field not in SPECIAL_FIELDS and not _text(row[field]):
                    errors.append(f"{at}.{field} : texte non vide requis")
            identifier = row.get("id")
            if _text(identifier):
                if identifier in seen_ids:
                    errors.append(f"{at}.id : identifiant dupliqué {identifier!r} ({seen_ids[identifier]})")
                else:
                    seen_ids[identifier] = at
                index[collection][identifier] = row
            for field in SCALE_FIELDS.get(collection, ()):
                if not _scale(row.get(field)):
                    errors.append(f"{at}.{field} : entier 1–4 requis (booléen interdit)")
            if collection in ("baseline_controls", "treatment_actions"):
                if row.get("status") not in ACTION_STATUSES:
                    errors.append(f"{at}.status : statut de mesure inconnu")
            if collection == "treatment_actions" and not _date(row.get("due_date")):
                errors.append(f"{at}.due_date : date ISO valide requise")
            if collection == "source_objective_pairs" and type(row.get("retained")) is not bool:
                errors.append(f"{at}.retained : booléen requis")
            if collection in ("strategic_scenarios", "operational_scenarios"):
                field = "path" if collection == "strategic_scenarios" else "steps"
                if not isinstance(row.get(field), list) or not row[field] or not all(map(_text, row[field])):
                    errors.append(f"{at}.{field} : liste non vide de textes requise")

    # References are checked against the correct collection, not merely any known ID.
    for collection, refs in REFERENCES.items():
        for number, row in enumerate(rows[collection]):
            at = f"{collection}[{number}]"
            for field, target in refs.items():
                value = row.get(field)
                if field.endswith("_ids"):
                    if not isinstance(value, list) or (not value and field != "evidence_ids"):
                        errors.append(f"{at}.{field} : liste de références non vide requise")
                        continue
                    valid_values = [v for v in value if _text(v)]
                    if len(set(valid_values)) != len(valid_values):
                        errors.append(f"{at}.{field} : références dupliquées")
                    references = value
                else:
                    references = [value]
                for ref in references:
                    if not _text(ref) or ref not in index[target]:
                        errors.append(f"{at}.{field} : référence inconnue dans {target}: {ref!r}")
            if collection in ("baseline_controls", "treatment_actions"):
                if row.get("status") == "implemented_in_lab" and not row.get("evidence_ids"):
                    errors.append(f"{at} : mise en œuvre annoncée sans preuve")

    evidence_paths: set[str] = set()
    for number, row in enumerate(rows["evidence"]):
        try:
            path = _safe_path(root, row.get("path"))
            if not path.is_file():
                raise ValueError("la preuve doit être un fichier existant")
            key = os.path.normcase(str(path))
            if key in evidence_paths:
                errors.append(f"evidence[{number}].path : chemin de preuve dupliqué")
            evidence_paths.add(key)
        except (ValueError, OSError, RuntimeError) as exc:
            errors.append(f"evidence[{number}].path : {exc}")

    def lookup(collection: str, identifier: Any) -> dict | None:
        return index[collection].get(identifier) if _text(identifier) else None

    for row in rows["strategic_scenarios"]:
        pair = lookup("source_objective_pairs", row.get("pair_id"))
        if pair is not None and pair.get("retained") is not True:
            errors.append(f"strategic_scenarios.{row.get('id')} : paire non retenue")

    def refs(row: dict, field: str) -> list[str]:
        value = row.get(field)
        return [v for v in value if _text(v)] if isinstance(value, list) else []

    for risk in rows["risks"]:
        rid = risk.get("id", "?")
        status = risk.get("status")
        if status not in RISK_STATUSES:
            errors.append(f"risks.{rid}.status : statut de risque inconnu")
        actions = [index["treatment_actions"][a] for a in refs(risk, "action_ids")
                   if a in index["treatment_actions"]]
        for action in actions:
            if rid not in refs(action, "risk_ids"):
                errors.append(f"risks.{rid} : lien action {action.get('id')} non réciproque")
        operational = lookup("operational_scenarios", risk.get("operational_scenario_id"))
        if operational:
            if risk.get("initial_likelihood") != operational.get("likelihood"):
                errors.append(f"risks.{rid} : vraisemblance initiale différente du scénario opérationnel")
            strategic = lookup("strategic_scenarios", operational.get("strategic_scenario_id"))
            event = lookup("feared_events", strategic.get("feared_event_id")) if strategic else None
            if event and risk.get("initial_severity") != event.get("severity"):
                errors.append(f"risks.{rid} : gravité initiale différente de l'événement redouté")
        implemented = [a for a in actions if a.get("status") == "implemented_in_lab" and refs(a, "evidence_ids")]
        scales = [risk.get(f"{phase}_{axis}") for phase in ("initial", "current")
                  for axis in ("severity", "likelihood")]
        if all(map(_scale, scales)):
            lowered = risk["current_severity"] < risk["initial_severity"] or risk["current_likelihood"] < risk["initial_likelihood"]
            if lowered and (not implemented or not _text(risk.get("current_rationale"))):
                errors.append(f"risks.{rid} : baisse du risque courant sans action mise en œuvre et preuve expliquée")
        all_implemented = bool(actions) and len(implemented) == len(refs(risk, "action_ids"))
        if status in ("treated", "accepted_simulated") and not all_implemented:
            errors.append(f"risks.{rid} : statut traité/accepté sans toutes les actions mises en œuvre avec preuves")
        acceptance = risk.get("acceptance")
        if status == "accepted_simulated":
            if not isinstance(acceptance, dict):
                errors.append(f"risks.{rid}.acceptance : dossier d'acceptation simulée requis")
            else:
                for field in ("reviewer", "rationale"):
                    if not _text(acceptance.get(field)):
                        errors.append(f"risks.{rid}.acceptance.{field} : texte non vide requis")
                if not _date(acceptance.get("date")):
                    errors.append(f"risks.{rid}.acceptance.date : date ISO valide requise")
                if acceptance.get("simulated") is not True:
                    errors.append(f"risks.{rid}.acceptance.simulated : true obligatoire")
        elif acceptance is not None:
            errors.append(f"risks.{rid}.acceptance : null requis hors acceptation simulée")

    for action in rows["treatment_actions"]:
        for risk_id in refs(action, "risk_ids"):
            risk = index["risks"].get(risk_id)
            if risk is not None and action.get("id") not in refs(risk, "action_ids"):
                errors.append(f"treatment_actions.{action.get('id')} : lien risque {risk_id} non réciproque")
    return errors


def _level(score: int) -> str:
    return LEVELS[0] if score <= 3 else LEVELS[1] if score <= 7 else LEVELS[2] if score <= 11 else LEVELS[3]


def build_report(data: Any, root: str | Path) -> dict:
    """Validate, recalculate evidence hashes and return a deterministic report."""
    errors = validate(data, root)
    if errors:
        raise ValueError("\n".join(errors))
    root = Path(root).resolve()
    risks = []
    for risk in sorted(data["risks"], key=lambda row: row["id"]):
        out = {key: risk[key] for key in (
            "id", "name", "operational_scenario_id", "status", "rationale",
            "current_rationale", "target_rationale"
        )}
        out["acceptance"] = ({key: risk["acceptance"][key] for key in
                              ("reviewer", "date", "rationale", "simulated")}
                             if risk["acceptance"] is not None else None)
        out["action_ids"] = sorted(risk["action_ids"])
        for phase in ("initial", "current", "target"):
            severity, likelihood = risk[f"{phase}_severity"], risk[f"{phase}_likelihood"]
            score = severity * likelihood
            out[phase] = {"severity": severity, "likelihood": likelihood, "score": score, "level": _level(score)}
        risks.append(out)
    evidence = []
    for row in sorted(data["evidence"], key=lambda item: item["id"]):
        path = _safe_path(root, row["path"])
        try:
            digest, size = _digest(path)
        except OSError as exc:
            raise ValueError(f"Preuve illisible {row['id']}: {exc}") from exc
        evidence.append({"id": row["id"], "path": path.relative_to(root).as_posix(),
                         "description": row["description"], "sha256": digest, "size_bytes": size})
    action_counts = Counter(row["status"] for row in data["treatment_actions"])
    risk_counts = Counter(row["status"] for row in data["risks"])
    level_counts = Counter(row["current"]["level"] for row in risks)
    registers = {}
    for collection, fields in FIELDS.items():
        if collection in ("risks", "evidence"):
            continue
        registers[collection] = [{key: row[key] for key in fields}
                                 for row in sorted(data[collection], key=lambda item: item["id"])]
    return {
        "warning": WARNING,
        "scoring_convention": SCORE_NOTE,
        "metadata": {key: data["metadata"][key] for key in (
            "name", "version", "created", "educational", "fictional", "scope", "scoring_note", "exclusions"
        )},
        "summary": {
            "risks_total": len(risks), "actions_total": len(data["treatment_actions"]),
            "actions_by_status": {key: action_counts[key] for key in ACTION_STATUSES},
            "risks_by_status": {key: risk_counts[key] for key in RISK_STATUSES},
            "current_risks_by_level": {key: level_counts[key] for key in LEVELS},
        },
        "risks": risks, "evidence": evidence, "registers": registers,
    }


def _md(value: Any) -> str:
    return str(value).replace("\\", "\\\\").replace("|", "\\|").replace("<", "&lt;").replace(">", "&gt;").replace("\r", " ").replace("\n", " ")


def render_markdown(report: dict) -> str:
    """Render the report without timestamps, external services or inferred compliance."""
    meta = report["metadata"]
    lines = [f"> **{WARNING}**", "", f"# {_md(meta['name'])}", "",
             f"Version : {_md(meta['version'])} — créé le {_md(meta['created'])}.", "",
             f"Périmètre : {_md(meta['scope'])}", "", SCORE_NOTE, "", _md(meta["scoring_note"]), "",
             "## Limites", ""]
    lines += [f"- {_md(value)}" for value in meta["exclusions"]]
    lines += ["- Un fichier de preuve ou un test local ne démontre pas l'efficacité dans un SI réel.",
              "- Aucun audit PASSI, conformité ISO/LPM ou décision réelle d'homologation n'est prononcé.", "",
              "## Risques : initial, courant et cible", "",
              "| Risque | Initial | Courant | Cible non acquise | Statut | Actions |",
              "|---|---|---|---|---|---|"]
    for row in report["risks"]:
        values = []
        for phase in ("initial", "current", "target"):
            state = row[phase]
            values.append(f"{state['severity']} × {state['likelihood']} = {state['score']} ({state['level']})")
        lines.append("| " + " | ".join(map(_md, [row["id"] + " — " + row["name"], *values,
                                                row["status"], ", ".join(row["action_ids"])])) + " |")
    for row in report["risks"]:
        lines += ["", f"### {_md(row['id'])} — justifications", "",
                  f"- Initial : {_md(row['rationale'])}",
                  f"- Courant : {_md(row['current_rationale'])}",
                  f"- Cible : {_md(row['target_rationale'])}"]
        if row["acceptance"] is not None:
            accept = row["acceptance"]
            lines.append(f"- Acceptation **simulée** : {_md(accept['reviewer'])}, {_md(accept['date'])} — {_md(accept['rationale'])}")
    lines += ["", "## Actions de traitement", "",
              "| Statut | Nombre |", "|---|---:|"]
    lines += [f"| {status} | {report['summary']['actions_by_status'][status]} |" for status in ACTION_STATUSES]
    lines += ["", "| Action | Risques | Responsable fictif | Échéance | Statut | Preuves |",
              "|---|---|---|---|---|---|"]
    for row in report["registers"]["treatment_actions"]:
        lines.append("| " + " | ".join(map(_md, [row["id"] + " — " + row["name"], ", ".join(row["risk_ids"]),
                                                row["owner"], row["due_date"], row["status"], ", ".join(row["evidence_ids"])])) + " |")
    lines += ["", "## Mesures de base", "", "| Mesure | Statut déclaré | Preuves |", "|---|---|---|"]
    for row in report["registers"]["baseline_controls"]:
        lines.append("| " + " | ".join(map(_md, [row["id"] + " — " + row["name"], row["status"], ", ".join(row["evidence_ids"])])) + " |")
    lines += ["", "## Empreintes des preuves", "",
              "| ID | Fichier relatif | Taille (octets) | SHA-256 |", "|---|---|---:|---|"]
    for row in report["evidence"]:
        lines.append("| " + " | ".join(map(_md, [row["id"], row["path"], row["size_bytes"], row["sha256"]])) + " |")
    lines += ["", "Le rapport JSON conserve les registres et références du scénario. "
              "Les empreintes identifient les octets lus ; elles ne certifient ni le contenu ni une conformité.", ""]
    return "\n".join(lines)


def _unique_object(pairs: list[tuple[str, Any]]) -> dict:
    out = {}
    for key, value in pairs:
        if key in out:
            raise ValueError(f"Clé JSON dupliquée : {key}")
        out[key] = value
    return out


def _reject_constant(value: str) -> None:
    raise ValueError(f"Constante JSON non standard interdite : {value}")


def main(argv: list[str] | None = None, *, root: str | Path | None = None) -> int:
    parser = argparse.ArgumentParser(description=WARNING)
    commands = parser.add_subparsers(dest="command", required=True)
    for command in ("validate", "report"):
        sub = commands.add_parser(command)
        sub.add_argument("--data", default="data/scenario.json", help="Fichier JSON relatif à la racine du projet")
        if command == "report":
            sub.add_argument("--output", default="reports", help="Répertoire relatif à la racine du projet")
    args = parser.parse_args(argv)
    root = Path(root) if root is not None else Path(__file__).resolve().parent
    try:
        input_path = _safe_path(root, args.data)
        with input_path.open("r", encoding="utf-8") as stream:
            data = json.load(stream, object_pairs_hook=_unique_object, parse_constant=_reject_constant)
        errors = validate(data, root)
        if errors:
            for error in errors:
                print(f"Erreur : {error}", file=sys.stderr)
            return 1
        if args.command == "validate":
            print(f"VALID — {len(data['risks'])} risques fictifs, {len(data['treatment_actions'])} actions. {WARNING}")
            return 0
        report = build_report(data, root)
        content = {
            "report.json": json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False) + "\n",
            "report.md": render_markdown(report),
        }
        output = _safe_path(root, args.output, must_exist=False)
        for name in content:
            _safe_path(root, (Path(args.output) / name).as_posix(), must_exist=False)
        output.mkdir(parents=True, exist_ok=True)
        pending: list[tuple[str, Path]] = []
        try:
            for name, text in content.items():
                with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", newline="\n", dir=output,
                                                 prefix=".grc-", suffix=".tmp", delete=False) as stream:
                    pending.append((stream.name, output / name))
                    stream.write(text)
            for temporary, destination in pending:
                os.replace(temporary, destination)
        finally:
            for temporary, _ in pending:
                Path(temporary).unlink(missing_ok=True)
        print(f"Rapports pédagogiques écrits : {output / 'report.json'} ; {output / 'report.md'}")
        return 0
    except (ValueError, OSError, RuntimeError, UnicodeError) as exc:
        print(f"Erreur : {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())


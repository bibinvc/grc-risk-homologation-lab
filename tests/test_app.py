"""Contract and CLI regression tests using an entirely temporary fictional case."""
import contextlib
import copy
import hashlib
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

import app


def fixture():
    return {
        "metadata": {
            "name": "Cas fictif de validation", "version": "1.0", "created": "2026-11-12",
            "educational": True, "fictional": True, "scope": "Laboratoire local uniquement",
            "scoring_note": "Matrice locale d'apprentissage, pas une méthode normative.",
            "exclusions": ["Aucun SI réel", "Aucune décision réelle"],
        },
        "business_values": [{"id": "BV1", "name": "Continuité", "mission": "Service fictif"}],
        "supporting_assets": [{"id": "AS1", "name": "Serveur fictif", "business_value_ids": ["BV1"]}],
        "feared_events": [{"id": "FE1", "name": "Interruption", "business_value_id": "BV1", "severity": 4,
                           "rationale": "Impact fictif majeur"}],
        "baseline_controls": [{"id": "BC1", "name": "Procédure rédigée", "status": "documented", "evidence_ids": []}],
        "risk_sources": [{"id": "RS1", "name": "Source fictive", "motivation": "Perturbation fictive"}],
        "targeted_objectives": [{"id": "TO1", "name": "Indisponibilité"}],
        "source_objective_pairs": [{"id": "PA1", "risk_source_id": "RS1", "targeted_objective_id": "TO1",
                                    "retained": True, "rationale": "Hypothèse pédagogique"}],
        "stakeholders": [{"id": "SH1", "name": "Prestataire fictif", "exposure": "Dépendance fictive"}],
        "strategic_scenarios": [{"id": "SS1", "name": "Parcours stratégique", "pair_id": "PA1",
                                 "stakeholder_ids": ["SH1"], "feared_event_id": "FE1", "path": ["Dépendance", "Interruption"]}],
        "operational_scenarios": [{"id": "OS1", "name": "Parcours opérationnel", "strategic_scenario_id": "SS1",
                                   "asset_ids": ["AS1"], "steps": ["Condition fictive", "Observation locale"],
                                   "likelihood": 3, "rationale": "Hypothèse de travail"}],
        "risks": [{"id": "RI1", "name": "Risque fictif", "operational_scenario_id": "OS1",
                   "initial_severity": 4, "initial_likelihood": 3, "current_severity": 4, "current_likelihood": 3,
                   "target_severity": 2, "target_likelihood": 2, "rationale": "Scénario de référence",
                   "current_rationale": "Mesures non mises en œuvre : aucune baisse acquise.",
                   "target_rationale": "Cible hypothétique après vérification future.",
                   "action_ids": ["TA1"], "status": "open", "acceptance": None}],
        "treatment_actions": [{"id": "TA1", "name": "Action fictive", "risk_ids": ["RI1"], "owner": "Rôle fictif",
                               "due_date": "2026-12-01", "status": "planned", "evidence_ids": []}],
        "evidence": [{"id": "EV1", "path": "evidence/checks.txt", "description": "Sortie synthétique locale"}],
    }


class ContractTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / "evidence").mkdir()
        (self.root / "evidence/checks.txt").write_text("Synthetic test evidence.\n", encoding="utf-8")
        self.data = fixture()

    def errors(self, expected=None):
        errors = app.validate(self.data, self.root)
        self.assertTrue(errors)
        if expected:
            self.assertIn(expected, "\n".join(errors))
        return errors

    def implement(self):
        action = self.data["treatment_actions"][0]
        action.update(status="implemented_in_lab", evidence_ids=["EV1"])
        self.data["risks"][0]["current_rationale"] = "Vérification fictive locale avec preuve EV1."

    def write_data(self, text=None):
        path = self.root / "data/scenario.json"
        path.parent.mkdir(exist_ok=True)
        path.write_text(text if text is not None else json.dumps(self.data, ensure_ascii=False), encoding="utf-8")
        return path

    def run_cli(self, *args):
        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = app.main(list(args), root=self.root)
        return code, stdout.getvalue(), stderr.getvalue()

    def test_valid_case_allows_documented_baseline_without_claiming_reduction(self):
        self.assertEqual(app.validate(self.data, self.root), [])

    def test_all_collections_required_and_nonempty(self):
        for name in app.FIELDS:
            with self.subTest(name=name):
                changed = copy.deepcopy(self.data)
                changed[name] = []
                self.assertTrue(app.validate(changed, self.root))
        self.assertTrue(app.validate([], self.root))

    def test_required_text_and_metadata_flags(self):
        self.data["metadata"].update(name="  ", educational=1, fictional=False, scope=None)
        self.data["risks"][0]["current_rationale"] = ""
        errors = self.errors()
        self.assertGreaterEqual(len(errors), 5)

    def test_duplicate_identifiers_across_different_collections(self):
        self.data["supporting_assets"][0]["id"] = "BV1"
        self.errors("identifiant dupliqué")

    def test_duplicate_references_are_not_silently_counted_twice(self):
        self.data["risks"][0]["action_ids"] = ["TA1", "TA1"]
        self.errors("références dupliquées")

    def test_reference_must_resolve_to_correct_collection(self):
        self.data["operational_scenarios"][0]["asset_ids"] = ["BV1"]
        self.errors("référence inconnue dans supporting_assets")

    def test_reference_integrity_for_each_relationship(self):
        for collection, fields in app.REFERENCES.items():
            for field in fields:
                with self.subTest(collection=collection, field=field):
                    changed = copy.deepcopy(self.data)
                    changed[collection][0][field] = ["MISSING"] if field.endswith("_ids") else "MISSING"
                    self.assertTrue(app.validate(changed, self.root))

    def test_malformed_nested_types_return_errors_instead_of_crashing(self):
        cases = [("risks", "operational_scenario_id", {}), ("strategic_scenarios", "pair_id", []),
                 ("operational_scenarios", "strategic_scenario_id", []), ("feared_events", "severity", {}),
                 ("risks", "action_ids", [{}]), ("treatment_actions", "risk_ids", [True]),
                 ("baseline_controls", "evidence_ids", {}), ("risks", "status", [])]
        for collection, field, value in cases:
            with self.subTest(collection=collection, field=field):
                changed = copy.deepcopy(self.data)
                changed[collection][0][field] = value
                self.assertTrue(app.validate(changed, self.root))
        changed = copy.deepcopy(self.data)
        changed["risks"] = [None, 7]
        self.assertTrue(app.validate(changed, self.root))

    def test_scale_rejects_boolean_float_and_out_of_bounds(self):
        for collection, fields in app.SCALE_FIELDS.items():
            for field in fields:
                for value in (True, False, 0, 5, 2.0, "2", None):
                    with self.subTest(collection=collection, field=field, value=value):
                        changed = copy.deepcopy(self.data)
                        changed[collection][0][field] = value
                        self.assertTrue(app.validate(changed, self.root))

    def test_dates_require_valid_iso_calendar_dates(self):
        for value in ("2026-02-30", "20261112", "12/11/2026", "2026-11-12T00:00:00Z", True):
            with self.subTest(value=value):
                changed = copy.deepcopy(self.data)
                changed["metadata"]["created"] = value
                changed["treatment_actions"][0]["due_date"] = value
                self.assertGreaterEqual(len(app.validate(changed, self.root)), 2)

    def test_initial_risk_is_traced_to_event_and_operational_scenario(self):
        self.data["risks"][0].update(initial_severity=3, initial_likelihood=2)
        errors = self.errors()
        self.assertIn("gravité initiale", "\n".join(errors))
        self.assertIn("vraisemblance initiale", "\n".join(errors))

    def test_strategic_scenario_cannot_use_unretained_pair(self):
        self.data["source_objective_pairs"][0]["retained"] = False
        self.errors("paire non retenue")

    def test_retained_value_requires_boolean_not_integer(self):
        self.data["source_objective_pairs"][0]["retained"] = 1
        self.errors("booléen requis")

    def test_risk_action_links_are_reciprocal_both_directions(self):
        self.data["treatment_actions"][0]["risk_ids"] = []
        self.errors("non réciproque")
        self.data = fixture()
        self.data["risks"][0]["action_ids"] = []
        self.errors("non réciproque")

    def test_unknown_status_is_invalid(self):
        self.data["risks"][0]["status"] = "certified"
        self.data["treatment_actions"][0]["status"] = "deployed"
        self.errors("statut")

    def test_evidence_path_must_be_relative_and_contained(self):
        for name in ("../outside.txt", str(self.root / "evidence/checks.txt"),
                     "C:\\secrets\\key.txt", "\\\\server\\share\\x.txt", "evidence/../../x", "a\x00b"):
            with self.subTest(name=name):
                changed = copy.deepcopy(self.data)
                changed["evidence"][0]["path"] = name
                self.assertTrue(app.validate(changed, self.root))

    def test_evidence_must_exist_and_be_a_file(self):
        self.data["evidence"][0]["path"] = "evidence/missing.txt"
        self.errors()
        self.data["evidence"][0]["path"] = "evidence"
        self.errors("fichier existant")

    def test_duplicate_evidence_path_detects_equivalent_paths(self):
        self.data["evidence"].append({"id": "EV2", "path": "evidence/./checks.txt", "description": "Autre référence"})
        self.errors("chemin de preuve dupliqué")

    def test_evidence_symlink_cannot_escape_or_alias_local_file(self):
        link = self.root / "evidence/link.txt"
        try:
            link.symlink_to(self.root / "evidence/checks.txt")
        except (OSError, NotImplementedError):
            self.skipTest("Symlink creation is unavailable to this account")
        self.data["evidence"][0]["path"] = "evidence/link.txt"
        self.errors("lien symbolique")
        link.unlink()
        outside = Path(self.tmp.name).parent / (self.root.name + "-outside")
        outside.write_text("Synthetic outside fixture", encoding="utf-8")
        self.addCleanup(outside.unlink, missing_ok=True)
        link.symlink_to(outside)
        self.errors("lien symbolique")

    def test_parent_directory_symlink_is_rejected(self):
        link = self.root / "alias"
        try:
            link.symlink_to(self.root / "evidence", target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest("Symlink creation is unavailable to this account")
        self.data["evidence"][0]["path"] = "alias/checks.txt"
        self.errors("lien symbolique")

    def test_implemented_action_and_baseline_need_evidence(self):
        self.data["treatment_actions"][0]["status"] = "implemented_in_lab"
        self.data["baseline_controls"][0]["status"] = "implemented_in_lab"
        errors = self.errors("sans preuve")
        self.assertEqual(sum("sans preuve" in error for error in errors), 2)

    def test_planned_or_documented_measure_cannot_reduce_current_risk(self):
        self.data["risks"][0]["current_likelihood"] = 2
        for status in ("planned", "documented"):
            with self.subTest(status=status):
                self.data["treatment_actions"][0].update(status=status, evidence_ids=["EV1"])
                self.errors("baisse du risque courant")

    def test_each_reduced_dimension_requires_implemented_evidence(self):
        self.data["risks"][0].update(current_severity=3, current_likelihood=4)
        # Same total score (12) still contains a lowered severity dimension.
        self.errors("baisse du risque courant")

    def test_implemented_evidence_can_support_local_reduction_but_not_empty_rationale(self):
        self.implement()
        self.data["risks"][0]["current_likelihood"] = 2
        self.assertEqual(app.validate(self.data, self.root), [])
        self.data["risks"][0]["current_rationale"] = " "
        self.errors()

    def test_target_is_separate_and_does_not_reduce_reported_current_score(self):
        report = app.build_report(self.data, self.root)
        risk = report["risks"][0]
        self.assertEqual(risk["initial"]["score"], 12)
        self.assertEqual(risk["current"]["score"], 12)
        self.assertEqual(risk["target"]["score"], 4)
        self.assertEqual(report["summary"]["actions_by_status"],
                         {"planned": 1, "documented": 0, "implemented_in_lab": 0})

    def test_simulated_acceptance_rejects_unimplemented_actions_and_missing_record(self):
        self.data["risks"][0]["status"] = "accepted_simulated"
        errors = self.errors()
        self.assertIn("sans toutes les actions", "\n".join(errors))
        self.assertIn("dossier d'acceptation simulée", "\n".join(errors))

    def test_simulated_acceptance_requires_true_flag_reviewer_date_and_rationale(self):
        self.implement()
        risk = self.data["risks"][0]
        risk.update(status="accepted_simulated", acceptance={
            "reviewer": "Comité fictif", "date": "2026-11-12", "rationale": "Exercice uniquement", "simulated": True
        })
        self.assertEqual(app.validate(self.data, self.root), [])
        valid = copy.deepcopy(risk["acceptance"])
        for field, value in (("reviewer", ""), ("date", "2026-02-30"), ("rationale", None), ("simulated", 1)):
            with self.subTest(field=field):
                risk["acceptance"] = copy.deepcopy(valid)
                risk["acceptance"][field] = value
                self.errors("acceptance")

    def test_open_risk_cannot_hide_acceptance_and_treated_needs_all_actions(self):
        self.data["risks"][0]["acceptance"] = {"simulated": True}
        self.errors("null requis")
        self.data["risks"][0].update(acceptance=None, status="treated")
        self.errors("sans toutes les actions")
        self.implement()
        self.assertEqual(app.validate(self.data, self.root), [])

    def test_evidence_hashes_and_size_are_recomputed_from_actual_bytes(self):
        proof = self.root / "evidence/checks.txt"
        first = app.build_report(self.data, self.root)["evidence"][0]
        self.assertEqual(first["sha256"], hashlib.sha256(proof.read_bytes()).hexdigest())
        self.assertEqual(first["size_bytes"], len(proof.read_bytes()))
        proof.write_bytes(b"Changed synthetic evidence\x00\xff")
        second = app.build_report(self.data, self.root)["evidence"][0]
        self.assertNotEqual(first["sha256"], second["sha256"])
        self.assertEqual(second["size_bytes"], 28)

    def test_report_levels_and_markdown_preserve_local_warning(self):
        for severity, likelihood, level in ((1, 3, "faible"), (2, 2, "modéré"), (3, 3, "élevé"), (4, 3, "critique")):
            with self.subTest(level=level):
                changed = copy.deepcopy(self.data)
                changed["feared_events"][0]["severity"] = severity
                changed["operational_scenarios"][0]["likelihood"] = likelihood
                changed["risks"][0].update(initial_severity=severity, current_severity=severity,
                                            initial_likelihood=likelihood, current_likelihood=likelihood)
                report = app.build_report(changed, self.root)
                self.assertEqual(report["risks"][0]["current"]["level"], level)
                markdown = app.render_markdown(report)
                self.assertTrue(markdown.startswith("> **EXERCICE PÉDAGOGIQUE"))
                self.assertIn("Cible non acquise", markdown)
                self.assertIn("non une prescription ISO", markdown)

    def test_report_is_deterministic_and_json_utf8_is_valid(self):
        self.write_data()
        code, _, errors = self.run_cli("report")
        self.assertEqual((code, errors), (0, ""))
        before = {path.name: path.read_bytes() for path in (self.root / "reports").iterdir()}
        self.assertEqual(set(before), {"report.json", "report.md"})
        self.assertIn("PÉDAGOGIQUE", before["report.json"].decode("utf-8"))
        self.assertEqual(json.loads(before["report.json"])["risks"][0]["current"]["score"], 12)
        self.assertEqual(self.run_cli("report")[0], 0)
        self.assertEqual(before, {path.name: path.read_bytes() for path in (self.root / "reports").iterdir()})

    def test_invalid_data_creates_no_report_and_preserves_existing_output(self):
        self.data["risks"][0]["current_likelihood"] = 1
        self.write_data()
        self.assertEqual(self.run_cli("report")[0], 1)
        self.assertFalse((self.root / "reports").exists())
        (self.root / "reports").mkdir()
        for name in ("report.json", "report.md"):
            (self.root / "reports" / name).write_text("Existing valid output", encoding="utf-8")
        self.assertEqual(self.run_cli("report")[0], 1)
        for path in (self.root / "reports").iterdir():
            self.assertEqual(path.read_text(encoding="utf-8"), "Existing valid output")

    def test_json_syntax_duplicate_keys_and_nonstandard_constants_fail_cleanly(self):
        for raw in ('{"metadata":', '{"metadata":{},"metadata":{}}', '{"metadata":NaN}'):
            with self.subTest(raw=raw):
                self.write_data(raw)
                code, _, errors = self.run_cli("report")
                self.assertEqual(code, 1)
                self.assertIn("Erreur", errors)
                self.assertFalse((self.root / "reports").exists())

    def test_cli_refuses_external_input_or_output_and_supports_custom_relative_paths(self):
        self.write_data()
        self.assertEqual(self.run_cli("validate", "--data", "../outside.json")[0], 1)
        self.assertEqual(self.run_cli("report", "--output", "../outside")[0], 1)
        self.assertEqual(self.run_cli("report", "--output", "results/nested")[0], 0)
        self.assertTrue((self.root / "results/nested/report.json").is_file())

    def test_cli_resolves_paths_from_its_project_root_not_working_directory(self):
        self.write_data()
        shutil.copyfile(Path(app.__file__), self.root / "app.py")
        elsewhere = self.root / "unrelated-cwd"
        elsewhere.mkdir()
        result = subprocess.run([sys.executable, str(self.root / "app.py"), "validate"], cwd=elsewhere,
                                capture_output=True, text=True, encoding="utf-8", errors="replace", check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("VALID", result.stdout)
        result = subprocess.run([sys.executable, str(self.root / "app.py"), "report"], cwd=elsewhere,
                                capture_output=True, text=True, encoding="utf-8", errors="replace", check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.root / "reports/report.md").is_file())
        self.assertFalse((elsewhere / "reports").exists())

    def test_build_report_refuses_invalid_data_without_partial_object(self):
        self.data["evidence"][0]["path"] = "missing"
        with self.assertRaises(ValueError):
            app.build_report(self.data, self.root)


if __name__ == "__main__":
    unittest.main()


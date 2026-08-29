from __future__ import annotations

import importlib.util
import json
import re
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"nao foi possivel importar {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


registry = load_module("build_registry", ROOT / "scripts" / "build-registry.py")
v4mos = load_module(
    "v4mos_meta",
    ROOT / ".claude" / "skills" / "v4mos-dados-meta-ads" / "scripts" / "v4mos_meta.py",
)


class RegistryTests(unittest.TestCase):
    def test_novo_squad_is_a_base_skill(self):
        self.assertEqual(("base", "_base"), registry.classify("novo-squad", {}))

    def test_render_is_deterministic_and_has_no_dynamic_date(self):
        first = registry.render_registry()
        second = registry.render_registry()
        self.assertEqual(first, second)
        self.assertNotIn("última atualização", first)
        self.assertIn("`novo-squad`", first)


class V4mosClientResolutionTests(unittest.TestCase):
    def make_repo(self, root: Path) -> None:
        (root / "AGENTS.md").write_text("hub", encoding="utf-8")
        (root / "squads").mkdir()

    def make_client(self, root: Path, squad: str, client: str) -> Path:
        client_dir = root / "squads" / squad / "clientes" / client
        client_dir.mkdir(parents=True)
        return client_dir

    def test_resolves_explicit_squad_and_client(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            self.make_repo(root)
            client_dir = self.make_client(root, "alpha", "acme")
            env, client = v4mos.find_client_env("acme", "alpha", root)
            self.assertEqual((client_dir / ".env").resolve(), env)
            self.assertEqual("acme", client)

    def test_detects_client_from_nested_cwd(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            self.make_repo(root)
            client_dir = self.make_client(root, "alpha", "acme")
            nested = client_dir / "campanhas" / "2026"
            nested.mkdir(parents=True)
            env, client = v4mos.find_client_env(None, start=nested)
            self.assertEqual((client_dir / ".env").resolve(), env)
            self.assertEqual("acme", client)

    def test_requires_squad_for_duplicate_client_names(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            self.make_repo(root)
            self.make_client(root, "alpha", "acme")
            self.make_client(root, "beta", "acme")
            with self.assertRaisesRegex(ValueError, "mais de um squad"):
                v4mos.find_client_env("acme", start=root)

    def test_missing_client_does_not_create_directories(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            self.make_repo(root)
            env, client = v4mos.find_client_env("inexistente", "alpha", root)
            self.assertIsNone(env)
            self.assertEqual("inexistente", client)
            self.assertFalse(
                (root / "squads" / "alpha" / "clientes" / "inexistente").exists()
            )


class V4mosDataTests(unittest.TestCase):
    def test_sort_keeps_missing_values_last(self):
        rows = [{"spend": None}, {"spend": "2"}, {"spend": 10}]
        self.assertEqual(
            [10, "2", None],
            [row["spend"] for row in v4mos.sort_rows(rows, "spend", "DESC")],
        )

    def test_csv_neutralizes_formula_injection(self):
        rendered = v4mos.render_csv([{"ad_name": '=HYPERLINK("bad")', "spend": -2}])
        self.assertIn("'=HYPERLINK", rendered)
        self.assertIn(",-2", rendered)

    def test_where_numeric_filter(self):
        predicate = v4mos.parse_where("spend>=10")
        self.assertTrue(predicate({"spend": "12.5"}))
        self.assertFalse(predicate({"spend": 9}))

    def test_retries_transient_server_error(self):
        class Response:
            def __init__(self, status, payload=None):
                self.status_code = status
                self.headers = {}
                self.payload = payload or {}

            def raise_for_status(self):
                if self.status_code >= 400:
                    raise RuntimeError(self.status_code)

            def json(self):
                return self.payload

        class Requests:
            def __init__(self):
                self.responses = [
                    Response(500),
                    Response(
                        200, {"data": [{"id": 1}], "meta": {"hasNextPage": False}}
                    ),
                ]
                self.calls = 0

            def get(self, *args, **kwargs):
                response = self.responses[self.calls]
                self.calls += 1
                return response

        fake_requests = Requests()
        original_requests, original_sleep = v4mos.requests, v4mos.time.sleep
        try:
            v4mos.requests = fake_requests
            v4mos.time.sleep = lambda _: None
            client = v4mos.V4mos(
                {
                    "V4MOS_CLIENT_ID": "id",
                    "V4MOS_CLIENT_SECRET": "secret",
                    "V4MOS_WORKSPACE_ID": "workspace",
                }
            )
            self.assertEqual([{"id": 1}], client.get("/test"))
            self.assertEqual(2, fake_requests.calls)
        finally:
            v4mos.requests, v4mos.time.sleep = original_requests, original_sleep

    def test_rejects_conflicting_or_invalid_cli_ranges(self):
        base = {
            "days": None,
            "since": None,
            "until": None,
            "limit": 500,
            "max": None,
        }
        with self.assertRaisesRegex(SystemExit, "--limit"):
            v4mos.validate_args(SimpleNamespace(**{**base, "limit": 5001}))
        with self.assertRaisesRegex(SystemExit, "não os dois"):
            v4mos.validate_args(
                SimpleNamespace(**{**base, "days": 7, "since": "2026-08-01"})
            )
        with self.assertRaisesRegex(SystemExit, "posterior"):
            v4mos.validate_args(
                SimpleNamespace(
                    **{
                        **base,
                        "since": "2026-08-02",
                        "until": "2026-08-01",
                    }
                )
            )


class TemplateTests(unittest.TestCase):
    def test_project_template_context_files_match(self):
        template = ROOT / "bases" / "_template" / "_template-projeto"
        self.assertEqual(
            (template / "CLAUDE.md").read_bytes(),
            (template / "AGENTS.md").read_bytes(),
        )
        for directory in ("docs", "dados", "referencias"):
            self.assertTrue((template / directory / ".gitkeep").is_file())

    def test_kickoff_template_contains_only_generic_payload(self):
        template = (
            ROOT
            / ".claude"
            / "skills"
            / "account-handoff"
            / "assets"
            / "template-kickoff.html"
        )
        text = template.read_text(encoding="utf-8")
        match = re.search(
            r'<script id="dados-handoff" type="application/json">\s*(.*?)\s*</script>',
            text,
            re.DOTALL,
        )
        self.assertIsNotNone(match)
        payload = json.loads(match.group(1))
        self.assertEqual("[Nome do cliente]", payload["capa"]["cliente"])
        serialized = json.dumps(payload, ensure_ascii=False)
        self.assertNotRegex(serialized, r"@[a-z0-9._-]+")
        self.assertNotRegex(serialized, r"\bhttps?://|\bwww\.|\.com\.br\b")
        self.assertNotIn("R$", serialized)


if __name__ == "__main__":
    unittest.main()

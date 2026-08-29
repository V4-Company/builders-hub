from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

SCRIPT = pathlib.Path(__file__).parents[1] / "scripts" / "plano-backup.py"


def rodar(kb: pathlib.Path, *args: str) -> tuple[dict, str]:
    processo = subprocess.run(
        [sys.executable, str(SCRIPT), str(kb), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(processo.stdout), processo.stderr


class PlanoBackupTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.kb = pathlib.Path(self.tmp.name) / "cliente-x"
        (self.kb / "calls").mkdir(parents=True)
        (self.kb / "mission-control").mkdir()
        (self.kb / "calls" / "reuniao.md").write_text("call", encoding="utf-8")
        (self.kb / "mission-control" / "personas-call.md").write_text(
            "interno", encoding="utf-8"
        )
        (self.kb / ".env").write_text("TOKEN=nao-subir", encoding="utf-8")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_modo_material_exclui_interno_e_segredo(self) -> None:
        plano, _ = rodar(self.kb, "--modo", "material", "--destino", "pasta-a")
        self.assertEqual(plano["resumo"]["selecionados"], 1)
        self.assertEqual(plano["resumo"]["a_subir"], 1)
        self.assertEqual(plano["pastas"], ["calls"])
        self.assertEqual(plano["segredo"][0]["caminho"], ".env")

    def test_manifesto_so_e_reutilizado_no_mesmo_destino(self) -> None:
        inicial, _ = rodar(self.kb, "--destino", "pasta-a")
        item = inicial["material"][0]
        manifesto = {
            "pasta_destino": "pasta-a",
            "arquivos": {item["caminho"]: {"id": "id-remoto", "sha": item["sha"]}},
        }
        (self.kb / ".backup-drive.json").write_text(
            json.dumps(manifesto), encoding="utf-8"
        )

        mesmo, _ = rodar(self.kb, "--destino", "pasta-a")
        outro, stderr = rodar(self.kb, "--destino", "pasta-b")

        self.assertTrue(mesmo["manifesto_compativel"])
        self.assertEqual(mesmo["resumo"]["ja_atualizados"], 1)
        self.assertFalse(outro["manifesto_compativel"])
        self.assertEqual(outro["resumo"]["a_subir"], 2)
        self.assertIn("o destino mudou", stderr)

    def test_link_simbolico_e_ignorado_sem_ler_o_alvo(self) -> None:
        alvo = pathlib.Path(self.tmp.name) / "fora.txt"
        alvo.write_text("fora do escopo", encoding="utf-8")
        link = self.kb / "calls" / "atalho.txt"
        try:
            link.symlink_to(alvo)
        except OSError as exc:
            self.skipTest(f"ambiente sem suporte a symlink: {exc}")

        plano, _ = rodar(self.kb, "--destino", "pasta-a")
        ignorados = {item["caminho"]: item for item in plano["segredo"]}
        self.assertEqual(
            ignorados["calls/atalho.txt"]["motivo"], "link simbolico ignorado"
        )


if __name__ == "__main__":
    unittest.main()

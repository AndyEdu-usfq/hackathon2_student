from __future__ import annotations

from pathlib import Path

import nbformat
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError


ROOT = Path(__file__).resolve().parent
NOTEBOOK = ROOT / "Hackathon_2_Starter.ipynb"
OUTPUT = ROOT / "output" / "Hackathon_2_Verificado.ipynb"


def main() -> None:
    notebook = nbformat.read(NOTEBOOK, as_version=4)
    sources = "\n".join(cell.source for cell in notebook.cells)

    pending = [marker for marker in ("TODO", "RESPUESTA AQUÍ") if marker in sources]
    if pending:
        raise SystemExit(
            "El notebook todavía contiene marcadores pendientes: " + ", ".join(pending)
        )

    try:
        client = NotebookClient(
            notebook,
            timeout=180,
            kernel_name="python3",
            resources={"metadata": {"path": str(ROOT)}},
        )
        client.execute()
    except CellExecutionError as exc:
        raise SystemExit(f"La ejecución desde cero falló:\n{exc}") from exc

    expected_plot = ROOT / "output" / "pca_penguins.png"
    if not expected_plot.exists() or expected_plot.stat().st_size == 0:
        raise SystemExit("No se creó output/pca_penguins.png.")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    nbformat.write(notebook, OUTPUT)
    print("VERIFICACIÓN COMPLETA")
    print(f"Notebook ejecutado: {OUTPUT.relative_to(ROOT)}")
    print(f"Gráfico encontrado: {expected_plot.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

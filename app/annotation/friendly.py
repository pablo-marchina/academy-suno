#!/usr/bin/env python3
"""Portuguese guided interface for W004 blind primary annotation."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from suno_content.annotation.operator import (  # noqa: E402
    CHECK_VALUES,
    DIMENSIONS,
    LABELS,
    export_jsonl,
    get_blind_item,
    load_session,
    make_record,
    status,
    submit_record,
)

DIMENSION_HELP = {
    "D1_JARGON_CONTEXTUALIZATION": (
        "Os termos financeiros são explicados ou o texto assume que você já conhece?",
        "0 = simples/explicado | 1 = algum conhecimento prévio | 2 = técnico/especializado",
    ),
    "D2_BACKGROUND_ASSUMED": (
        "Quanto conhecimento financeiro prévio o leitor precisa para acompanhar?",
        "0 = pouco | 1 = conhecimento intermediário | 2 = bastante conhecimento técnico",
    ),
    "D3_CONCEPTUAL_DEPTH": (
        "Quão profunda é a análise para entender o conteúdo?",
        "0 = explica o essencial | 1 = interpreta relações/tendências | 2 = análise técnica/metodológica",
    ),
    "D4_CONTENT_FOCUS": (
        "Qual é o foco dominante do conteúdo?",
        "0 = o que é/por que importa | 1 = interpretação de mercado | 2 = análise técnica/mecanismos",
    ),
    "D5_TECHNICITY_PRESERVATION": (
        "Quanto detalhe técnico foi mantido no conteúdo?",
        "0 = simplificado | 1 = termos e relações centrais | 2 = alta granularidade/nuance técnica",
    ),
}

LABEL_HELP = {
    "BEGINNER": "iniciante: pouco conhecimento prévio, explicações mais simples",
    "INTERMEDIATE": "intermediário: pressupõe conceitos financeiros básicos",
    "ADVANCED": "avançado: pressupõe repertório técnico/institucional",
    "UNSCORABLE": "não classificável: texto quebrado, incoerente ou sem nível dominante defensável",
}

CHECK_HELP = {
    "FACTUAL_CRITICAL_PRESERVATION": (
        "Existe erro factual importante, contradição com a fonte ou perda de ressalva essencial?"
    ),
    "MATERIAL_CONCEPT_PRESERVATION": (
        "Algum conceito essencial da fonte foi perdido ou distorcido para simplificar o texto?"
    ),
    "FORMAT_NATIVE_CONTRACT": (
        "O conteúdo parece adequado ao formato informado (artigo, carrossel ou vídeo curto)?"
    ),
}


def _choice(question: str, choices: tuple[str, ...], help_lines: dict[str, str] | None = None) -> str:
    while True:
        print(f"\n{question}")
        if help_lines:
            for key in choices:
                if key in help_lines:
                    print(f"  {key}: {help_lines[key]}")
        value = input(f"Escolha [{'/'.join(choices)}]\n> ").strip().upper()
        if value in choices:
            return value
        print("Resposta inválida. Escolha exatamente uma das opções mostradas.")


def _dimension(key: str) -> int:
    question, legend = DIMENSION_HELP[key]
    while True:
        print(f"\n{question}")
        print(f"  {legend}")
        value = input("Escolha [0/1/2]\n> ").strip()
        if value in {"0", "1", "2"}:
            return int(value)
        print("Resposta inválida. Digite somente 0, 1 ou 2.")


def _check(key: str) -> str:
    print(f"\n{CHECK_HELP[key]}")
    if key == "FORMAT_NATIVE_CONTRACT":
        help_lines = {
            "PASS": "sim, o formato está adequado",
            "FAIL": "não, há problema claro de formato",
            "NOT_APPLICABLE": "não consigo avaliar esse formato aqui",
            "REVIEW_REQUIRED": "tenho dúvida e gostaria de revisão",
        }
    else:
        help_lines = {
            "PASS": "não identifiquei problema material",
            "FAIL": "identifiquei problema material",
            "REVIEW_REQUIRED": "tenho dúvida e gostaria de revisão",
        }
    choices = tuple(sorted(CHECK_VALUES[key]))
    return _choice("Sua avaliação:", choices, help_lines)


def _show_item(item: dict, completed: int, total: int) -> None:
    print("\n" + "=" * 80)
    print(f"ITEM {completed + 1} DE {total}")
    print("=" * 80)
    print(f"Formato: {item.get('format', 'N/A')}")
    print("\nCONTEÚDO A AVALIAR:\n")
    print(item.get("output_text", ""))
    context = item.get("source_check_context")
    if context:
        print("\nCONTEXTO DA FONTE PARA CHECAGEM FACTUAL:\n")
        print(json.dumps(context, indent=2, ensure_ascii=False))
    print("\nResponda pela sua percepção. Não existe resposta sugerida pelo sistema.")


def _collect_record(root: Path, session: dict) -> dict:
    st = status(session)
    item = get_blind_item(root, session)
    item_id = item.get("item_id", item.get("blind_item_id"))
    _show_item(item, st["completed"], st["total"])

    dimensions = {key: _dimension(key) for key in DIMENSIONS}
    label = _choice(
        "No geral, para qual nível de público este conteúdo parece ter sido escrito?",
        tuple(LABELS),
        LABEL_HELP,
    )
    mixed = (
        _choice(
            "O conteúdo mistura de forma relevante níveis diferentes de dificuldade?",
            ("SIM", "NAO"),
            {
                "SIM": "há partes claramente de níveis diferentes",
                "NAO": "há um nível dominante suficientemente claro",
            },
        )
        == "SIM"
    )

    checks = {key: _check(key) for key in CHECK_VALUES}
    confidence = _choice(
        "Quão confiante você está na sua avaliação?",
        ("LOW", "MEDIUM", "HIGH"),
        {
            "LOW": "baixa confiança",
            "MEDIUM": "confiança média",
            "HIGH": "alta confiança",
        },
    )

    reason = None
    if label == "UNSCORABLE":
        while not reason:
            reason = input("Explique brevemente por que este item não é classificável:\n> ").strip()

    notes = input("Observação opcional (Enter para deixar vazio):\n> ")
    return make_record(
        session,
        item_id,
        audience_label=label,
        dimensions=dimensions,
        mixed_level_flag=mixed,
        checks=checks,
        confidence=confidence,
        notes=notes,
        unscorable_reason=reason,
    )


def _default_output(session_path: Path, session: dict) -> Path:
    return session_path.parent / f"annotations_{session['annotation_role'].lower()}.jsonl"


def run_guided(root: Path, session_path: Path, output: Path | None = None) -> int:
    try:
        while True:
            session = load_session(root, session_path)
            st = status(session)
            if st["complete"]:
                destination = output or _default_output(session_path, session)
                exported, provenance = export_jsonl(root, session_path, destination)
                print("\n" + "=" * 80)
                print("ANOTAÇÃO CONCLUÍDA")
                print(f"Itens concluídos: {st['completed']}/{st['total']}")
                print(f"Export: {exported}")
                print(f"Proveniência: {provenance}")
                return 0

            record = _collect_record(root, session)
            new_status = submit_record(root, session_path, record)
            print(f"\nSalvo com sucesso: {new_status['completed']}/{new_status['total']} concluídos.")
            print("O próximo item será aberto automaticamente.")
    except KeyboardInterrupt:
        session = load_session(root, session_path)
        st = status(session)
        print("\n\nInterrompido pelo usuário. O progresso já salvo foi preservado.")
        print(f"Progresso atual: {st['completed']}/{st['total']}.")
        print("Rode o mesmo comando depois para continuar do próximo item.")
        return 130


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Interface guiada em português para as anotações humanas cegas de W004. "
            "Percorre automaticamente todos os itens restantes e salva após cada item."
        )
    )
    parser.add_argument("--session", required=True, type=Path)
    parser.add_argument("--repo-root", default=".", type=lambda p: Path(p).expanduser().resolve())
    parser.add_argument("--output", type=Path, help="Destino opcional do JSONL final.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return run_guided(args.repo_root, args.session, args.output)


if __name__ == "__main__":
    raise SystemExit(main())

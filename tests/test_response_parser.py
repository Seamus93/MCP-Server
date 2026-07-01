from workflow.response_parser import ChatGPTResponseParser


def test_parser_extracts_required_sections() -> None:
    response = """
Sintesi
Parser pronto.

Piano operativo
- creare tool ingest
- salvare JSON

File da modificare
- server/main.py
- workflow/response_parser.py

Test consigliati
pytest

Rischi
Formato risposta variabile.

Prossima azione
Eseguire test.
"""
    parsed = ChatGPTResponseParser().parse(response)

    assert parsed.status == "planned"
    assert parsed.summary == "Parser pronto."
    assert "creare tool" in parsed.plan
    assert "server/main.py" in parsed.files_to_modify
    assert parsed.next_action == "Eseguire test."


def test_parser_marks_missing_sections_for_review() -> None:
    parsed = ChatGPTResponseParser().parse("Risposta libera senza struttura")

    assert parsed.status == "needs_review"
    assert "missing_plan" in parsed.warnings
    assert "missing_next_action" in parsed.warnings

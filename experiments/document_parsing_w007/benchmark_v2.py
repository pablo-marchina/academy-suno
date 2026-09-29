from __future__ import annotations

import benchmark as base


def role_metrics(tables: list[dict], gold: list[dict]) -> dict:
    """Score table roles while allowing a logical row to span adjacent physical rows.

    The hard requirement is unchanged: a target only counts when the parser preserves
    (1) the named column, (2) the row label, and (3) the expected value in that
    column. We allow the value to appear up to two physical rows after the row-label
    row because source-original table geometry can split one logical row vertically.
    """
    if not gold:
        return {
            "applicable": False,
            "true_positive": None,
            "false_positive": None,
            "recall": None,
            "precision": None,
            "assertions": [],
        }

    assertions = []
    tp = fp = 0
    for target in gold:
        expected = base.norm(target["value"])
        asserted = None
        evidence = None
        for table in tables:
            rows = table.get("cells") or []
            column_index = None
            header_row = None
            for ri, row in enumerate(rows[:8]):
                for ci, cell in enumerate(row or []):
                    if base.norm(target["column"]) == base.norm(cell):
                        header_row, column_index = ri, ci
                        break
                if column_index is not None:
                    break
            if column_index is None:
                continue

            for ri in range((header_row or 0) + 1, len(rows)):
                row = rows[ri] or []
                joined = " | ".join(base.norm(c) for c in row)
                if base.norm(target["row"]) not in joined:
                    continue
                # A logical row may be split over the label row + up to two
                # following physical rows. Do not search beyond that local span.
                for value_ri in range(ri, min(ri + 3, len(rows))):
                    value_row = rows[value_ri] or []
                    if column_index < len(value_row):
                        candidate = base.norm(value_row[column_index])
                        if candidate:
                            asserted = candidate
                            evidence = {
                                "table_index": table.get("table_index"),
                                "header_row_index": header_row,
                                "row_label_index": ri,
                                "value_row_index": value_ri,
                                "column_index": column_index,
                            }
                            break
                break
            if asserted is not None:
                break

        if asserted is not None:
            ok = expected == asserted
            tp += int(ok)
            fp += int(not ok)
            assertions.append(
                {
                    "row": target["row"],
                    "column": target["column"],
                    "expected": target["value"],
                    "asserted": asserted,
                    "correct": ok,
                    "evidence": evidence,
                }
            )

    recall = tp / len(gold)
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    return {
        "applicable": True,
        "true_positive": tp,
        "false_positive": fp,
        "recall": recall,
        "precision": precision,
        "assertions": assertions,
    }


base.role_metrics = role_metrics

if __name__ == "__main__":
    base.main()

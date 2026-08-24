import json
from pathlib import Path


DEFAULT_LOG_PATH = Path(
    "logs/decision_trace.jsonl"
)


def save_trace(
    trace: dict,
    log_path=DEFAULT_LOG_PATH,
):
    """
    Decision trace kaydını JSONL formatında
    log dosyasına ekler.

    Her satır bağımsız bir JSON kaydıdır.
    """

    log_path = Path(log_path)

    # logs klasörü yoksa oluştur.
    log_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with log_path.open(
        "a",
        encoding="utf-8",
    ) as log_file:

        json.dump(
            trace,
            log_file,
            ensure_ascii=False,
        )

        log_file.write("\n")


def read_traces(
    log_path=DEFAULT_LOG_PATH,
):
    """
    JSONL dosyasındaki bütün trace
    kayıtlarını liste olarak okur.
    """

    log_path = Path(log_path)

    if not log_path.exists():
        return []

    traces = []

    with log_path.open(
        "r",
        encoding="utf-8",
    ) as log_file:

        for line in log_file:

            line = line.strip()

            if not line:
                continue

            traces.append(
                json.loads(line)
            )

    return traces